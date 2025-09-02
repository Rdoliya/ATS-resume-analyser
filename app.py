import os
import logging
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from services.parser import ResumeParser
from services.scorer import ATSScorer
from services.suggestions import SuggestionEngine

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Enable CORS for API endpoints
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize services
resume_parser = ResumeParser()
ats_scorer = ATSScorer()
suggestion_engine = SuggestionEngine()

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Serve the main application page."""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    """
    API endpoint to analyze uploaded resume.
    Returns ATS score and improvement suggestions.
    """
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            }), 400

        file = request.files['file']
        
        # Check if file was selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400

        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Please upload PDF or DOCX files only.'
            }), 400

        # Save uploaded file
        filename = secure_filename(file.filename or "resume")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Parse resume content
            logging.debug(f"Parsing file: {filepath}")
            resume_data = resume_parser.parse(filepath)
            
            if not resume_data or not resume_data.get('text'):
                return jsonify({
                    'success': False,
                    'error': 'Failed to extract text from the document. Please ensure the file is not corrupted.'
                }), 400

            # Calculate ATS score
            logging.debug("Calculating ATS score")
            score_data = ats_scorer.calculate_score(resume_data)
            
            # Generate improvement suggestions
            logging.debug("Generating suggestions")
            suggestions = suggestion_engine.generate_suggestions(resume_data, score_data)
            
            # Prepare response
            response = {
                'success': True,
                'filename': filename,
                'overall_score': score_data['overall_score'],
                'score_breakdown': score_data['breakdown'],
                'suggestions': suggestions,
                'resume_stats': {
                    'word_count': resume_data.get('word_count', 0),
                    'sections_found': list(resume_data.get('sections', {}).keys()),
                    'contact_info_present': bool(resume_data.get('contact_info')),
                    'skills_found': len(resume_data.get('skills', [])),
                    'experience_entries': len(resume_data.get('experience', [])),
                    'education_entries': len(resume_data.get('education', []))
                }
            }
            
            return jsonify(response)

        finally:
            # Clean up uploaded file
            try:
                os.remove(filepath)
            except OSError:
                logging.warning(f"Failed to remove temporary file: {filepath}")

    except Exception as e:
        logging.error(f"Error analyzing resume: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while analyzing the resume. Please try again.'
        }), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum file size is 16MB.'
    }), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return render_template('index.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
