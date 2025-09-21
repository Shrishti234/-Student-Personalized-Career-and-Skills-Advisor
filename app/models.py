from app import db
from datetime import datetime
import json

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    academic_level = db.Column(db.String(50), nullable=False)
    major = db.Column(db.String(100))
    gpa = db.Column(db.Float)
    graduation_year = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    skills = db.relationship('StudentSkill', backref='student', lazy=True, cascade='all, delete-orphan')
    interests = db.relationship('StudentInterest', backref='student', lazy=True, cascade='all, delete-orphan')
    recommendations = db.relationship('CareerRecommendation', backref='student', lazy=True, cascade='all, delete-orphan')
    progress = db.relationship('StudentProgress', backref='student', lazy=True, cascade='all, delete-orphan')

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Technical, Soft, Domain-specific
    description = db.Column(db.Text)
    
    # Relationships
    student_skills = db.relationship('StudentSkill', backref='skill', lazy=True)

class StudentSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    proficiency_level = db.Column(db.Integer, nullable=False)  # 1-5 scale
    is_desired = db.Column(db.Boolean, default=False)  # Skills they want to learn
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)

class StudentInterest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    interest_id = db.Column(db.Integer, db.ForeignKey('interest.id'), nullable=False)
    strength = db.Column(db.Integer, nullable=False)  # 1-5 scale
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CareerPath(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    industry = db.Column(db.String(100))
    required_skills = db.Column(db.Text)  # JSON string
    average_salary = db.Column(db.Integer)
    growth_rate = db.Column(db.Float)  # Percentage
    education_requirements = db.Column(db.Text)
    
    # Relationships
    recommendations = db.relationship('CareerRecommendation', backref='career_path', lazy=True)

class CareerRecommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    career_path_id = db.Column(db.Integer, db.ForeignKey('career_path.id'), nullable=False)
    match_score = db.Column(db.Float, nullable=False)  # 0-1 scale
    reasoning = db.Column(db.Text)
    skill_gaps = db.Column(db.Text)  # JSON string
    recommended_resources = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LearningResource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    resource_type = db.Column(db.String(50), nullable=False)  # Course, Article, Book, Video, etc.
    url = db.Column(db.String(500))
    skills_taught = db.Column(db.Text)  # JSON string
    difficulty_level = db.Column(db.String(20))  # Beginner, Intermediate, Advanced
    duration_hours = db.Column(db.Integer)
    rating = db.Column(db.Float)
    provider = db.Column(db.String(100))

class StudentProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    target_proficiency = db.Column(db.Integer, nullable=False)
    current_proficiency = db.Column(db.Integer, nullable=False)
    resources_completed = db.Column(db.Text)  # JSON string
    milestones = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    skill = db.relationship('Skill', backref='progress_records')