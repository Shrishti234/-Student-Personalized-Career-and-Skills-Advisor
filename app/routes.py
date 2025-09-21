from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from app.models import *
from app.ai_engine import CareerRecommendationEngine, LearningPathGenerator
from app import db
import json

# Create blueprints
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

# Initialize AI components
recommendation_engine = CareerRecommendationEngine()
learning_path_generator = LearningPathGenerator()

@main_bp.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@main_bp.route('/profile')
def profile():
    """Student profile management page"""
    return render_template('profile.html')

@main_bp.route('/recommendations')
def recommendations():
    """Career recommendations page"""
    return render_template('recommendations.html')

@main_bp.route('/roadmap')
def roadmap():
    """Learning roadmap page"""
    return render_template('roadmap.html')

@main_bp.route('/progress')
def progress():
    """Progress tracking page"""
    return render_template('progress.html')

# API Routes
@api_bp.route('/students', methods=['POST'])
def create_student():
    """Create a new student profile"""
    data = request.get_json()
    
    try:
        student = Student(
            name=data['name'],
            email=data['email'],
            academic_level=data['academic_level'],
            major=data.get('major'),
            gpa=data.get('gpa'),
            graduation_year=data.get('graduation_year')
        )
        
        db.session.add(student)
        db.session.commit()
        
        return jsonify({
            'id': student.id,
            'name': student.name,
            'email': student.email,
            'message': 'Student profile created successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api_bp.route('/students/<int:student_id>')
def get_student(student_id):
    """Get student profile"""
    student = Student.query.get_or_404(student_id)
    
    return jsonify({
        'id': student.id,
        'name': student.name,
        'email': student.email,
        'academic_level': student.academic_level,
        'major': student.major,
        'gpa': student.gpa,
        'graduation_year': student.graduation_year,
        'skills': [{
            'name': ss.skill.name,
            'category': ss.skill.category,
            'proficiency': ss.proficiency_level,
            'is_desired': ss.is_desired
        } for ss in student.skills],
        'interests': [{
            'name': si.interest.name,
            'category': si.interest.category,
            'strength': si.strength
        } for si in student.interests]
    })

@api_bp.route('/students/<int:student_id>/skills', methods=['POST'])
def add_student_skill():
    """Add or update a skill for a student"""
    student_id = request.view_args['student_id']
    data = request.get_json()
    
    student = Student.query.get_or_404(student_id)
    
    # Find or create skill
    skill = Skill.query.filter_by(name=data['skill_name']).first()
    if not skill:
        skill = Skill(
            name=data['skill_name'],
            category=data.get('category', 'Technical'),
            description=data.get('description', '')
        )
        db.session.add(skill)
        db.session.flush()
    
    # Find or create student skill
    student_skill = StudentSkill.query.filter_by(
        student_id=student_id,
        skill_id=skill.id
    ).first()
    
    if student_skill:
        student_skill.proficiency_level = data['proficiency_level']
        student_skill.is_desired = data.get('is_desired', False)
    else:
        student_skill = StudentSkill(
            student_id=student_id,
            skill_id=skill.id,
            proficiency_level=data['proficiency_level'],
            is_desired=data.get('is_desired', False)
        )
        db.session.add(student_skill)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Skill added/updated successfully',
        'skill': skill.name,
        'proficiency': student_skill.proficiency_level
    })

@api_bp.route('/students/<int:student_id>/interests', methods=['POST'])
def add_student_interest():
    """Add an interest for a student"""
    student_id = request.view_args['student_id']
    data = request.get_json()
    
    # Find or create interest
    interest = Interest.query.filter_by(name=data['interest_name']).first()
    if not interest:
        interest = Interest(
            name=data['interest_name'],
            category=data.get('category', 'General'),
            description=data.get('description', '')
        )
        db.session.add(interest)
        db.session.flush()
    
    # Find or create student interest
    student_interest = StudentInterest.query.filter_by(
        student_id=student_id,
        interest_id=interest.id
    ).first()
    
    if student_interest:
        student_interest.strength = data['strength']
    else:
        student_interest = StudentInterest(
            student_id=student_id,
            interest_id=interest.id,
            strength=data['strength']
        )
        db.session.add(student_interest)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Interest added/updated successfully',
        'interest': interest.name,
        'strength': student_interest.strength
    })

