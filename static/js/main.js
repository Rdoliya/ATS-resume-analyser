/**
 * Resume ATS Scorer - Frontend JavaScript
 * Handles file upload, API communication, and results visualization
 */

class ResumeATSScorer {
    constructor() {
        this.scoreChart = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.setupFormValidation();
    }

    bindEvents() {
        const uploadForm = document.getElementById('upload-form');
        const fileInput = document.getElementById('resume-file');

        uploadForm.addEventListener('submit', (e) => this.handleFormSubmit(e));
        fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
    }

    setupFormValidation() {
        const fileInput = document.getElementById('resume-file');
        
        fileInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                // Validate file size (16MB = 16 * 1024 * 1024 bytes)
                if (file.size > 16 * 1024 * 1024) {
                    this.value = '';
                    alert('File size must be less than 16MB');
                    return;
                }

                // Validate file type
                const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
                if (!allowedTypes.includes(file.type)) {
                    this.value = '';
                    alert('Please upload only PDF or DOCX files');
                    return;
                }
            }
        });
    }

    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            // Visual feedback for file selection
            const fileName = file.name;
            const fileSize = this.formatFileSize(file.size);
            console.log(`Selected file: ${fileName} (${fileSize})`);
        }
    }

    async handleFormSubmit(event) {
        event.preventDefault();
        
        const fileInput = document.getElementById('resume-file');
        const file = fileInput.files[0];
        
        if (!file) {
            this.showError('Please select a file to upload');
            return;
        }

        try {
            this.showLoading();
            const result = await this.uploadAndAnalyze(file);
            
            if (result.success) {
                this.displayResults(result);
            } else {
                this.showError(result.error || 'An error occurred while analyzing your resume');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showError('Network error. Please check your connection and try again.');
        } finally {
            this.hideLoading();
        }
    }

    async uploadAndAnalyze(file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            if (response.status === 413) {
                throw new Error('File too large. Maximum size is 16MB.');
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    showLoading() {
        document.getElementById('loading-section').style.display = 'block';
        document.getElementById('results-section').style.display = 'none';
        document.getElementById('error-section').style.display = 'none';
        
        const analyzeBtn = document.getElementById('analyze-btn');
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...';
    }

    hideLoading() {
        document.getElementById('loading-section').style.display = 'none';
        
        const analyzeBtn = document.getElementById('analyze-btn');
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = '<i class="fas fa-chart-line me-2"></i>Analyze Resume';
    }

    showError(message) {
        document.getElementById('error-message').textContent = message;
        document.getElementById('error-section').style.display = 'block';
        document.getElementById('results-section').style.display = 'none';
    }

    displayResults(data) {
        document.getElementById('results-section').style.display = 'block';
        document.getElementById('error-section').style.display = 'none';
        
        // Display overall score
        this.displayOverallScore(data.overall_score);
        
        // Display score breakdown
        this.displayScoreBreakdown(data.score_breakdown);
        
        // Display resume statistics
        this.displayResumeStats(data.resume_stats);
        
        // Display suggestions
        this.displaySuggestions(data.suggestions);

        // Scroll to results
        document.getElementById('results-section').scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }

    displayOverallScore(score) {
        const scoreElement = document.getElementById('overall-score');
        const descriptionElement = document.getElementById('score-description');
        
        // Animate score counting
        this.animateScore(scoreElement, 0, score, 1500);
        
        // Set description based on score
        let description, color;
        if (score >= 90) {
            description = "Excellent! Your resume is highly ATS-friendly.";
            color = '#198754';
        } else if (score >= 80) {
            description = "Good! Your resume has strong ATS compatibility.";
            color = '#0dcaf0';
        } else if (score >= 60) {
            description = "Fair. Your resume needs some improvements for better ATS compatibility.";
            color = '#ffc107';
        } else {
            description = "Poor. Your resume needs significant improvements for ATS systems.";
            color = '#dc3545';
        }
        
        descriptionElement.textContent = description;
        scoreElement.style.color = color;
        
        // Create circular progress chart
        this.createScoreChart(score);
    }

    createScoreChart(score) {
        const ctx = document.getElementById('score-chart').getContext('2d');
        
        // Destroy existing chart if it exists
        if (this.scoreChart) {
            this.scoreChart.destroy();
        }
        
        const color = score >= 90 ? '#198754' : 
                     score >= 80 ? '#0dcaf0' : 
                     score >= 60 ? '#ffc107' : '#dc3545';
        
        this.scoreChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [score, 100 - score],
                    backgroundColor: [color, '#e9ecef'],
                    borderWidth: 0,
                    cutout: '80%'
                }]
            },
            options: {
                responsive: false,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        enabled: false
                    }
                }
            }
        });
    }

    displayScoreBreakdown(breakdown) {
        const container = document.getElementById('score-breakdown');
        container.innerHTML = '';
        
        Object.entries(breakdown).forEach(([category, data]) => {
            const score = data.score;
            const weight = Math.round(data.weight * 100);
            const description = data.description;
            
            const progressColor = score >= 80 ? 'bg-success' : 
                                score >= 60 ? 'bg-info' : 
                                score >= 40 ? 'bg-warning' : 'bg-danger';
            
            const scoreItem = document.createElement('div');
            scoreItem.className = 'score-item';
            scoreItem.innerHTML = `
                <div class="score-label">
                    <span class="fw-semibold">${this.formatCategoryName(category)}</span>
                    <span class="score-value">${score.toFixed(1)}/100 (${weight}%)</span>
                </div>
                <div class="progress" style="height: 10px;">
                    <div class="progress-bar ${progressColor}" 
                         role="progressbar" 
                         style="width: ${score}%"
                         aria-valuenow="${score}" 
                         aria-valuemin="0" 
                         aria-valuemax="100">
                    </div>
                </div>
                <small class="text-muted">${description}</small>
            `;
            
            container.appendChild(scoreItem);
        });
    }

    displayResumeStats(stats) {
        const container = document.getElementById('resume-stats');
        
        const statsHtml = `
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value">${stats.word_count}</div>
                    <div class="stat-label">Words</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${stats.sections_found.length}</div>
                    <div class="stat-label">Sections</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${stats.skills_found}</div>
                    <div class="stat-label">Skills Found</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${stats.experience_entries}</div>
                    <div class="stat-label">Experience Entries</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${stats.education_entries}</div>
                    <div class="stat-label">Education Entries</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${stats.contact_info_present ? 'Yes' : 'No'}</div>
                    <div class="stat-label">Contact Info</div>
                </div>
            </div>
            <div class="mt-3">
                <h6>Sections Found:</h6>
                <p class="text-muted mb-0">
                    ${stats.sections_found.length > 0 ? 
                        stats.sections_found.map(section => this.formatCategoryName(section)).join(', ') : 
                        'No clear sections identified'}
                </p>
            </div>
        `;
        
        container.innerHTML = statsHtml;
    }

    displaySuggestions(suggestions) {
        const container = document.getElementById('suggestions-list');
        
        if (!suggestions || suggestions.length === 0) {
            container.innerHTML = '<p class="text-muted">No specific suggestions available. Your resume looks good!</p>';
            return;
        }
        
        // Group suggestions by priority
        const groupedSuggestions = {
            high: suggestions.filter(s => s.priority === 'high'),
            medium: suggestions.filter(s => s.priority === 'medium'),
            low: suggestions.filter(s => s.priority === 'low')
        };
        
        let html = '';
        
        Object.entries(groupedSuggestions).forEach(([priority, prioritySuggestions]) => {
            if (prioritySuggestions.length === 0) return;
            
            html += `
                <div class="mb-4">
                    <h5 class="mb-3">
                        <span class="badge priority-badge-${priority} me-2">${priority.toUpperCase()} PRIORITY</span>
                        (${prioritySuggestions.length} suggestion${prioritySuggestions.length > 1 ? 's' : ''})
                    </h5>
                    <div class="suggestions-container">
            `;
            
            prioritySuggestions.forEach((suggestion, index) => {
                html += `
                    <div class="card suggestion-card suggestion-${priority} mb-3">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <h6 class="card-title mb-0">${suggestion.title}</h6>
                                <span class="badge bg-secondary text-capitalize">${suggestion.category}</span>
                            </div>
                            <p class="card-text text-muted mb-0">${suggestion.description}</p>
                        </div>
                    </div>
                `;
            });
            
            html += '</div></div>';
        });
        
        container.innerHTML = html;
    }

    animateScore(element, start, end, duration) {
        const startTime = performance.now();
        
        const updateScore = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function for smooth animation
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const currentScore = start + (end - start) * easeOutQuart;
            
            element.textContent = Math.round(currentScore);
            
            if (progress < 1) {
                requestAnimationFrame(updateScore);
            }
        };
        
        requestAnimationFrame(updateScore);
    }

    formatCategoryName(category) {
        return category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ResumeATSScorer();
});
