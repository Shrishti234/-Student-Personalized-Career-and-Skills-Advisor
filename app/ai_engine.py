import json
import re
import math
from collections import Counter
from app.models import Student, CareerPath, Skill, StudentSkill, StudentInterest

class CareerRecommendationEngine:
    def __init__(self):
        self.career_paths_data = []
        
    def prepare_career_data(self):
        """Prepare career path data"""
        career_paths = CareerPath.query.all()
        
        self.career_paths_data = []
        for cp in career_paths:
            required_skills = json.loads(cp.required_skills) if cp.required_skills else []
            self.career_paths_data.append({
                'id': cp.id,
                'title': cp.title,
                'description': cp.description,
                'industry': cp.industry,
                'required_skills': required_skills,
                'average_salary': cp.average_salary or 0,
                'growth_rate': cp.growth_rate or 0,
                'career_path': cp
            })
    
    def calculate_text_similarity(self, text1, text2):
        """Simple text similarity using word overlap"""
        if not text1 or not text2:
            return 0.0
            
        # Convert to lowercase and split into words
        words1 = set(re.findall(r'\b\w+\b', text1.lower()))
        words2 = set(re.findall(r'\b\w+\b', text2.lower()))
        
        if not words1 or not words2:
            return 0.0
        
        # Calculate Jaccard similarity
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def create_student_profile_text(self, student):
        """Create a text representation of student profile"""
        student_skills = StudentSkill.query.filter_by(student_id=student.id).all()
        student_interests = StudentInterest.query.filter_by(student_id=student.id).all()
        
        # Create weighted text based on proficiency/strength
        skills_text = []
        for ss in student_skills:
            skill_name = ss.skill.name.lower()
            # Repeat skill name based on proficiency level
            skills_text.extend([skill_name] * ss.proficiency_level)
        
        interests_text = []
        for si in student_interests:
            interest_name = si.interest.name.lower()
            # Repeat interest name based on strength
            interests_text.extend([interest_name] * si.strength)
        
        # Combine all profile information
        profile_parts = [
            student.major or '',
            student.academic_level,
            ' '.join(skills_text),
            ' '.join(interests_text)
        ]
        
        return ' '.join(filter(None, profile_parts)).lower()
    
    def calculate_skill_match_score(self, student, career_path):
        """Calculate how well student's skills match career requirements"""
        required_skills = json.loads(career_path.required_skills) if career_path.required_skills else []
        student_skills = {ss.skill.name.lower(): ss.proficiency_level for ss in student.skills}
        
        if not required_skills:
            return 0.5  # Neutral score if no requirements specified
        
        total_score = 0
        matched_skills = 0
        
        for skill in required_skills:
            skill_lower = skill.lower()
            if skill_lower in student_skills:
                # Score based on proficiency (1-5 scale normalized to 0-1)
                total_score += student_skills[skill_lower] / 5.0
                matched_skills += 1
            else:
                # Check for partial matches in skill names
                partial_match = False
                for student_skill in student_skills:
                    if skill_lower in student_skill or student_skill in skill_lower:
                        total_score += student_skills[student_skill] / 10.0  # Reduced score for partial match
                        partial_match = True
                        break
                
                if not partial_match:
                    total_score += 0.1  # Small penalty for missing skills
        
        return min(total_score / len(required_skills), 1.0)
    
    def identify_skill_gaps(self, student, career_path):
        """Identify skills the student needs to develop for this career"""
        required_skills = json.loads(career_path.required_skills) if career_path.required_skills else []
        student_skills = {ss.skill.name.lower(): ss.proficiency_level for ss in student.skills}
        
        gaps = []
        for skill in required_skills:
            skill_lower = skill.lower()
            current_level = 0
            
            # Look for exact or partial matches
            for student_skill, level in student_skills.items():
                if skill_lower == student_skill or skill_lower in student_skill or student_skill in skill_lower:
                    current_level = max(current_level, level)
            
            target_level = 3  # Assume 3 is minimum proficiency needed
            if current_level < target_level:
                gaps.append({
                    'skill': skill,
                    'current_level': current_level,
                    'target_level': target_level,
                    'gap': target_level - current_level
                })
        
        return sorted(gaps, key=lambda x: x['gap'], reverse=True)
    
    def recommend_careers(self, student, top_k=5):
        """Generate top-k career recommendations for a student"""
        if not self.career_paths_data:
            self.prepare_career_data()
        
        if not self.career_paths_data:
            return []
        
        student_profile_text = self.create_student_profile_text(student)
        
        recommendations = []
        for career_data in self.career_paths_data:
            career_path = career_data['career_path']
            
            # Create career text representation
            career_text = f"{career_path.title} {career_path.description} {career_path.industry} {' '.join(career_data['required_skills'])}"
            
            # Calculate text similarity
            text_similarity = self.calculate_text_similarity(student_profile_text, career_text)
            
            # Calculate skill match
            skill_match = self.calculate_skill_match_score(student, career_path)
            
            # Calculate salary and growth factor
            salary_factor = min((career_data['average_salary'] or 50000) / 100000, 1.0)  # Normalize to 0-1
            growth_factor = min((career_data['growth_rate'] or 10) / 30, 1.0)  # Normalize to 0-1
            
            # Combine scores with weights
            final_score = (
                0.4 * text_similarity +
                0.4 * skill_match +
                0.1 * salary_factor +
                0.1 * growth_factor
            )
            
            skill_gaps = self.identify_skill_gaps(student, career_path)
            
            recommendations.append({
                'career_path': career_path,
                'match_score': final_score,
                'similarity_score': text_similarity,
                'skill_match_score': skill_match,
                'skill_gaps': skill_gaps,
                'reasoning': self.generate_reasoning(student, career_path, text_similarity, skill_match)
            })
        
        # Sort by final score and return top-k
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return recommendations[:top_k]
    
    def generate_reasoning(self, student, career_path, similarity_score, skill_match_score):
        """Generate human-readable reasoning for the recommendation"""
        reasons = []
        
        if similarity_score > 0.7:
            reasons.append("Strong alignment with your interests and background")
        elif similarity_score > 0.5:
            reasons.append("Good alignment with your profile")
        
        if skill_match_score > 0.7:
            reasons.append("You have most of the required skills")
        elif skill_match_score > 0.5:
            reasons.append("You have some relevant skills with room to grow")
        else:
            reasons.append("Great opportunity to develop new skills")
        
        if career_path.growth_rate and career_path.growth_rate > 10:
            reasons.append("High growth industry with excellent job prospects")
        
        if career_path.average_salary and career_path.average_salary > 70000:
            reasons.append("Competitive salary range")
        
        return " • ".join(reasons) if reasons else "Based on your profile analysis"

