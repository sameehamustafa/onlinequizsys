# 🎓 Quizify - Modern Online Quiz System

Quizify is a full-featured, responsive, role-based **Online Quiz and Examination Management System** built with **Python 3**, **Django framework**, **SQLite**, and **Bootstrap 5**.

---

## 🌟 Key Features & Architecture

### 1. User Roles & Secure Authentication
- **Role-Based Access Control**:
  - **Administrator / Staff**: Full access to the custom Admin Dashboard, Subject/Quiz/Question management, User history, and system-wide results analytics.
  - **Registered Students**: Access to the Student Dashboard, categorized quiz catalog, timed quiz engine, instant auto-grading, and personal attempt history.
- **Authentication Views**:
  - User Registration with form validation
  - Secure Login / Logout
  - Profile view and real-time profile information updates
  - Password Change with Django security hash synchronization

### 2. Admin Management Module
- **Admin Dashboard**: Visual KPI cards (Total Subjects, Total Quizzes, Total Questions, Registered Students, Total Attempts, Global Pass Rate), recent attempt feeds, and quick navigation.
- **Subject Management**: Full CRUD (Create, Read, Update, Delete) for academic subjects with custom Bootstrap icon support.
- **Quiz Management**: Full CRUD for quizzes under subjects with duration configuration, passing percentage benchmark, and draft/published visibility toggles.
- **Question Bank Management**: Full CRUD for multiple-choice questions (Option A, B, C, D, marks allocation, answer key assignment, and detailed educational explanations).
- **User & Attempt Management**: View registered students, inspect individual attempt history, and delete student accounts.
- **Results & Performance Analytics**: Filter and inspect all quiz attempts across the platform by Quiz, User, and Pass/Fail status.
- **Django Standard Admin**: Accessible at `/django-admin/` for low-level database operations.

### 3. Student Quiz Portal
- **Interactive Dashboard**: Quick metrics on completed quizzes, passed quizzes, success rate, and average score.
- **Quiz Catalog & Search**: Categorized subjects and search filtering by keyword or subject.
- **Live Timed Quiz Engine**:
  - Real-time countdown timer (`quiz_timer.js`)
  - Red warning countdown when under 60 seconds
  - Auto-submission when time limit expires
  - Clean card-based radio option selector
- **Instant Auto-Evaluation & Detailed Review**:
  - Immediate calculation of marks, percentage, correct/incorrect/unanswered counters, and pass/fail verdict.
  - Question-by-Question review highlighting user's choice vs correct answer and displaying solution explanations.
- **Attempt History**: Full history table with scores, percentages, timestamps, time taken, and instant links to breakdown reviews.

---

## 📁 Project Directory Layout

```
Quiz System/
├── manage.py
├── requirements.txt
├── README.md
├── seed_data.py                   # Automated database seeding script
├── quiz_project/                  # Django project configuration
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── quiz_app/                      # Core quiz application
    ├── __init__.py
    ├── admin.py                   # Django admin registration
    ├── apps.py
    ├── models.py                  # Subject, Quiz, Question, QuizAttempt, UserAnswer
    ├── forms.py                   # Registration, Profile, Subject, Quiz, Question forms
    ├── urls.py                    # Role-based URL routes
    ├── decorators.py              # @admin_required, @anonymous_required
    ├── views/
    │   ├── __init__.py
    │   ├── auth_views.py          # Register, Login, Logout, Profile, Password
    │   ├── user_views.py          # Dashboard, Quizzes, Attempt, Submit, Results, History
    │   └── admin_views.py         # Admin Dashboard, Subject/Quiz/Question/User CRUD
    ├── templates/
    │   ├── base.html              # Responsive Bootstrap 5 base layout
    │   ├── auth/                  # Login, Register, Profile, Change Password
    │   ├── user/                  # Student portal templates
    │   └── admin_panel/           # Custom Admin management templates
    └── static/
        ├── css/
        │   └── style.css          # Custom styling, glassmorphism, badges, animations
        └── js/
            ├── main.js            # Alerts and UI helpers
            └── quiz_timer.js      # Live countdown timer and auto-submit
```

---

## 🚀 Step-by-Step Setup & Run Instructions

### 1. Prerequisites
Ensure you have Python 3.10+ installed on your system.

### 2. Set Up Virtual Environment & Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS / Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Seed Database with Sample Data & Users

Populate sample subjects (Python, Web Dev, SQL), quizzes, multiple-choice questions, and pre-configured accounts:

```bash
python seed_data.py
```

### 5. Start Development Server

```bash
python manage.py runserver
```

Open your browser and navigate to: **`http://127.0.0.1:8000/`**

---

## 🔑 Default Login Credentials

| Role | Username | Password | Notes |
|---|---|---|---|
| **Administrator** | `admin` | `admin123` | Full access to Admin Panel & Dashboard |
| **Student User** | `student` | `student123` | Student portal, quizzes, results, and history |

*(You can also register new student accounts freely using the Registration page).*

---

## 🧪 Testing the Application

1. **Test Student Workflow**:
   - Log in as `student` / `student123`.
   - Go to **Browse Quizzes**, select **"Python Fundamentals & Data Structures"**.
   - Read instructions and click **Begin Quiz Attempt**.
   - Select answers to questions, observe the countdown timer, and submit.
   - Review your instant score, percentage badge, and question explanations.
   - Check your updated **Attempt History** and **User Dashboard**.

2. **Test Admin Workflow**:
   - Log in as `admin` / `admin123`.
   - View high-level metrics on the **Admin Dashboard**.
   - Navigate to **Subjects** &rarr; click **Add New Subject**.
   - Navigate to **Quizzes** &rarr; click **Add New Quiz**.
   - Navigate to **Questions** &rarr; add new questions with options and explanation.
   - Navigate to **Users** &rarr; inspect registered users and individual performance histories.
   - Navigate to **All Results** &rarr; filter attempts by Quiz, User, or Pass/Fail status.
