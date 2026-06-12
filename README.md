# Resume ATS Scorer

A powerful full-stack web application that analyzes uploaded resumes for Applicant Tracking System (ATS) compatibility and provides actionable suggestions for improvement.

## 🚀 Features

- **Document Processing**: Support for PDF and DOCX resume uploads
- **Advanced ATS Scoring**: Comprehensive evaluation based on 6 key criteria
- **Smart Analysis**: NLP-powered text analysis using spaCy
- **Real-time Visualization**: Interactive score charts and progress bars
- **Actionable Suggestions**: Prioritized recommendations for improvement
- **Modern UI**: Responsive design with Bootstrap and dark theme
- **Secure File Handling**: Automatic file cleanup after processing
- **RESTful API**: Clean API endpoints for integration

## 📋 Requirements

### System Requirements
- Python 3.11 or higher
- Node.js (for frontend dependencies via CDN)
- At least 1GB RAM
- 500MB free disk space

### Python Dependencies
- Flask (web framework)
- Flask-CORS (cross-origin resource sharing)
- python-docx (DOCX file processing)
- PyPDF2 (PDF file processing)
- spaCy (natural language processing)
- Werkzeug (file handling utilities)
- Gunicorn (production WSGI server)

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd resume-ats-scorer
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
# Using pip
pip install flask flask-cors python-docx PyPDF2 spacy gunicorn

# Or using uv (faster package manager)
uv add flask flask-cors python-docx PyPDF2 spacy gunicorn
```

### 4. Download spaCy Language Model
```bash
python -m spacy download en_core_web_sm
```

### 5. Set Environment Variables
Create a `.env` file in the root directory:
```bash
# .env file
SESSION_SECRET=your-secret-key-here-change-in-production
FLASK_ENV=development
FLASK_DEBUG=1
```

## 🏃‍♂️ Running the Application

### Development Mode
```bash
# Method 1: Using Flask directly
python app.py

# Method 2: Using Gunicorn (recommended)
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app

# Method 3: Using Python module
python -m flask --app app run --host=0.0.0.0 --port=5000
```

### Production Mode
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

The application will be available at: `http://localhost:5000`
or 
"http://192.168.1.66:5000"

## 📁 Project Structure

```
resume-ats-scorer/
├── app.py                 # Main Flask application
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── services/            # Business logic modules
│   ├── parser.py        # Resume parsing logic
│   ├── scorer.py        # ATS scoring algorithms
│   └── suggestions.py   # Improvement suggestions engine
├── static/              # Frontend assets
│   ├── css/
│   │   └── style.css    # Custom styles
│   └── js/
│       └── main.js      # Frontend JavaScript logic
├── templates/           # HTML templates
│   └── index.html       # Main application page
└── uploads/             # Temporary file storage (auto-cleaned)
    └── .gitkeep
```

## 🔧 Configuration

### Application Settings
- **Maximum file size**: 16MB
- **Supported formats**: PDF, DOCX
- **Upload timeout**: 2 minutes
- **Port**: 5000 (configurable)

### Security Features
- Secure filename handling
- File type validation
- Size limit enforcement
- Automatic file cleanup
- Session-based security

## 📊 ATS Scoring Criteria

The application evaluates resumes based on six key criteria:

1. **Keywords (25% weight)**: Action verbs, technical skills, industry terms
2. **Sections (20% weight)**: Required sections (contact, experience, education, skills)
3. **Formatting (15% weight)**: ATS-friendly formatting, no special characters
4. **Contact Information (10% weight)**: Email and phone number presence
5. **Content Quality (20% weight)**: Word count, experience depth, skills diversity
6. **Readability (10% weight)**: Sentence structure, word complexity

### Score Ranges
- **90-100**: Excellent ATS compatibility
- **80-89**: Good ATS compatibility
- **60-79**: Fair, needs some improvements
- **0-59**: Poor, needs significant improvements

## 🛡️ API Documentation

### Upload and Analyze Resume
**Endpoint**: `POST /api/analyze`

**Request**:
```bash
curl -X POST -F "file=@resume.pdf" http://localhost:5000/api/analyze
```

**Response**:
```json
{
  "success": true,
  "filename": "resume.pdf",
  "overall_score": 75.8,
  "score_breakdown": {
    "keywords": {
      "score": 65.0,
      "weight": 0.25,
      "description": "Keyword optimization and action verbs usage"
    },
    "sections": {
      "score": 85.0,
      "weight": 0.20,
      "description": "Presence of required and optional resume sections"
    }
    // ... other criteria
  },
  "suggestions": [
    {
      "priority": "high",
      "category": "keywords",
      "title": "Add More Action Verbs",
      "description": "Use strong action verbs like 'achieved,' 'managed,' 'developed'",
      "impact": "high"
    }
    // ... more suggestions
  ],
  "resume_stats": {
    "word_count": 450,
    "sections_found": ["contact", "experience", "education"],
    "contact_info_present": true,
    "skills_found": 8,
    "experience_entries": 3,
    "education_entries": 1
  }
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Invalid file type. Please upload PDF or DOCX files only."
}
```

## 🎨 Frontend Features

### Interactive Elements
- Drag-and-drop file upload
- Real-time progress indicators
- Animated score visualization
- Responsive design for all devices
- Dark theme with Bootstrap

### Visualization Components
- Circular progress charts using Chart.js
- Color-coded score breakdown
- Priority-based suggestion grouping
- Statistics dashboard

## 🧪 Testing the Application

### Manual Testing
1. Start the application
2. Open `http://localhost:5000`
3. Upload a sample resume (PDF or DOCX)
4. Review the analysis results
5. Check suggestions for improvement

### Sample Test Files
Create test resumes with:
- Different file formats (PDF, DOCX)
- Various content quality levels
- Missing sections (to test suggestions)
- Different formatting styles

## 🔧 Troubleshooting

### Common Issues

**1. spaCy Model Not Found**
```bash
# Error: spaCy model 'en_core_web_sm' not found
# Solution:
python -m spacy download en_core_web_sm
```

**2. File Upload Issues**
- Check file size (max 16MB)
- Verify file format (PDF/DOCX only)
- Ensure proper file permissions

**3. Port Already in Use**
```bash
# Find process using port 5000
lsof -i :5000
# Kill the process
kill -9 <PID>
```

**4. Import Errors**
```bash
# Reinstall dependencies
pip install --force-reinstall flask flask-cors python-docx PyPDF2 spacy
```

### Debug Mode
Enable debug logging by setting:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance Optimization

### Recommendations
- Use Gunicorn with multiple workers in production
- Implement file caching for large documents
- Add database for user analytics (optional)
- Use CDN for static assets in production

### Scaling Considerations
- Add Redis for session management
- Implement background job processing
- Use load balancer for multiple instances
- Add monitoring and logging

## 🤝 Contributing

### Development Guidelines
1. Follow PEP 8 style guidelines
2. Add type hints for new functions
3. Include docstrings for all methods
4. Test with various resume formats
5. Update documentation for new features

### Code Style
- Use Black for code formatting
- Add comprehensive error handling
- Implement proper logging
- Follow security best practices

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the application logs
3. Test with different file formats
4. Verify all dependencies are installed

## 🔮 Future Enhancements

Potential improvements:
- Machine learning-based scoring
- Industry-specific ATS rules
- Batch processing capabilities
- Resume template recommendations
- Integration with job boards
- Multi-language support
- PDF generation for optimized resumes

---

**Built with ❤️ using Flask, spaCy, and modern web technologies**