// Global utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        ${message}
        <span class="notification-close">&times;</span>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
    
    // Close button handler
    notification.querySelector('.notification-close').onclick = () => {
        notification.style.opacity = '0';
        setTimeout(() => notification.remove(), 300);
    };
}

// API helper functions
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(endpoint, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'API call failed');
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call error:', error);
        throw error;
    }
}

// Student management
class StudentManager {
    constructor() {
        this.currentStudentId = localStorage.getItem('currentStudentId');
    }
    
    setCurrentStudent(studentId) {
        this.currentStudentId = studentId;
        localStorage.setItem('currentStudentId', studentId);
    }
    
    getCurrentStudentId() {
        return this.currentStudentId;
    }
    
    async createStudent(studentData) {
        const data = await apiCall('/api/students', {
            method: 'POST',
            body: JSON.stringify(studentData)
        });
        this.setCurrentStudent(data.id);
        return data;
    }
    
    async getStudent(studentId = null) {
        const id = studentId || this.currentStudentId;
        if (!id) throw new Error('No student ID available');
        return await apiCall(`/api/students/${id}`);
    }
    
    async addSkill(skillData, studentId = null) {
        const id = studentId || this.currentStudentId;
        if (!id) throw new Error('No student ID available');
        return await apiCall(`/api/students/${id}/skills`, {
            method: 'POST',
            body: JSON.stringify(skillData)
        });
    }
    
    async addInterest(interestData, studentId = null) {
        const id = studentId || this.currentStudentId;
        if (!id) throw new Error('No student ID available');
        return await apiCall(`/api/students/${id}/interests`, {
            method: 'POST',
            body: JSON.stringify(interestData)
        });
    }
    
    async getRecommendations(studentId = null) {
        const id = studentId || this.currentStudentId;
        if (!id) throw new Error('No student ID available');
        return await apiCall(`/api/students/${id}/recommendations`);
    }
    
    async getRoadmap(studentId = null) {
        const id = studentId || this.currentStudentId;
        if (!id) throw new Error('No student ID available');
        return await apiCall(`/api/students/${id}/roadmap`);
    }
    
    async getProgress(studentId = null) {
        const id = studentId || this.currentStudentId;
        if (!id) throw new Error('No student ID available');
        return await apiCall(`/api/students/${id}/progress`);
    }
    
    async updateProgress(progressData, studentId = null) {
        const id = studentId || this.currentStudentId;
        if (!id) throw new Error('No student ID available');
        return await apiCall(`/api/students/${id}/progress`, {
            method: 'POST',
            body: JSON.stringify(progressData)
        });
    }
}

// Initialize global student manager
const studentManager = new StudentManager();

// Chart utilities
function createProgressChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => item.label),
            datasets: [{
                label: options.label || 'Progress',
                data: data.map(item => item.value),
                backgroundColor: options.backgroundColor || '#4CAF50',
                borderColor: options.borderColor || '#45a049',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: options.showLegend || false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: options.maxValue || 100
                }
            },
            ...options.chartOptions
        }
    });
}

function createDoughnutChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.map(item => item.label),
            datasets: [{
                data: data.map(item => item.value),
                backgroundColor: options.colors || [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4CAF50', '#FF9800'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: options.legendPosition || 'top'
                }
            },
            ...options.chartOptions
        }
    });
}

// Form utilities
function validateForm(formElement) {
    const requiredFields = formElement.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('error');
            isValid = false;
        } else {
            field.classList.remove('error');
        }
    });
    
    return isValid;
}

function serializeForm(formElement) {
    const formData = new FormData(formElement);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        // Handle multiple values for the same key
        if (data[key]) {
            if (Array.isArray(data[key])) {
                data[key].push(value);
            } else {
                data[key] = [data[key], value];
            }
        } else {
            data[key] = value;
        }
    }
    
    return data;
}

// Skill proficiency utilities
function renderProficiencyDots(level, maxLevel = 5) {
    let html = '<div class="proficiency-dots">';
    for (let i = 1; i <= maxLevel; i++) {
        const activeClass = i <= level ? 'active' : '';
        html += `<span class="proficiency-dot ${activeClass}"></span>`;
    }
    html += '</div>';
    return html;
}

function renderSkillList(skills, containerElement, options = {}) {
    if (!skills || skills.length === 0) {
        containerElement.innerHTML = '<p>No skills added yet.</p>';
        return;
    }
    
    const html = skills.map(skill => `
        <div class="skill-item" data-skill-id="${skill.id || ''}">
            <div class="skill-info">
                <div class="skill-name">${skill.name}</div>
                <div class="skill-category">${skill.category || ''}</div>
            </div>
            <div class="skill-level">
                ${renderProficiencyDots(skill.proficiency || skill.proficiency_level || 0)}
                ${options.showRemove ? '<button class="remove-skill" onclick="removeSkill(this)">×</button>' : ''}
            </div>
        </div>
    `).join('');
    
    containerElement.innerHTML = html;
}

