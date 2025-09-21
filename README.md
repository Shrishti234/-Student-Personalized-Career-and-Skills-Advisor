# 🎯 Student Personalized Career and Skills Advisor

A comprehensive AI-powered career advisory system that helps students navigate their professional journey through personalized recommendations, skill mapping, and dynamic learning roadmaps.

## 🌟 Features

### 🔍 AI-Powered Career Recommendations
- **Intelligent Matching**: Advanced AI algorithms analyze student profiles to recommend tailored career paths
- **Skills Gap Analysis**: Identifies specific skills needed for target careers
- **Industry Insights**: Real-time data on salary ranges, growth rates, and job market trends
- **Personalized Reasoning**: Clear explanations for each career recommendation

### 📊 Interactive Dashboard
- **Real-time Analytics**: Live updates on learning progress and career matches
- **Visual Progress Tracking**: Charts and graphs showing skill development over time
- **Industry Trends**: Current market insights and emerging opportunities
- **Achievement System**: Milestone tracking and progress recognition

### 🗺️ Dynamic Learning Roadmaps
- **Personalized Learning Paths**: Custom roadmaps based on career goals and current skills
- **Time-based Goals**: Short-term (0-3 months), medium-term (3-12 months), and long-term (1+ years) planning
- **Resource Recommendations**: Curated learning materials from top platforms
- **Progress Milestones**: Clear checkpoints to track advancement

### 👤 Comprehensive Student Profiles
- **Skills Assessment**: Self-evaluation with proficiency levels (1-5 scale)
- **Interest Mapping**: Strength-based interest tracking across multiple categories
- **Academic Integration**: GPA, major, and graduation year consideration
- **Goal Setting**: Career aspirations and learning objectives

### 📈 Progress Tracking System
- **Skill Development Monitoring**: Real-time tracking of proficiency improvements
- **Achievement Badges**: Recognition system for completed milestones
- **Learning Analytics**: Detailed insights into learning patterns and progress
- **Resource Completion Tracking**: Monitor courses, articles, and tutorials completed

## 🛠️ Technology Stack

### Backend
- **Flask**: Lightweight Python web framework for API development
- **SQLAlchemy**: Object-relational mapping for database operations
- **SQLite**: Embedded database for data persistence
- **Custom AI Engine**: Proprietary recommendation algorithms

### Frontend
- **HTML5/CSS3**: Modern, responsive web interface
- **JavaScript (ES6+)**: Interactive client-side functionality
- **Chart.js**: Data visualization and progress charts
- **Responsive Design**: Mobile-first approach for all devices

### AI & Analytics
- **Text Similarity Analysis**: Natural language processing for profile matching
- **Skill Gap Analysis**: Algorithmic identification of learning opportunities
- **Career Path Scoring**: Multi-factor recommendation scoring system
- **Learning Path Generation**: Intelligent roadmap creation

## 📋 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Shrishti234/-Student-Personalized-Career-and-Skills-Advisor.git
   cd -Student-Personalized-Career-and-Skills-Advisor
   ```

2. **Install Dependencies**
   ```bash
   pip install Flask Flask-SQLAlchemy
   ```

3. **Initialize Database**
   ```bash
   python setup_data.py
   ```

4. **Run the Application**
   ```bash
   python run.py
   ```

5. **Access the Application**
   Open your browser and navigate to `http://localhost:5000`

### Database Setup
The application automatically creates a SQLite database with sample data including:
- 15+ predefined skills across technical and soft skill categories
- 8+ career paths in technology industry with detailed requirements
- 8+ learning resources from top educational platforms
- Sample interests across technology, business, and other domains

## 🎮 Usage Guide

### Getting Started

1. **Create Your Profile**
   - Enter basic information (name, email, academic level, major)
   - Add your current skills with proficiency ratings
   - Include interests with strength indicators

2. **Get Career Recommendations**
   - View AI-generated career matches based on your profile
   - Explore detailed career information including salaries and growth rates
   - Understand why each career was recommended for you

3. **Build Your Learning Roadmap**
   - Generate personalized learning paths for your target careers
   - Set short-term and long-term learning goals
   - Access curated learning resources for each skill

4. **Track Your Progress**
   - Update your skill proficiency as you learn
   - Mark milestones and completed resources
   - Monitor your overall learning progress

### Key Workflows

#### Profile Completion
1. Navigate to Profile page
2. Add 5-10 relevant skills with honest proficiency ratings
3. Include 3-5 interests with strength levels
4. Ensure all required fields are completed

#### Career Exploration
1. Complete your profile first
2. Visit Recommendations page
3. Review top career matches
4. Explore detailed career information
5. Note skill gaps for targeted learning

#### Learning Path Creation
1. Get career recommendations
2. Navigate to Learning Roadmap
3. Review immediate, short-term, and long-term goals
4. Start with immediate goals (0-3 months)
5. Use recommended resources for each skill