class LearningPathGenerator:
    def __init__(self):
        pass
    
    def generate_learning_roadmap(self, student, career_recommendations):
        """Generate a personalized learning roadmap based on career goals"""
        roadmap = {
            'immediate_goals': [],  # 0-3 months
            'short_term_goals': [], # 3-12 months
            'long_term_goals': []   # 1+ years
        }
        
        all_skill_gaps = []
        for rec in career_recommendations:
            all_skill_gaps.extend(rec['skill_gaps'])
        
        # Group and prioritize skills
        skill_priority = {}
        for gap in all_skill_gaps:
            skill = gap['skill']
            if skill in skill_priority:
                skill_priority[skill] += gap['gap']
            else:
                skill_priority[skill] = gap['gap']
        
        # Sort skills by priority
        prioritized_skills = sorted(skill_priority.items(), key=lambda x: x[1], reverse=True)
        
        # Assign skills to timeframes based on complexity and current gaps
        for i, (skill, gap_score) in enumerate(prioritized_skills[:15]):  # Top 15 skills
            skill_obj = Skill.query.filter(Skill.name.ilike(f'%{skill}%')).first()
            
            goal = {
                'skill': skill,
                'current_level': 5 - gap_score,  # Approximate current level
                'target_level': 3,
                'resources': self.find_learning_resources(skill),
                'estimated_time_weeks': max(2, int(gap_score * 4))
            }
            
            if i < 3 and gap_score > 2:  # Most critical gaps
                roadmap['immediate_goals'].append(goal)
            elif i < 8:
                roadmap['short_term_goals'].append(goal)
            else:
                roadmap['long_term_goals'].append(goal)
        
        return roadmap
    
    def find_learning_resources(self, skill):
        """Find relevant learning resources for a skill"""
        from app.models import LearningResource
        
        resources = LearningResource.query.filter(
            LearningResource.skills_taught.contains(skill)
        ).limit(3).all()
        
        return [{
            'title': r.title,
            'type': r.resource_type,
            'url': r.url,
            'difficulty': r.difficulty_level,
            'duration_hours': r.duration_hours,
            'rating': r.rating
        } for r in resources]