// Progress tracking utilities
function calculateOverallProgress(progressData) {
    if (!progressData || progressData.length === 0) return 0;
    
    const totalProgress = progressData.reduce((sum, item) => {
        return sum + (item.progress_percentage || 0);
    }, 0);
    
    return Math.round(totalProgress / progressData.length);
}

function formatTimeAgo(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);
    
    if (diffInSeconds < 60) return 'Just now';
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`;
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`;
    if (diffInSeconds < 2592000) return `${Math.floor(diffInSeconds / 86400)}d ago`;
    
    return date.toLocaleDateString();
}

// Career recommendation utilities
function renderCareerRecommendations(recommendations, containerElement) {
    if (!recommendations || recommendations.length === 0) {
        containerElement.innerHTML = '<p>No recommendations available. Complete your profile to get personalized suggestions!</p>';
        return;
    }
    
    const html = recommendations.map(rec => {
        const career = rec.career_path;
        const matchPercentage = Math.round(rec.match_score * 100);
        
        return `
            <div class="recommendation-card">
                <div class="recommendation-header">
                    <h3>${career.title}</h3>
                    <div class="match-score">${matchPercentage}% Match</div>
                </div>
                <div class="career-details">
                    <p><strong>Industry:</strong> ${career.industry || 'Not specified'}</p>
                    <p><strong>Description:</strong> ${career.description || 'No description available'}</p>
                    ${career.average_salary ? `<p><strong>Average Salary:</strong> $${career.average_salary.toLocaleString()}</p>` : ''}
                    ${career.growth_rate ? `<p><strong>Growth Rate:</strong> ${career.growth_rate}%</p>` : ''}
                </div>
                <div class="recommendation-reasoning">
                    <p><strong>Why this matches:</strong> ${rec.reasoning}</p>
                </div>
                ${rec.skill_gaps && rec.skill_gaps.length > 0 ? `
                    <div class="skill-gaps">
                        <h4>Skills to develop:</h4>
                        ${rec.skill_gaps.map(gap => `
                            <div class="skill-gap-item">
                                <span>${gap.skill}</span>
                                <span>Gap: ${gap.gap} levels</span>
                            </div>
                        `).join('')}
                    </div>
                ` : ''}
            </div>
        `;
    }).join('');
    
    containerElement.innerHTML = html;
}

// Learning roadmap utilities
function renderLearningRoadmap(roadmap, containerElement) {
    if (!roadmap) {
        containerElement.innerHTML = '<p>No roadmap available. Complete your profile to get a personalized learning plan!</p>';
        return;
    }
    
    const sections = [
        { key: 'immediate_goals', title: '🎯 Immediate Goals (0-3 months)', color: '#ff6b6b' },
        { key: 'short_term_goals', title: '📈 Short-term Goals (3-12 months)', color: '#4ecdc4' },
        { key: 'long_term_goals', title: '🚀 Long-term Goals (1+ years)', color: '#45b7d1' }
    ];
    
    let html = '<div class="roadmap-sections">';
    
    sections.forEach(section => {
        const goals = roadmap[section.key] || [];
        html += `
            <div class="roadmap-section">
                <h3 style="color: ${section.color}">${section.title}</h3>
                ${goals.length > 0 ? `
                    <div class="goals-list">
                        ${goals.map(goal => `
                            <div class="goal-item">
                                <div class="goal-header">
                                    <span class="goal-skill">${goal.skill}</span>
                                    <span class="goal-time">${goal.estimated_time_weeks} weeks</span>
                                </div>
                                <div class="goal-progress">
                                    Level ${goal.current_level} → ${goal.target_level}
                                </div>
                                ${goal.resources && goal.resources.length > 0 ? `
                                    <div class="goal-resources">
                                        <h5>Recommended Resources:</h5>
                                        ${goal.resources.map(resource => `
                                            <a href="${resource.url}" target="_blank" class="resource-link">
                                                ${resource.title} (${resource.type})
                                            </a>
                                        `).join('')}
                                    </div>
                                ` : ''}
                            </div>
                        `).join('')}
                    </div>
                ` : '<p>No goals in this timeframe.</p>'}
            </div>
        `;
    });
    
    html += '</div>';
    containerElement.innerHTML = html;
}

// Initialize common functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add active class to current page navigation
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Add smooth scrolling to anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Export for use in other scripts
window.CareerAdvisor = {
    studentManager,
    showNotification,
    apiCall,
    createProgressChart,
    createDoughnutChart,
    renderSkillList,
    renderCareerRecommendations,
    renderLearningRoadmap,
    calculateOverallProgress,
    formatTimeAgo
};