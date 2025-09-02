import re
import logging
from typing import Dict, List, Any
from collections import Counter

class ATSScorer:
    """
    ATS (Applicant Tracking System) scorer that evaluates resumes based on
    multiple criteria and provides detailed scoring breakdown.
    """
    
    def __init__(self):
        """Initialize the ATS scorer with evaluation criteria."""
        
        # Common ATS-friendly keywords by category
        self.ats_keywords = {
            'action_verbs': [
                'achieved', 'managed', 'led', 'developed', 'implemented', 'created',
                'improved', 'optimized', 'designed', 'built', 'delivered', 'coordinated',
                'analyzed', 'solved', 'increased', 'reduced', 'streamlined', 'executed',
                'collaborated', 'initiated', 'maintained', 'automated', 'enhanced'
            ],
            'technical_skills': [
                'python', 'java', 'javascript', 'sql', 'html', 'css', 'react', 'angular',
                'node.js', 'aws', 'docker', 'kubernetes', 'git', 'agile', 'scrum',
                'machine learning', 'data analysis', 'project management', 'api'
            ],
            'soft_skills': [
                'leadership', 'communication', 'teamwork', 'problem solving',
                'analytical', 'creative', 'detail oriented', 'time management',
                'adaptability', 'collaboration', 'critical thinking'
            ]
        }
        
        # Required sections for a complete resume
        self.required_sections = [
            'contact', 'experience', 'education', 'skills'
        ]
        
        # Optional but valuable sections
        self.optional_sections = [
            'summary', 'projects', 'certifications', 'awards'
        ]
        
        # ATS-unfriendly elements
        self.formatting_issues = {
            'special_chars': re.compile(r'[^\w\s\-\.\@\(\)\+\/\,\:\;\'\"]'),
            'excessive_formatting': re.compile(r'[\*\#\&\%\$]{2,}'),
            'tables_columns': re.compile(r'\|\s*\||\t{2,}'),
            'graphics_symbols': re.compile(r'[★☆♦◆■□●○▪▫]')
        }
    
    def calculate_score(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive ATS score for the resume.
        
        Args:
            resume_data: Parsed resume data
            
        Returns:
            Dictionary containing overall score and detailed breakdown
        """
        if not resume_data or not resume_data.get('text'):
            return {'overall_score': 0, 'breakdown': {}}
        
        text = resume_data['text']
        sections = resume_data.get('sections', {})
        
        # Calculate individual scores
        keyword_score = self._score_keywords(text)
        section_score = self._score_sections(sections)
        formatting_score = self._score_formatting(text)
        contact_score = self._score_contact_info(resume_data.get('contact_info', {}))
        content_quality_score = self._score_content_quality(text, resume_data)
        readability_score = self._score_readability(text)
        
        # Weight the scores (totaling 100%)
        weights = {
            'keywords': 0.25,      # 25% - Keyword optimization
            'sections': 0.20,      # 20% - Section completeness
            'formatting': 0.15,    # 15% - ATS-friendly formatting
            'contact': 0.10,       # 10% - Contact information
            'content_quality': 0.20, # 20% - Content quality and depth
            'readability': 0.10    # 10% - Text readability
        }
        
        scores = {
            'keywords': keyword_score,
            'sections': section_score,
            'formatting': formatting_score,
            'contact': contact_score,
            'content_quality': content_quality_score,
            'readability': readability_score
        }
        
        # Calculate weighted overall score
        overall_score = sum(scores[category] * weights[category] for category in scores)
        overall_score = round(overall_score, 1)
        
        return {
            'overall_score': overall_score,
            'breakdown': {
                'keywords': {
                    'score': keyword_score,
                    'weight': weights['keywords'],
                    'description': 'Keyword optimization and action verbs usage'
                },
                'sections': {
                    'score': section_score,
                    'weight': weights['sections'],
                    'description': 'Presence of required and optional resume sections'
                },
                'formatting': {
                    'score': formatting_score,
                    'weight': weights['formatting'],
                    'description': 'ATS-friendly formatting and structure'
                },
                'contact': {
                    'score': contact_score,
                    'weight': weights['contact'],
                    'description': 'Contact information completeness'
                },
                'content_quality': {
                    'score': content_quality_score,
                    'weight': weights['content_quality'],
                    'description': 'Content depth and professional experience'
                },
                'readability': {
                    'score': readability_score,
                    'weight': weights['readability'],
                    'description': 'Text readability and clarity'
                }
            }
        }
    
    def _score_keywords(self, text: str) -> float:
        """Score based on presence of ATS-friendly keywords."""
        text_lower = text.lower()
        total_keywords = 0
        found_keywords = 0
        
        for category, keywords in self.ats_keywords.items():
            total_keywords += len(keywords)
            for keyword in keywords:
                if keyword in text_lower:
                    found_keywords += 1
        
        # Calculate keyword density
        words = len(text.split())
        keyword_density = found_keywords / max(words / 100, 1)  # Keywords per 100 words
        
        # Score based on keyword presence and density
        presence_score = (found_keywords / total_keywords) * 70  # Up to 70 points for presence
        density_score = min(keyword_density * 10, 30)  # Up to 30 points for density
        
        return min(presence_score + density_score, 100)
    
    def _score_sections(self, sections: Dict[str, List[str]]) -> float:
        """Score based on presence of required and optional sections."""
        section_keys = set(sections.keys())
        
        # Check required sections
        required_found = len(section_keys.intersection(self.required_sections))
        required_score = (required_found / len(self.required_sections)) * 70
        
        # Check optional sections
        optional_found = len(section_keys.intersection(self.optional_sections))
        optional_score = (optional_found / len(self.optional_sections)) * 30
        
        return min(required_score + optional_score, 100)
    
    def _score_formatting(self, text: str) -> float:
        """Score based on ATS-friendly formatting."""
        issues_count = 0
        total_checks = len(self.formatting_issues)
        
        for issue_name, pattern in self.formatting_issues.items():
            matches = len(pattern.findall(text))
            if matches > 5:  # Allow some instances but penalize excessive use
                issues_count += 1
        
        # Check for other formatting issues
        lines = text.split('\n')
        
        # Too many blank lines
        blank_lines = sum(1 for line in lines if not line.strip())
        if blank_lines > len(lines) * 0.3:  # More than 30% blank lines
            issues_count += 1
        
        # Lines that are too long (may indicate formatting issues)
        long_lines = sum(1 for line in lines if len(line) > 120)
        if long_lines > len(lines) * 0.2:  # More than 20% very long lines
            issues_count += 1
        
        # Calculate score (fewer issues = higher score)
        max_possible_issues = total_checks + 2  # Additional checks above
        score = ((max_possible_issues - issues_count) / max_possible_issues) * 100
        
        return max(score, 0)
    
    def _score_contact_info(self, contact_info: Dict[str, str]) -> float:
        """Score based on completeness of contact information."""
        required_fields = ['email']  # Email is essential
        optional_fields = ['phone']  # Phone is good to have
        
        score = 0
        
        # Required fields
        for field in required_fields:
            if field in contact_info and contact_info[field]:
                score += 70  # 70 points for email
        
        # Optional fields
        for field in optional_fields:
            if field in contact_info and contact_info[field]:
                score += 30  # 30 points for phone
        
        return min(score, 100)
    
    def _score_content_quality(self, text: str, resume_data: Dict[str, Any]) -> float:
        """Score based on content quality and depth."""
        word_count = len(text.split())
        experience_entries = len(resume_data.get('experience', []))
        skills_count = len(resume_data.get('skills', []))
        
        # Word count score (optimal range: 300-800 words)
        if 300 <= word_count <= 800:
            word_score = 40
        elif 200 <= word_count < 300 or 800 < word_count <= 1000:
            word_score = 30
        elif word_count < 200:
            word_score = 10
        else:
            word_score = 20
        
        # Experience depth score
        experience_score = min(experience_entries * 15, 35)  # Up to 35 points
        
        # Skills diversity score
        skills_score = min(skills_count * 2, 25)  # Up to 25 points
        
        return word_score + experience_score + skills_score
    
    def _score_readability(self, text: str) -> float:
        """Score based on text readability and clarity."""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 0
        
        # Calculate average sentence length
        words = text.split()
        avg_sentence_length = len(words) / len(sentences)
        
        # Calculate average word length
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        
        # Ideal ranges for professional writing
        sentence_score = 50
        if 10 <= avg_sentence_length <= 20:  # Ideal sentence length
            sentence_score = 50
        elif avg_sentence_length < 5 or avg_sentence_length > 30:
            sentence_score = 20
        else:
            sentence_score = 35
        
        word_score = 50
        if 4 <= avg_word_length <= 6:  # Ideal word length
            word_score = 50
        elif avg_word_length < 3 or avg_word_length > 8:
            word_score = 20
        else:
            word_score = 35
        
        return sentence_score + word_score
