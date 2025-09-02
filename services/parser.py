import os
import re
import logging
from typing import Dict, List, Any
import docx
import PyPDF2
import spacy

class ResumeParser:
    """
    Resume parser that extracts text and structured data from PDF and DOCX files.
    """
    
    def __init__(self):
        """Initialize the parser with spaCy NLP model."""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logging.warning("spaCy model 'en_core_web_sm' not found. Using blank model.")
            self.nlp = spacy.blank("en")
        
        # Common section headers to identify resume sections
        self.section_patterns = {
            'contact': re.compile(r'\b(contact|personal|info|information)\b', re.IGNORECASE),
            'summary': re.compile(r'\b(summary|profile|objective|about)\b', re.IGNORECASE),
            'experience': re.compile(r'\b(experience|work|employment|career|professional)\b', re.IGNORECASE),
            'education': re.compile(r'\b(education|academic|qualification|degree|university|college)\b', re.IGNORECASE),
            'skills': re.compile(r'\b(skills|competenc|technolog|technical|proficienc)\b', re.IGNORECASE),
            'projects': re.compile(r'\b(projects|portfolio|work samples)\b', re.IGNORECASE),
            'certifications': re.compile(r'\b(certification|certificate|license|accreditation)\b', re.IGNORECASE),
            'awards': re.compile(r'\b(awards|achievement|honor|recognition)\b', re.IGNORECASE)
        }
        
        # Email and phone regex patterns
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.phone_pattern = re.compile(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
        
    def parse(self, filepath: str) -> Dict[str, Any]:
        """
        Parse resume file and extract structured data.
        
        Args:
            filepath: Path to the resume file
            
        Returns:
            Dictionary containing parsed resume data
        """
        file_extension = os.path.splitext(filepath)[1].lower()
        
        if file_extension == '.pdf':
            text = self._extract_pdf_text(filepath)
        elif file_extension == '.docx':
            text = self._extract_docx_text(filepath)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
            
        if not text or len(text.strip()) < 50:
            logging.warning(f"Extracted text is too short: {len(text)} characters")
            return {}
            
        # Process text with NLP
        doc = self.nlp(text)
        
        # Extract structured information
        resume_data = {
            'text': text,
            'word_count': len(text.split()),
            'sections': self._identify_sections(text),
            'contact_info': self._extract_contact_info(text),
            'skills': self._extract_skills(doc),
            'experience': self._extract_experience(text),
            'education': self._extract_education(text),
            'entities': self._extract_entities(doc)
        }
        
        return resume_data
    
    def _extract_pdf_text(self, filepath: str) -> str:
        """Extract text from PDF file."""
        try:
            text = ""
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            logging.error(f"Error extracting PDF text: {str(e)}")
            return ""
    
    def _extract_docx_text(self, filepath: str) -> str:
        """Extract text from DOCX file."""
        try:
            doc = docx.Document(filepath)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            logging.error(f"Error extracting DOCX text: {str(e)}")
            return ""
    
    def _identify_sections(self, text: str) -> Dict[str, List[str]]:
        """Identify different sections in the resume text."""
        sections = {}
        lines = text.split('\n')
        current_section = None
        section_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line is a section header
            section_found = False
            for section_name, pattern in self.section_patterns.items():
                if pattern.search(line) and len(line) < 50:  # Section headers are usually short
                    # Save previous section
                    if current_section and section_content:
                        sections[current_section] = section_content
                    
                    # Start new section
                    current_section = section_name
                    section_content = []
                    section_found = True
                    break
            
            if not section_found and current_section:
                section_content.append(line)
        
        # Add the last section
        if current_section and section_content:
            sections[current_section] = section_content
            
        return sections
    
    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information from resume text."""
        contact_info = {}
        
        # Extract email
        email_match = self.email_pattern.search(text)
        if email_match:
            contact_info['email'] = email_match.group()
        
        # Extract phone number
        phone_match = self.phone_pattern.search(text)
        if phone_match:
            contact_info['phone'] = phone_match.group()
            
        return contact_info
    
    def _extract_skills(self, doc) -> List[str]:
        """Extract skills from the resume using NLP."""
        skills = []
        
        # Common technical skills patterns
        skill_patterns = [
            re.compile(r'\b(Python|Java|JavaScript|C\+\+|C#|PHP|Ruby|Swift|Kotlin|Go|Rust)\b', re.IGNORECASE),
            re.compile(r'\b(React|Angular|Vue|Node\.js|Express|Django|Flask|Spring|Laravel)\b', re.IGNORECASE),
            re.compile(r'\b(HTML|CSS|SCSS|SQL|MongoDB|PostgreSQL|MySQL|Redis|Docker|Kubernetes)\b', re.IGNORECASE),
            re.compile(r'\b(AWS|Azure|GCP|Git|Jenkins|CI/CD|DevOps|Agile|Scrum)\b', re.IGNORECASE),
            re.compile(r'\b(Machine Learning|AI|Data Science|Analytics|Tableau|Power BI)\b', re.IGNORECASE)
        ]
        
        text = doc.text
        for pattern in skill_patterns:
            matches = pattern.findall(text)
            skills.extend(matches)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_skills = []
        for skill in skills:
            if skill.lower() not in seen:
                seen.add(skill.lower())
                unique_skills.append(skill)
        
        return unique_skills
    
    def _extract_experience(self, text: str) -> List[Dict[str, str]]:
        """Extract work experience entries."""
        experience = []
        
        # Look for date patterns that indicate work periods
        date_pattern = re.compile(r'\b(20\d{2}|19\d{2})\b.*(?:present|current|\d{4})', re.IGNORECASE)
        date_matches = date_pattern.findall(text)
        
        # Simple heuristic: count potential experience entries
        for match in date_matches[:5]:  # Limit to 5 entries
            experience.append({
                'period': match,
                'details': 'Work experience entry found'
            })
        
        return experience
    
    def _extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education entries."""
        education = []
        
        # Look for degree patterns
        degree_patterns = [
            re.compile(r'\b(bachelor|master|phd|doctorate|associate|diploma)\b.*\b(degree|of)\b', re.IGNORECASE),
            re.compile(r'\b(bs|ba|ms|ma|mba|phd|bsc|msc)\b', re.IGNORECASE),
            re.compile(r'\b(university|college|institute|school)\b.*\b(20\d{2}|19\d{2})\b', re.IGNORECASE)
        ]
        
        for pattern in degree_patterns:
            matches = pattern.findall(text)
            for match in matches[:3]:  # Limit to 3 entries
                education.append({
                    'degree': str(match),
                    'details': 'Education entry found'
                })
        
        return education
    
    def _extract_entities(self, doc) -> Dict[str, List[str]]:
        """Extract named entities from the text."""
        entities = {
            'organizations': [],
            'persons': [],
            'locations': [],
            'dates': []
        }
        
        for ent in doc.ents:
            if ent.label_ == "ORG":
                entities['organizations'].append(ent.text)
            elif ent.label_ == "PERSON":
                entities['persons'].append(ent.text)
            elif ent.label_ in ["GPE", "LOC"]:
                entities['locations'].append(ent.text)
            elif ent.label_ == "DATE":
                entities['dates'].append(ent.text)
        
        return entities
