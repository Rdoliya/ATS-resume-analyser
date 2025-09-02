import re
from typing import Dict, List, Any

class SuggestionEngine:
    """
    Generates actionable suggestions to improve ATS scores based on resume analysis.
    """
    
    def __init__(self):
        """Initialize the suggestion engine with improvement templates."""
        
        # High-impact keywords that should be present
        self.important_keywords = {
            'general': [
                'achieved', 'managed', 'led', 'developed', 'implemented',
                'improved', 'optimized', 'designed', 'delivered', 'increased'
            ],
            'technical': [
                'python', 'java', 'javascript', 'sql', 'aws', 'docker',
                'git', 'agile', 'api', 'database', 'framework'
            ],
            'leadership': [
                'leadership', 'team', 'project management', 'coordination',
                'mentoring', 'training', 'strategic planning'
            ]
        }
        
        # Section improvement templates
        self.section_templates = {
            'summary': 'Add a professional summary at the top highlighting your key qualifications and career objectives.',
            'skills': 'Include a dedicated skills section with relevant technical and soft skills.',
            'projects': 'Add a projects section to showcase your practical experience and achievements.',
            'certifications': 'Include any relevant certifications or professional credentials.',
            'awards': 'Mention any awards, recognitions, or achievements to stand out.'
        }
    
    def generate_suggestions(self, resume_data: Dict[str, Any], score_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate prioritized suggestions based on resume analysis and scores.
        
        Args:
            resume_data: Parsed resume data
            score_data: ATS scoring results
            
        Returns:
            List of suggestion dictionaries with priority, category, and description
        """
        suggestions = []
        
        if not resume_data or not score_data:
            return suggestions
        
        breakdown = score_data.get('breakdown', {})
        overall_score = score_data.get('overall_score', 0)
        
        # Generate suggestions based on score breakdown
        suggestions.extend(self._suggest_keyword_improvements(resume_data, breakdown.get('keywords', {})))
        suggestions.extend(self._suggest_section_improvements(resume_data, breakdown.get('sections', {})))
        suggestions.extend(self._suggest_formatting_improvements(resume_data, breakdown.get('formatting', {})))
        suggestions.extend(self._suggest_contact_improvements(resume_data, breakdown.get('contact', {})))
        suggestions.extend(self._suggest_content_improvements(resume_data, breakdown.get('content_quality', {})))
        suggestions.extend(self._suggest_readability_improvements(resume_data, breakdown.get('readability', {})))
        
        # Add general suggestions based on overall score
        if overall_score < 60:
            suggestions.append({
                'priority': 'high',
                'category': 'general',
                'title': 'Overall Resume Optimization',
                'description': 'Your resume needs significant improvements to be ATS-friendly. Focus on the high-priority suggestions first.',
                'impact': 'high'
            })
        elif overall_score < 80:
            suggestions.append({
                'priority': 'medium',
                'category': 'general',
                'title': 'Fine-tuning Required',
                'description': 'Your resume is good but has room for improvement. Address the medium-priority suggestions to boost your score.',
                'impact': 'medium'
            })
        
        # Sort suggestions by priority and impact
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        impact_order = {'high': 3, 'medium': 2, 'low': 1}
        
        suggestions.sort(key=lambda x: (
            priority_order.get(x['priority'], 0),
            impact_order.get(x['impact'], 0)
        ), reverse=True)
        
        return suggestions[:15]  # Limit to top 15 suggestions
    
    def _suggest_keyword_improvements(self, resume_data: Dict[str, Any], keyword_score: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate keyword-related improvement suggestions."""
        suggestions = []
        score = keyword_score.get('score', 0)
        text = resume_data.get('text', '').lower()
        
        if score < 50:
            suggestions.append({
                'priority': 'high',
                'category': 'keywords',
                'title': 'Add More Action Verbs',
                'description': 'Use strong action verbs like "achieved," "managed," "developed," and "implemented" to describe your accomplishments.',
                'impact': 'high'
            })
        
        if score < 70:
            # Check for missing important keywords
            missing_keywords = []
            for category, keywords in self.important_keywords.items():
                category_missing = [kw for kw in keywords[:5] if kw not in text]  # Check top 5 per category
                missing_keywords.extend(category_missing[:2])  # Add top 2 missing per category
            
            if missing_keywords:
                suggestions.append({
                    'priority': 'medium',
                    'category': 'keywords',
                    'title': 'Include Relevant Keywords',
                    'description': f'Consider adding these relevant keywords: {", ".join(missing_keywords[:5])}. Use them naturally in your experience descriptions.',
                    'impact': 'medium'
                })
        
        # Check for quantifiable achievements
        numbers_pattern = re.compile(r'\d+%|\$\d+|\d+\+|\d+x|increased.*\d+|reduced.*\d+|improved.*\d+')
        if len(numbers_pattern.findall(resume_data.get('text', ''))) < 3:
            suggestions.append({
                'priority': 'high',
                'category': 'keywords',
                'title': 'Add Quantifiable Achievements',
                'description': 'Include specific numbers, percentages, or metrics to demonstrate your impact (e.g., "Increased sales by 25%" or "Managed team of 10 people").',
                'impact': 'high'
            })
        
        return suggestions
    
    def _suggest_section_improvements(self, resume_data: Dict[str, Any], section_score: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate section-related improvement suggestions."""
        suggestions = []
        score = section_score.get('score', 0)
        sections = resume_data.get('sections', {})
        
        # Check for missing required sections
        required_sections = ['contact', 'experience', 'education', 'skills']
        missing_required = [sec for sec in required_sections if sec not in sections]
        
        for section in missing_required:
            priority = 'high' if section in ['experience', 'skills'] else 'medium'
            suggestions.append({
                'priority': priority,
                'category': 'sections',
                'title': f'Add {section.title()} Section',
                'description': f'Include a dedicated {section} section. This is essential for ATS systems to categorize your information properly.',
                'impact': 'high'
            })
        
        # Suggest optional sections that could improve the resume
        if score < 80:
            optional_sections = ['summary', 'projects', 'certifications']
            for section in optional_sections:
                if section not in sections:
                    suggestions.append({
                        'priority': 'medium',
                        'category': 'sections',
                        'title': f'Consider Adding {section.title()} Section',
                        'description': self.section_templates.get(section, f'Adding a {section} section could strengthen your resume.'),
                        'impact': 'medium'
                    })
                    break  # Only suggest one optional section at a time
        
        return suggestions
    
    def _suggest_formatting_improvements(self, resume_data: Dict[str, Any], formatting_score: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate formatting-related improvement suggestions."""
        suggestions = []
        score = formatting_score.get('score', 0)
        text = resume_data.get('text', '')
        
        if score < 70:
            suggestions.append({
                'priority': 'high',
                'category': 'formatting',
                'title': 'Improve ATS Compatibility',
                'description': 'Use simple formatting without tables, columns, or special characters. Stick to standard fonts and clear section headers.',
                'impact': 'high'
            })
        
        # Check for specific formatting issues
        if re.search(r'[★☆♦◆■□●○▪▫]', text):
            suggestions.append({
                'priority': 'medium',
                'category': 'formatting',
                'title': 'Remove Special Symbols',
                'description': 'Replace bullet points with standard dashes (-) or asterisks (*). Avoid special symbols that ATS systems cannot read.',
                'impact': 'medium'
            })
        
        # Check for excessive blank lines
        lines = text.split('\n')
        blank_lines = sum(1 for line in lines if not line.strip())
        if blank_lines > len(lines) * 0.3:
            suggestions.append({
                'priority': 'low',
                'category': 'formatting',
                'title': 'Reduce White Space',
                'description': 'Remove excessive blank lines to make your resume more compact and easier for ATS systems to parse.',
                'impact': 'low'
            })
        
        return suggestions
    
    def _suggest_contact_improvements(self, resume_data: Dict[str, Any], contact_score: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate contact information improvement suggestions."""
        suggestions = []
        score = contact_score.get('score', 0)
        contact_info = resume_data.get('contact_info', {})
        
        if score < 70:
            if not contact_info.get('email'):
                suggestions.append({
                    'priority': 'high',
                    'category': 'contact',
                    'title': 'Add Email Address',
                    'description': 'Include a professional email address at the top of your resume. This is essential for recruiters to contact you.',
                    'impact': 'high'
                })
            
            if not contact_info.get('phone'):
                suggestions.append({
                    'priority': 'medium',
                    'category': 'contact',
                    'title': 'Add Phone Number',
                    'description': 'Include your phone number for additional contact options. Use a standard format like (555) 123-4567.',
                    'impact': 'medium'
                })
        
        return suggestions
    
    def _suggest_content_improvements(self, resume_data: Dict[str, Any], content_score: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate content quality improvement suggestions."""
        suggestions = []
        score = content_score.get('score', 0)
        word_count = resume_data.get('word_count', 0)
        experience_count = len(resume_data.get('experience', []))
        skills_count = len(resume_data.get('skills', []))
        
        if word_count < 300:
            suggestions.append({
                'priority': 'high',
                'category': 'content',
                'title': 'Expand Resume Content',
                'description': 'Your resume is too brief. Add more details about your experience, achievements, and skills. Aim for 300-800 words total.',
                'impact': 'high'
            })
        elif word_count > 1000:
            suggestions.append({
                'priority': 'medium',
                'category': 'content',
                'title': 'Reduce Resume Length',
                'description': 'Your resume may be too long. Focus on the most relevant and impactful information. Keep it concise and under 2 pages.',
                'impact': 'medium'
            })
        
        if experience_count < 2:
            suggestions.append({
                'priority': 'high',
                'category': 'content',
                'title': 'Add More Experience Details',
                'description': 'Include more detailed work experience entries with specific accomplishments and responsibilities for each role.',
                'impact': 'high'
            })
        
        if skills_count < 5:
            suggestions.append({
                'priority': 'medium',
                'category': 'content',
                'title': 'Expand Skills Section',
                'description': 'Add more relevant skills including both technical and soft skills. Include tools, programming languages, and methodologies you\'ve used.',
                'impact': 'medium'
            })
        
        return suggestions
    
    def _suggest_readability_improvements(self, resume_data: Dict[str, Any], readability_score: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate readability improvement suggestions."""
        suggestions = []
        score = readability_score.get('score', 0)
        text = resume_data.get('text', '')
        
        if score < 60:
            suggestions.append({
                'priority': 'medium',
                'category': 'readability',
                'title': 'Improve Text Clarity',
                'description': 'Use clear, concise sentences. Avoid overly complex words or very long sentences that may be difficult for ATS systems to parse.',
                'impact': 'medium'
            })
        
        # Check sentence structure
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if sentences:
            words = text.split()
            avg_sentence_length = len(words) / len(sentences)
            
            if avg_sentence_length > 25:
                suggestions.append({
                    'priority': 'low',
                    'category': 'readability',
                    'title': 'Shorten Sentences',
                    'description': 'Break down long sentences into shorter, more digestible ones. Aim for 10-20 words per sentence on average.',
                    'impact': 'low'
                })
            elif avg_sentence_length < 8:
                suggestions.append({
                    'priority': 'low',
                    'category': 'readability',
                    'title': 'Combine Short Sentences',
                    'description': 'Some sentences are too short. Consider combining related short sentences for better flow and readability.',
                    'impact': 'low'
                })
        
        return suggestions
