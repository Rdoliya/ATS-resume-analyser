# Resume ATS Scorer

## Overview

The Resume ATS Scorer is a Flask-based web application that analyzes uploaded resumes for Applicant Tracking System (ATS) compatibility. It parses PDF and DOCX resume files, extracts structured data, calculates ATS scores based on multiple criteria, and provides actionable suggestions for improvement. The application helps job seekers optimize their resumes to better pass through automated screening systems used by employers.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Single-page application** using vanilla JavaScript with Bootstrap for responsive UI
- **File upload interface** with client-side validation for file type (.pdf, .docx) and size (16MB limit)
- **Real-time results visualization** with score circles, progress bars, and suggestion lists
- **CORS-enabled API communication** for seamless frontend-backend interaction

### Backend Architecture
- **Flask web framework** as the core application server
- **Modular service architecture** with three main components:
  - **ResumeParser**: Handles text extraction from PDF/DOCX files using PyPDF2 and python-docx
  - **ATSScorer**: Evaluates resumes based on keywords, formatting, and section completeness
  - **SuggestionEngine**: Generates prioritized improvement recommendations
- **RESTful API design** with `/api/analyze` endpoint for resume processing
- **File upload handling** with secure filename processing and temporary storage

### Data Processing Pipeline
- **Text extraction** from uploaded documents with fallback handling for different file formats
- **NLP processing** using spaCy for entity recognition and text analysis
- **Pattern matching** with regex for contact information, sections, and ATS-friendly elements
- **Scoring algorithm** that weighs multiple factors: keywords, formatting, section presence, and content quality

### Authentication & Security
- **Session-based security** with configurable secret keys
- **File validation** to prevent malicious uploads
- **Secure filename handling** using Werkzeug utilities
- **CORS configuration** for controlled cross-origin requests

## External Dependencies

### Core Frameworks
- **Flask**: Web application framework with CORS support
- **Bootstrap 5**: Frontend CSS framework with dark theme variant
- **Font Awesome**: Icon library for UI elements

### Document Processing
- **PyPDF2**: PDF text extraction and parsing
- **python-docx**: Microsoft Word document processing
- **spaCy**: Natural language processing and entity recognition (en_core_web_sm model)

### Development Tools
- **Werkzeug**: WSGI utilities for secure file handling
- **Python logging**: Application monitoring and debugging

### Static Assets
- **Bootstrap CSS**: Delivered via CDN for responsive design
- **Font Awesome**: Icon fonts delivered via CDN
- **Custom CSS/JS**: Local assets for application-specific styling and functionality

The application is designed to run locally with all processing handled server-side, ensuring privacy of uploaded resume data while providing comprehensive ATS analysis and improvement suggestions.