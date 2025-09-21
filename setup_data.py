from app import create_app, db
from app.models import *
import json

def populate_sample_data():
    """Populate database with sample career paths, skills, and resources"""
    
    # Create sample skills
    skills_data = [
        {"name": "Python", "category": "Technical", "description": "Programming language for AI and web development"},
        {"name": "JavaScript", "category": "Technical", "description": "Programming language for web development"},
        {"name": "Machine Learning", "category": "Technical", "description": "AI and ML algorithms and techniques"},
        {"name": "Data Analysis", "category": "Technical", "description": "Analyzing and interpreting data"},
        {"name": "SQL", "category": "Technical", "description": "Database query language"},
        {"name": "Communication", "category": "Soft", "description": "Effective verbal and written communication"},
        {"name": "Problem Solving", "category": "Soft", "description": "Analytical thinking and solution finding"},
        {"name": "Leadership", "category": "Soft", "description": "Leading teams and projects"},
        {"name": "Project Management", "category": "Soft", "description": "Planning and managing projects"},
        {"name": "Cloud Computing", "category": "Technical", "description": "AWS, Azure, Google Cloud platforms"},
        {"name": "Cybersecurity", "category": "Technical", "description": "Information security and protection"},
        {"name": "UX/UI Design", "category": "Technical", "description": "User experience and interface design"},
        {"name": "React", "category": "Technical", "description": "JavaScript library for building UIs"},
        {"name": "Docker", "category": "Technical", "description": "Containerization technology"},
        {"name": "Git", "category": "Technical", "description": "Version control system"}
    ]
    
    skills = []
    for skill_data in skills_data:
        existing_skill = Skill.query.filter_by(name=skill_data["name"]).first()
        if not existing_skill:
            skill = Skill(**skill_data)
            db.session.add(skill)
            skills.append(skill)
    
    db.session.flush()  # Get IDs for skills
    
    # Create sample interests
    interests_data = [
        {"name": "Artificial Intelligence", "category": "Technology", "description": "AI and machine learning"},
        {"name": "Web Development", "category": "Technology", "description": "Building web applications"},
        {"name": "Data Science", "category": "Technology", "description": "Data analysis and insights"},
        {"name": "Cybersecurity", "category": "Technology", "description": "Information security"},
        {"name": "Mobile Development", "category": "Technology", "description": "Building mobile applications"},
        {"name": "Cloud Computing", "category": "Technology", "description": "Cloud platforms and services"},
        {"name": "DevOps", "category": "Technology", "description": "Development and operations"},
        {"name": "Entrepreneurship", "category": "Business", "description": "Starting and running businesses"},
        {"name": "Finance", "category": "Business", "description": "Financial analysis and management"},
        {"name": "Marketing", "category": "Business", "description": "Digital and traditional marketing"}
    ]
    
    for interest_data in interests_data:
        existing_interest = Interest.query.filter_by(name=interest_data["name"]).first()
        if not existing_interest:
            interest = Interest(**interest_data)
            db.session.add(interest)
    
    # Create sample career paths
    career_paths_data = [
        {
            "title": "Software Engineer",
            "description": "Design, develop, and maintain software applications and systems.",
            "industry": "Technology",
            "required_skills": json.dumps(["Python", "JavaScript", "Git", "Problem Solving", "Communication"]),
            "average_salary": 95000,
            "growth_rate": 22.0,
            "education_requirements": "Bachelor's degree in Computer Science or related field"
        },
        {
            "title": "Data Scientist",
            "description": "Extract insights from data using statistical analysis and machine learning.",
            "industry": "Technology",
            "required_skills": json.dumps(["Python", "Machine Learning", "Data Analysis", "SQL", "Communication"]),
            "average_salary": 120000,
            "growth_rate": 25.0,
            "education_requirements": "Bachelor's or Master's degree in Data Science, Statistics, or related field"
        },
        {
            "title": "Cybersecurity Analyst",
            "description": "Protect organizations from cyber threats and security breaches.",
            "industry": "Technology",
            "required_skills": json.dumps(["Cybersecurity", "Problem Solving", "Communication", "Data Analysis"]),
            "average_salary": 85000,
            "growth_rate": 18.0,
            "education_requirements": "Bachelor's degree in Cybersecurity, IT, or related field"
        },
        {
            "title": "UX/UI Designer",
            "description": "Design user interfaces and experiences for digital products.",
            "industry": "Technology",
            "required_skills": json.dumps(["UX/UI Design", "Communication", "Problem Solving", "JavaScript"]),
            "average_salary": 75000,
            "growth_rate": 13.0,
            "education_requirements": "Bachelor's degree in Design, HCI, or related field"
        },
        {
            "title": "DevOps Engineer",
            "description": "Bridge development and operations to improve software delivery.",
            "industry": "Technology",
            "required_skills": json.dumps(["Cloud Computing", "Docker", "Python", "Problem Solving", "Communication"]),
            "average_salary": 110000,
            "growth_rate": 20.0,
            "education_requirements": "Bachelor's degree in Computer Science or related field"
        },
        {
            "title": "Product Manager",
            "description": "Lead product development and strategy from conception to launch.",
            "industry": "Technology",
            "required_skills": json.dumps(["Leadership", "Project Management", "Communication", "Problem Solving", "Data Analysis"]),
            "average_salary": 130000,
            "growth_rate": 15.0,
            "education_requirements": "Bachelor's degree in Business, Engineering, or related field"
        },
        {
            "title": "Full Stack Developer",
            "description": "Develop both front-end and back-end components of web applications.",
            "industry": "Technology",
            "required_skills": json.dumps(["JavaScript", "Python", "React", "SQL", "Git", "Communication"]),
            "average_salary": 90000,
            "growth_rate": 20.0,
            "education_requirements": "Bachelor's degree in Computer Science or related field, or equivalent experience"
        },
        {
            "title": "AI/ML Engineer",
            "description": "Develop and deploy machine learning models and AI systems.",
            "industry": "Technology",
            "required_skills": json.dumps(["Python", "Machine Learning", "Data Analysis", "Cloud Computing", "Problem Solving"]),
            "average_salary": 140000,
            "growth_rate": 30.0,
            "education_requirements": "Master's degree in AI, ML, Computer Science, or related field"
        }
    ]
    
    for career_data in career_paths_data:
        existing_career = CareerPath.query.filter_by(title=career_data["title"]).first()
        if not existing_career:
            career = CareerPath(**career_data)
            db.session.add(career)
    
    # Create sample learning resources
    resources_data = [
        {
            "title": "Python for Beginners",
            "description": "Complete Python programming course for beginners",
            "resource_type": "Course",
            "url": "https://www.coursera.org/learn/python",
            "skills_taught": json.dumps(["Python"]),
            "difficulty_level": "Beginner",
            "duration_hours": 40,
            "rating": 4.8,
            "provider": "Coursera"
        },
        {
            "title": "Machine Learning Specialization",
            "description": "Comprehensive machine learning course by Andrew Ng",
            "resource_type": "Course",
            "url": "https://www.coursera.org/specializations/machine-learning",
            "skills_taught": json.dumps(["Machine Learning", "Python", "Data Analysis"]),
            "difficulty_level": "Intermediate",
            "duration_hours": 120,
            "rating": 4.9,
            "provider": "Coursera"
        },
        {
            "title": "JavaScript: The Complete Guide",
            "description": "Modern JavaScript from beginner to advanced",
            "resource_type": "Course",
            "url": "https://www.udemy.com/course/javascript-the-complete-guide-2020-beginner-advanced/",
            "skills_taught": json.dumps(["JavaScript"]),
            "difficulty_level": "Beginner",
            "duration_hours": 52,
            "rating": 4.7,
            "provider": "Udemy"
        },
        {
            "title": "React - The Complete Guide",
            "description": "Learn React.js from scratch with hooks and context",
            "resource_type": "Course",
            "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/",
            "skills_taught": json.dumps(["React", "JavaScript"]),
            "difficulty_level": "Intermediate",
            "duration_hours": 48,
            "rating": 4.8,
            "provider": "Udemy"
        },
        {
            "title": "AWS Cloud Practitioner",
            "description": "Introduction to AWS cloud computing services",
            "resource_type": "Course",
            "url": "https://aws.amazon.com/training/",
            "skills_taught": json.dumps(["Cloud Computing"]),
            "difficulty_level": "Beginner",
            "duration_hours": 20,
            "rating": 4.6,
            "provider": "AWS"
        },
        {
            "title": "Cybersecurity Fundamentals",
            "description": "Essential cybersecurity concepts and practices",
            "resource_type": "Course",
            "url": "https://www.edx.org/course/cybersecurity-fundamentals",
            "skills_taught": json.dumps(["Cybersecurity"]),
            "difficulty_level": "Beginner",
            "duration_hours": 30,
            "rating": 4.5,
            "provider": "edX"
        },
        {
            "title": "SQL for Data Science",
            "description": "Database querying and management for data analysis",
            "resource_type": "Course",
            "url": "https://www.coursera.org/learn/sql-for-data-science",
            "skills_taught": json.dumps(["SQL", "Data Analysis"]),
            "difficulty_level": "Beginner",
            "duration_hours": 25,
            "rating": 4.7,
            "provider": "Coursera"
        },
        {
            "title": "Docker Mastery",
            "description": "Complete guide to Docker containerization",
            "resource_type": "Course",
            "url": "https://www.udemy.com/course/docker-mastery/",
            "skills_taught": json.dumps(["Docker", "Cloud Computing"]),
            "difficulty_level": "Intermediate",
            "duration_hours": 19,
            "rating": 4.8,
            "provider": "Udemy"
        }
    ]
    
    for resource_data in resources_data:
        existing_resource = LearningResource.query.filter_by(title=resource_data["title"]).first()
        if not existing_resource:
            resource = LearningResource(**resource_data)
            db.session.add(resource)
    
    try:
        db.session.commit()
        print("✅ Sample data populated successfully!")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error populating sample data: {e}")
        return False

if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("📊 Database tables created")
        
        # Populate with sample data
        populate_sample_data()
        
        print("\n🚀 Database setup complete! You can now run the application.")
        print("Run: python run.py")