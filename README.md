
# EXAMBHAI
## By: Mayank Kumar Poddar
### 23f3004197 | Modern Application Development – II | IIT Madras
## Project Overview
This project is from the Modern Application Development - II course which is offered by IITM BS Degree during the Diploma in Programming. It is a multi-user app that acts as an exam preparation site for multiple courses. The platform provides both practice and exam modes for students to test their knowledge across various subjects and allows admins to create, manage, and analyse the quiz.

**🔗 Demo URL**: [https://exambhai.vercel.app](https://exambhai.vercel.app)  
**👤 Demo Student Login**: `user@email.com` | **🔐 Password**: `12345678`  
**👤 Demo Admin Login**: `admin@email.com` | **🔐 Password**: `12345678`

## Screenshots
<table>
   <tr>
     <td>
       <div>
         <div><img alt="Admin Dashboard" src="https://res.cloudinary.com/dohhiwhug/image/upload/v1748885275/app/static/images/localhost_5173_admin_dashboard_4.png" width="500"/></div>
         <div><img alt="Admin Student Quizzes" src="https://res.cloudinary.com/dohhiwhug/image/upload/v1748885278/app/static/images/localhost_5173_admin_dashboard.png" width="500"/></div>
       </div>
     </td>
     <td>
       <img alt="Student Result" src="https://res.cloudinary.com/dohhiwhug/image/upload/v1748885274/app/static/images/localhost_5173_admin_dashboard_1.png" width="500"/>
     </td>
   </tr>
</table>

| | | |
|:-------------------------:|:-------------------------:|:-------------------------:|
<img width="1604" alt="Student Dashboard" src="https://res.cloudinary.com/dohhiwhug/image/upload/v1748885270/app/static/images/localhost_5173_dashboard_my_quizzes_5_1.png">Student Dashboard | <img width="1604" alt="Exam Instructions" src="https://res.cloudinary.com/dohhiwhug/image/upload/v1748885270/app/static/images/localhost_5173_dashboard_my_quizzes_3_1.png">Exam Instructions | <img width="1604" alt="Exams List" src="https://res.cloudinary.com/dohhiwhug/image/upload/v1748885269/app/static/images/localhost_5173_browse_exam_1.png">Exams List

## Technologies used:
### Frontend:
- Vue.js 3 (Composition API) - JavaScript framework for building user interfaces
- Bootstrap 5 - CSS framework for responsive design
- Chart.js - JavaScript library for data visualization
- Axios - HTTP client for API requests
- Vue Router - Navigation management
- Notivue - Notification system
- Pinia - State management library for Vue 3
- Simple Datatables - Lightweight JavaScript HTML table library
  
### Backend:
- Flask - Python web framework
- Flask-RESTx - API development extension for Flask
- Flask-SQLAlchemy - ORM for database interaction
- Flask-JWT-Extended - Authentication handling with JWT
- Flask-Mail - Email functionality
- Flask-Migrate - Database migration
- Flask-Bcrypt - Password hashing
- Flask-Caching - Response caching

### Task Processing:
- Celery - Distributed task queue
- Redis - Message broker for Celery and caching  

## Setup Instructions:
Clone the repository:
```sh
git clone https://github.com/mynkpdr/mad2project.git
cd mad2project
```
### Backend (Flask)  
1. Navigate to the backend folder:
    ```sh
    cd backend
    ```
2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    ```
3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Run the backend server:
    ```sh
    flask run
    ```
5. Run the Celery beat and worker:
    ```sh
    celery -A app.worker.celery worker --beat
    ```
### Frontend (Vue 3 + Vite)  
1. Navigate to the frontend folder:
    ```sh
    cd frontend
    ```
2. Install dependencies:
    ```sh
    npm install
    ```
3. Start the development server:
    ```sh
    npm run dev
    ```
### Sample Data:
To populate the database with sample data for testing, you can use the populatedb.py script. This will insert some sample data into the database.

**Note: You need to make sure API is running because it uses API calls to send POST requests.**

Run the following command in the backend to populate the database:
```bash
python populatedb.py
```
    
## Database Schema Design:
The application uses a relational database with the following key models:
### User Model:
- Core user information (id, name, email, password, ...)
- Role-based access control (ADMIN, STUDENT)
- Account status tracking
- Email verification
- Notification preferences
- Oauth Logins

### Quiz Model:
- Quiz metadata (name, description, date_of_quiz, date_created)
- Settings (difficulty_level, time_duration)
- Quiz mode (PRACTICE, EXAM)
- Relationship to chapters and subjects

### Question Model:
- Question metadata (question_statement, marks, ...)
- Different question types (MCQ, MSQ, Numerical)
- Scoring information
- Optional images and answer explanations
  
### TakeQuiz Model:
- Represents an attempt at a quiz by a student
- Tracks completion status
- Timestamps for analytics

### QuizState Model:
- JSON storage of student's answers
- Result state for scoring and review
- Timestamp information

### Chapter/Subject Models:
- Hierarchical organization of content
- Many-to-many relationships
- 
### Other Models...

## Architecture and Features:
### Architecture:

1.  **Frontend-Backend Separation**:
- Vue.js frontend consuming REST API
- Flask backend providing RESTful endpoints
- JWT authentication for secure communication

2.  **Task Processing Pipeline**:
- Celery workers for asynchronous tasks
- Redis as message broker
- Background processing for reports and emails
- Scheduled tasks for notifications and analytics

3.  **Caching Strategy**:
- RedisCache for API response caching
- Optimized dashboard data retrieval
- Time-based cache invalidation
  
### Features:
#### Student Features:
1.  **Dual Quiz Interfaces**:
-  **Exam Mode**: Formal, assessment with strict rules similar to the IITM BS Degree quiz exams.
-  **Practice Mode**: Self-paced learning with immediate feedback.

2.  **Comprehensive Dashboard**:
- Performance analytics and visualization
- Subject-wise average scores
- Time vs. score analysis
- Points tracking and history
- Comparison between exam and practice performance

3.  **Quiz Experience**:
- Multiple question types (MCQ, MSQ, Numerical)
- Question navigation and review marking
- Scientific calculator for complex problems in exams
- Time tracking and automatic submission
- Detailed results and feedback
  
4.  **Personalization**:
- Profile management
- Performance tracking over time
- Upcoming quiz notifications
- Weekly/monthly activity reports via email
- Password reset functionality and email alerts for password resets

#### Admin Features:
1.  **Dashboard Analytics**:
- Student activity monitoring
- Quiz completion statistics
- Performance metrics by subject/chapter
- Difficulty level distribution
- Growth tracking (students and quiz attempts)

2.  **Content Management**:
- Quiz creation and scheduling
- Question bank management
- Subject and chapter organization
- CRUD the quizzes, subjects, chapters and the questions

3.  **User Management**:
- Student registration approval
- Account profile management
- Student quiz summary

### Special Implementations:
1.  **Adaptive User Interface**:
- Night mode toggle

2.  **Real-time Data Visualization**:
- Interactive charts and graphs
- Filterable date ranges
- Comparative analysis tools

3.  **Background Task Processing**:
- Automated email reports (weekly/monthly)
- Quiz reminders and notifications
- Data aggregation for analytics
  
4.  **Security Features**:
- JWT authentication with token expiry
- Password hashing with bcrypt
- Role-based access control
- Email verification


## Implementation Challenges and Solutions:
### Challenge 1: Quiz State Management
**Solution**: Implemented a robust state management system with timer using Pinia store with automatic saving and restoration of exam progress, allowing students to resume interrupted exams.

### Challenge 2: Asynchronous Task Processing
**Solution**: Integrated Celery with Redis to handle background tasks such as email notifications, report generation, and scheduled activities.

### Challenge 3: Performance Optimization for Dashboards
**Solution**: Implemented caching strategies and optimized database queries to improve dashboard loading times.

### Challenge 4: Supporting Multiple Question Types
**Solution**: Designed a flexible question model that accommodates different question types (MCQ, MSQ, Numerical) with appropriate validation and scoring logic for each type.

### Challenge 5: Quiz Results
**Solution**: The quiz results are calculated and stored efficiently using the following steps:

**1.  Score Calculation**:
- Each question is evaluated based on its type (MCQ, MSQ, Numerical).
- Correct answers are awarded marks, while incorrect answers will result in zero marks.
- Partial credit is given for MSQ questions based on the number of correct options selected.

**2.  Feedback Generation**:
- Detailed feedback is provided for each question, including the correct answer and an explanation if available.
- Overall performance metrics such as total score, percentage, time taken and comparision with others are displayed.

**3.  Result Storage**:
- Results are stored in the `Score` model, which includes the student's scores, time taken and other details.
- The `QuizState` model is used to save the state of the quiz, allowing students to review their answers and feedback.

**4.  Analytics and Reporting**:
- Performance data is aggregated to generate insights for both students and admins.
- Visualizations such as score distributions and time vs. score analysis are provided on the dashboard.

**5.  Result Display**:
- For practice mode, results are shown to students immediately after quiz submission.
- For exam mode, results are shown after twice the time duration of the exam. For example, an exam is set to start at 10:00 AM with duration of 30 minutes, then the result will be shown at 11:00 AM.

### Challenge 6: Leaderboard Points

**Solution**: Leaderboard scores are calculated using a weighted formula that considers average score, average time taken, and the total number of quizzes completed. The formula ensures a balanced evaluation of performance, efficiency, and participation.


## Future Enhancements:
**1.  Advanced Analytics**: Implement machine learning algorithms to provide personalized study recommendations based on performance patterns.

**2.  Offline Support**: Add Progressive Web App functionality to allow practice mode quizzes without internet connectivity.