## 🏗️ System Architecture

### Database Schema
- **Students**: Personal information and academic details
- **Skills**: Comprehensive skill database with categories
- **Interests**: Interest areas with descriptions
- **Career Paths**: Industry roles with requirements and statistics
- **Learning Resources**: Curated educational content
- **Progress Tracking**: Student learning advancement data

### AI Recommendation Engine
- **Profile Analysis**: Text processing of student skills and interests
- **Career Matching**: Similarity scoring between profiles and career requirements
- **Skill Gap Identification**: Analysis of missing or underdeveloped skills
- **Learning Path Generation**: Intelligent sequencing of skill development

### API Endpoints

#### Student Management
- `POST /api/students` - Create new student profile
- `GET /api/students/{id}` - Retrieve student information
- `POST /api/students/{id}/skills` - Add/update student skills
- `POST /api/students/{id}/interests` - Add/update student interests

#### Recommendations
- `GET /api/students/{id}/recommendations` - Get career recommendations
- `GET /api/students/{id}/roadmap` - Generate learning roadmap
- `GET /api/students/{id}/progress` - Retrieve progress data
- `POST /api/students/{id}/progress` - Update learning progress

#### Data Access
- `GET /api/careers` - List all career paths
- `GET /api/skills` - List all available skills
- `GET /api/resources` - List learning resources

## 🎨 User Interface

### Dashboard
- **Welcome Section**: Personalized greeting and navigation
- **Quick Stats**: Career matches, skills tracked, progress percentage
- **Recent Recommendations**: Top career suggestions
- **Skill Progress**: Visual charts of learning advancement
- **Next Steps**: Immediate learning goals
- **Industry Trends**: Current market insights

### Profile Management
- **Personal Information**: Editable academic and contact details
- **Skills Section**: Interactive skill addition with proficiency sliders
- **Interests Section**: Interest categorization with strength indicators
- **Visual Feedback**: Real-time profile completion status

### Career Recommendations
- **Match Scoring**: Percentage-based compatibility ratings
- **Detailed Career Cards**: Comprehensive role information
- **Skill Gap Analysis**: Clear identification of learning needs
- **Action Buttons**: Save, explore, or create learning paths

### Learning Roadmap
- **Timeline View**: Visual representation of learning phases
- **Goal Categorization**: Immediate, short-term, and long-term objectives
- **Resource Integration**: Direct links to learning materials
- **Progress Tracking**: Visual progress bars and completion status

## 🔧 Customization & Extension

### Adding New Career Paths
1. Update `setup_data.py` with new career information
2. Include required skills, salary data, and growth rates
3. Add detailed job descriptions and education requirements
4. Re-run database setup to populate new data

### Integrating Learning Platforms
1. Extend `LearningResource` model with platform-specific fields
2. Add API integrations for dynamic resource fetching
3. Implement progress synchronization with external platforms
4. Update recommendation algorithms for platform preferences

### Advanced Analytics
1. Add database logging for user interactions
2. Implement learning pattern analysis
3. Create predictive models for career success
4. Build comparative analytics for peer benchmarking

## 🚀 Future Enhancements

### Planned Features
- **AI Chatbot**: Interactive career counseling assistant
- **Peer Networking**: Connect with students on similar paths
- **Mentor Matching**: Connection with industry professionals
- **Job Board Integration**: Real-time job opportunity matching
- **Resume Builder**: AI-powered resume optimization
- **Interview Preparation**: Mock interviews and feedback

### Technical Improvements
- **Machine Learning Models**: Enhanced recommendation accuracy
- **Real-time Updates**: WebSocket integration for live updates
- **Mobile Application**: Native iOS and Android apps
- **Advanced Analytics**: Predictive modeling and trend analysis
- **Social Features**: Community forums and study groups

## 🤝 Contributing

We welcome contributions to improve the AI Career Advisor! Areas where you can help:

- **Algorithm Enhancement**: Improve recommendation accuracy
- **UI/UX Design**: Enhance user interface and experience
- **Data Integration**: Add more career paths and learning resources
- **Testing**: Improve test coverage and quality assurance
- **Documentation**: Expand guides and API documentation

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Install development dependencies
4. Make your changes with tests
5. Submit a pull request

## 📄 License

This project is designed for educational and career development purposes. Please ensure compliance with data privacy regulations when handling student information.

## 🙏 Acknowledgments

- **Educational Institutions**: For providing insight into student career development needs
- **Industry Partners**: For sharing job market data and skill requirements
- **Learning Platforms**: Coursera, Udemy, edX, and others for educational content
- **Open Source Community**: For tools and libraries that make this project possible

---

**Built with ❤️ for student success and career development**

For support, feature requests, or contributions, please open an issue or contact the development team.