@api_bp.route('/students/<int:student_id>/recommendations')
def get_career_recommendations(student_id):
    """Get personalized career recommendations for a student"""
    student = Student.query.get_or_404(student_id)
    
    try:
        recommendations = recommendation_engine.recommend_careers(student, top_k=5)
        
        result = []
        for rec in recommendations:
            cp = rec['career_path']
            result.append({
                'career_path': {
                    'id': cp.id,
                    'title': cp.title,
                    'description': cp.description,
                    'industry': cp.industry,
                    'average_salary': cp.average_salary,
                    'growth_rate': cp.growth_rate,
                    'education_requirements': cp.education_requirements
                },
                'match_score': round(rec['match_score'], 3),
                'skill_match_score': round(rec['skill_match_score'], 3),
                'reasoning': rec['reasoning'],
                'skill_gaps': rec['skill_gaps'][:5]  # Top 5 gaps
            })
        
        return jsonify({
            'student_id': student_id,
            'recommendations': result,
            'generated_at': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to generate recommendations: {str(e)}'}), 500

@api_bp.route('/students/<int:student_id>/roadmap')
def get_learning_roadmap(student_id):
    """Get personalized learning roadmap for a student"""
    student = Student.query.get_or_404(student_id)
    
    try:
        # Get recent recommendations
        recommendations = recommendation_engine.recommend_careers(student, top_k=3)
        
        # Generate roadmap
        roadmap = learning_path_generator.generate_learning_roadmap(student, recommendations)
        
        return jsonify({
            'student_id': student_id,
            'roadmap': roadmap,
            'generated_at': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to generate roadmap: {str(e)}'}), 500

@api_bp.route('/students/<int:student_id>/progress')
def get_student_progress(student_id):
    """Get student's learning progress"""
    student = Student.query.get_or_404(student_id)
    
    progress_data = []
    for progress in student.progress:
        milestones = json.loads(progress.milestones) if progress.milestones else []
        resources_completed = json.loads(progress.resources_completed) if progress.resources_completed else []
        
        progress_data.append({
            'skill': progress.skill.name,
            'current_proficiency': progress.current_proficiency,
            'target_proficiency': progress.target_proficiency,
            'progress_percentage': (progress.current_proficiency / progress.target_proficiency) * 100,
            'milestones': milestones,
            'resources_completed': resources_completed,
            'updated_at': progress.updated_at.isoformat()
        })
    
    return jsonify({
        'student_id': student_id,
        'progress': progress_data
    })

@api_bp.route('/students/<int:student_id>/progress', methods=['POST'])
def update_student_progress(student_id):
    """Update student's progress on a skill"""
    data = request.get_json()
    
    student = Student.query.get_or_404(student_id)
    skill = Skill.query.filter_by(name=data['skill_name']).first()
    
    if not skill:
        return jsonify({'error': 'Skill not found'}), 404
    
    progress = StudentProgress.query.filter_by(
        student_id=student_id,
        skill_id=skill.id
    ).first()
    
    if not progress:
        progress = StudentProgress(
            student_id=student_id,
            skill_id=skill.id,
            target_proficiency=data.get('target_proficiency', 5),
            current_proficiency=data['current_proficiency']
        )
        db.session.add(progress)
    else:
        progress.current_proficiency = data['current_proficiency']
        if 'target_proficiency' in data:
            progress.target_proficiency = data['target_proficiency']
    
    # Update milestones if provided
    if 'milestones' in data:
        progress.milestones = json.dumps(data['milestones'])
    
    # Update completed resources if provided
    if 'resources_completed' in data:
        progress.resources_completed = json.dumps(data['resources_completed'])
    
    db.session.commit()
    
    return jsonify({
        'message': 'Progress updated successfully',
        'skill': skill.name,
        'current_proficiency': progress.current_proficiency,
        'progress_percentage': (progress.current_proficiency / progress.target_proficiency) * 100
    })

@api_bp.route('/careers')
def list_career_paths():
    """List all available career paths"""
    career_paths = CareerPath.query.all()
    
    result = []
    for cp in career_paths:
        result.append({
            'id': cp.id,
            'title': cp.title,
            'description': cp.description,
            'industry': cp.industry,
            'average_salary': cp.average_salary,
            'growth_rate': cp.growth_rate,
            'required_skills': json.loads(cp.required_skills) if cp.required_skills else []
        })
    
    return jsonify(result)

@api_bp.route('/skills')
def list_skills():
    """List all available skills"""
    skills = Skill.query.all()
    
    result = []
    for skill in skills:
        result.append({
            'id': skill.id,
            'name': skill.name,
            'category': skill.category,
            'description': skill.description
        })
    
    return jsonify(result)

@api_bp.route('/resources')
def list_learning_resources():
    """List all learning resources"""
    resources = LearningResource.query.all()
    
    result = []
    for resource in resources:
        result.append({
            'id': resource.id,
            'title': resource.title,
            'description': resource.description,
            'type': resource.resource_type,
            'url': resource.url,
            'skills_taught': json.loads(resource.skills_taught) if resource.skills_taught else [],
            'difficulty_level': resource.difficulty_level,
            'duration_hours': resource.duration_hours,
            'rating': resource.rating,
            'provider': resource.provider
        })
    
    return jsonify(result)