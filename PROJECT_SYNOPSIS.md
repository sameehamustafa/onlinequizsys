# PROJECT SYNOPSIS

---

### **DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING**
### **KAMLA NEHRU INSTITUTE OF TECHNOLOGY, SULTANPUR**
#### **ACADEMIC SESSION: 2026–2027**

---

```
========================================================================================
                          PROJECT SYNOPSIS REPORT
      TOPIC: ONLINE QUIZ SYSTEM USING PYTHON DJANGO AND SQLITE DATABASE
========================================================================================
```

- **Project Title:** Online Quiz System using Python Django and SQLite
- **Author / Candidate Name:** Anuj Kumar
- **Degree Program:** Bachelor of Technology (B.Tech) in Computer Science & Engineering
- **Department:** Department of Computer Science & Engineering
- **Institution:** Kamla Nehru Institute of Technology (KNIT), Sultanpur, Uttar Pradesh, India
- **Technology Stack:** Python 3.12+, Django 5.x Framework, SQLite 3, HTML5, CSS3, JavaScript (ES6+), Bootstrap 5

---

## 1. Title of the Project

**Title:** Online Quiz System using Python Django and SQLite

- **Author:** Anuj Kumar
- **Institution:** Department of Computer Science & Engineering, Kamla Nehru Institute of Technology, Sultanpur
- **Academic Year:** 2026–2027
- **Primary Domain:** Web Application Development, Computer-Based Assessment (CBA), Educational Technology (EdTech)
- **Technology Stack:**
  - *Backend Core:* Python 3, Django Web Framework (Model-View-Template Architecture)
  - *Database Management:* SQLite 3 Relational Database
  - *Frontend & User Interface:* HTML5, CSS3, Vanilla JavaScript (ES6+), Bootstrap 5, Bootstrap Icons

---

## 2. Introduction

### 2.1 Background
The integration of Information and Communication Technology (ICT) in academic and corporate pedagogy has radically revolutionized traditional evaluation paradigms. Computer-Based Assessment (CBA) and web-based examination platforms have emerged as indispensable tools for educational institutions, standardized testing agencies, and vocational recruitment pipelines. Traditional pen-and-paper examinations inherently incur significant administrative overhead, high paper consumption, logistical complexities in physical script distribution, susceptibility to human evaluation errors, and substantial delays in announcing results and delivering diagnostic feedback to examinees.

### 2.2 Purpose and Scope
The **Online Quiz System** is designed as a centralized, robust, secure, and user-centric web platform engineered using Python’s high-level Django web framework and an SQLite relational database engine. The system automates the entire lifecycle of student assessments—ranging from subject-categorized quiz discovery and timed multiple-choice questionnaire (MCQ) delivery to automated instantaneous evaluation, immediate diagnostic feedback, and historical performance tracking.

The application incorporates strict **Role-Based Access Control (RBAC)**, bifurcating platform capabilities into two discrete functional ecosystems:
1. **Administrative Management Panel:** Empowers educators and system administrators with granular control over academic subject categorization, quiz configuration (allotted time, pass percentages, publication status), question bank authoring with option mapping and explanatory notes, user account oversight, and global performance analytics.
2. **Student Examination Portal:** Delivers an intuitive, clutter-free, responsive assessment environment featuring dynamic countdown timers, client-side auto-submission triggers upon time expiry, real-time grading calculation, and comprehensive post-submission question review showcasing correct answer keys and explanatory rationale.

---

## 3. Problem Statement

Traditional paper-and-pencil examinations and fragmented manual assessment systems suffer from fundamental systemic bottlenecks:

1. **Logistical Inefficiencies and Resource Waste:** Printing, transporting, safeguarding, and physically archiving examination papers entail heavy recurrent logistical expenditures and substantial environmental costs.
2. **Evaluation Latency and Feedback Delay:** Manual paper correction is laborious and inherently prone to subjective grading discrepancies, transcription errors, and prolonged turnaround intervals before students receive their grades.
3. **Absence of Real-Time Analytics:** Conventional examination models do not provide immediate granular diagnostics (e.g., time-per-question metrics, topic-wise proficiency distribution, historical performance trend analysis) to assist learners in self-remediation.
4. **Administrative Bottlenecks in Question Management:** Maintaining physical question repositories restricts dynamic test generation, rapid updates to erroneous questions, and modular categorization based on changing course syllabi.
5. **Security and Integrity Vulnerabilities:** Physical papers are vulnerable to leakage, loss in transit, unauthorized tampering, and physical destruction.

Consequently, there is an imperative academic requirement for a responsive, modular, scalable, and autonomous web-based assessment application that eliminates manual grading bottlenecks while upholding data integrity, assessment security, and operational reliability.

---

## 4. Objectives

The primary engineering objectives of the Online Quiz System project are:

1. **Automated Assessment & Instantaneous Grading:**
   - Eliminate manual evaluation through an automated server-side evaluation algorithm that calculates raw scores, percentages, and pass/fail thresholds in sub-second execution intervals upon submission.
2. **Role-Based Access Control (RBAC) & Secure Authentication:**
   - Implement secure user registration, session-based authentication, encrypted credential storage (utilizing PBKDF2 hashing with SHA-256), profile updates, and strict permission segregation between administrative staff and registered candidates.
3. **Dynamic Academic Subject & Quiz Management:**
   - Provide administrative interfaces for creating, updating, publishing, and deleting academic subjects and parameterized quizzes with configurable durations and passing benchmarks.
4. **Hierarchical Multiple-Choice Question Bank Architecture:**
   - Establish structured relational schemas supporting multiple options (A, B, C, D), correct option mapping, individual question marks allocation, and contextual solution explanations.
5. **Real-Time Interactive Examination Engine:**
   - Implement an interactive assessment interface with a persistent client-side JavaScript countdown timer synchronized with server-side duration constraints and automated submission triggers upon time exhaustion.
6. **Granular Diagnostic Review & Performance Archiving:**
   - Provide students with immediate post-test breakdowns highlighting correct answers, chosen selections, marked marks, and pedagogical explanations alongside an immutable chronological attempt history.
7. **Platform-Wide Performance Analytics for Administrators:**
   - Equip faculty and administrative staff with comprehensive dashboards visualizing registration metrics, quiz attempt distribution, overall pass rates, and candidate-specific historical performance logs.

---

## 5. Literature Review

The development of automated web assessment systems has been an active area of empirical research in Computer Science Education and Educational Technology.

```
+-------------------------------------------------------------------------------------------------------------+
|                                    COMPARATIVE LITERATURE MATRIX                                            |
+------------------------------+--------------------+-----------------------------+---------------------------+
| System / Literature Reference| Technology Stack   | Key Strengths               | Identified Research Gaps  |
+------------------------------+--------------------+-----------------------------+---------------------------+
| Traditional LMS              | PHP / MySQL /      | Comprehensive courseware    | High architectural bloat, |
| (e.g., Moodle, Blackboard)   | Modular Plugins    | and forum integration       | steep learning curve,     |
|                              |                    |                             | heavy server footprints.  |
+------------------------------+--------------------+-----------------------------+---------------------------+
| Standalone Desktop           | Java Swing /       | Local execution without     | Lacks cross-platform web  |
| Assessment Tools             | C++ / MS Access    | internet connectivity       | access, difficult update  |
|                              |                    |                             | and synchronization paths.|
+------------------------------+--------------------+-----------------------------+---------------------------+
| Commercial Cloud Quiz        | Proprietary SaaS / | High visual fidelity,       | Expensive subscription,   |
| Platforms (e.g., Quizizz)   | NoSQL / Cloud APIs | gamified interfaces         | lack of on-premise data   |
|                              |                    |                             | sovereignty, no offline DB|
+------------------------------+--------------------+-----------------------------+---------------------------+
| Proposed Online Quiz         | Python 3 / Django /| Lightweight, MVT pattern,   | Designed specifically for |
| System (Current Work)        | SQLite / Bootstrap | zero-configuration DB,      | high-performance academic |
|                              |                    | instantaneous auto-grading, | testing with full data    |
|                              |                    | deep diagnostic review.     | ownership and low latency.|
+------------------------------+--------------------+-----------------------------+---------------------------+
```

### 5.1 Analysis of Prior Approaches
- **Moodle & Canvas LMS:** While feature-dense, enterprise Learning Management Systems (LMS) introduce significant resource overhead, intricate navigational complexity for basic quizzes, and high configuration latency for small-to-medium academic institutions.
- **Microservices & Cloud SaaS Solutions:** Commercial solutions such as Google Forms or commercial quiz portals often lack fine-grained timer controls with enforced automated server-side submissions, store institutional assessment data on third-party cloud infrastructure without localized data governance, and frequently impose recurring licensing costs.
- **Django-Based Architectures:** Django’s built-in Object-Relational Mapper (ORM), Cross-Site Request Forgery (CSRF) protection, standardized cryptographic authentication, and clean Model-View-Template (MVT) modularity provide an optimal foundation for building a secure, rapid-response, low-latency examination system that balances performance, security, and computational simplicity.

---

## 6. Proposed Methodology

The implementation follows the **Model-View-Template (MVT)** architectural paradigm provided by Django, backed by a relational SQLite database and a modern, mobile-responsive Bootstrap 5 presentation layer.

```
                               +--------------------------------------------+
                               |              WEB CLIENT (BROWSER)          |
                               |    HTML5 + CSS3 + Bootstrap 5 + JS ES6     |
                               +---------------------+----------------------+
                                                     |  HTTP/HTTPS Requests
                                                     v
                               +--------------------------------------------+
                               |            DJANGO WEB SERVER (WSGI)        |
                               |         urls.py (URL Routing Engine)       |
                               +---------------------+----------------------+
                                                     |
                                                     v
                               +--------------------------------------------+
                               |               DJANGO VIEWS                 |
                               |  - auth_views.py  (Auth & Profile Logic)   |
                               |  - user_views.py  (Quiz Attempt Engine)    |
                               |  - admin_views.py (CRUD & Analytics Engine)|
                               +--------+--------------------------+--------+
                                        |                          |
               Business Logic / Models  |                          | Context Rendering
                                        v                          v
                        +-------------------------------+   +-------------------------------+
                        |       DJANGO ORM (MODELS)     |   |       DJANGO TEMPLATES        |
                        | - Subject     - QuizAttempt   |   | - base.html   - take_quiz.html|
                        | - Quiz        - UserAnswer    |   | - auth/*.html - result_detail |
                        | - Question                    |   | - admin_panel/*.html          |
                        +---------------+---------------+   +-------------------------------+
                                        |
                                        v SQL Queries
                        +-------------------------------+
                        |       SQLITE 3 DATABASE       |
                        |  (db.sqlite3 Relational Store)|
                        +-------------------------------+
```

### 6.1 System Architecture & Design Patterns
1. **Model (Data Layer):** Implemented in `quiz_app/models.py`. Manages relational integrity across subjects, quizzes, questions, attempts, and individual answer selections using Django ORM.
2. **View (Business Logic & Controllers):** Implemented in modular view controllers (`auth_views.py`, `user_views.py`, `admin_views.py`) to process user input, enforce security policies, orchestrate grading algorithms, and query the ORM.
3. **Template (Presentation Layer):** Built with semantic HTML5, custom CSS3 stylesheets, Bootstrap 5 UI widgets, and dynamic Django Template Language (DTL) tags for dynamic content rendering.

---

### 6.2 Relational Database Schema & Data Models

```
+-----------------------------------------------------------------------------------------------+
|                                    DATABASE ENTITY SCHEMA                                     |
+-------------------+---------------------------------------------------------------------------+
| Entity / Model    | Fields, Data Types & Constraints                                          |
+-------------------+---------------------------------------------------------------------------+
| User              | id (PK, Auto), username (Varchar, Unique), email (EmailField, Unique),   |
| (Django Built-in) | password (Varchar Hashed), first_name, last_name, is_staff, date_joined    |
+-------------------+---------------------------------------------------------------------------+
| Subject           | id (PK, Auto), name (Varchar 120, Unique), description (TextField),       |
|                   | icon (Varchar 50), created_at (DateTime), updated_at (DateTime)           |
+-------------------+---------------------------------------------------------------------------+
| Quiz              | id (PK, Auto), subject_id (FK -> Subject), title (Varchar 200),           |
|                   | description (TextField), duration_minutes (PositiveInt),                  |
|                   | pass_percentage (PositiveInt), is_published (Boolean), created_at         |
+-------------------+---------------------------------------------------------------------------+
| Question          | id (PK, Auto), quiz_id (FK -> Quiz), question_text (TextField),           |
|                   | option_a, option_b, option_c, option_d (Varchar 300),                     |
|                   | correct_option (Char 1: 'A'/'B'/'C'/'D'), marks (PositiveInt),            |
|                   | explanation (TextField), created_at (DateTime)                            |
+-------------------+---------------------------------------------------------------------------+
| QuizAttempt       | id (PK, Auto), user_id (FK -> User), quiz_id (FK -> Quiz),                |
|                   | score (Float), total_score (Float), percentage (Float), passed (Boolean), |
|                   | correct_count (Int), incorrect_count (Int), unanswered_count (Int),       |
|                   | time_taken_seconds (Int), completed_at (DateTime)                         |
+-------------------+---------------------------------------------------------------------------+
| UserAnswer        | id (PK, Auto), attempt_id (FK -> QuizAttempt),                            |
|                   | question_id (FK -> Question), selected_option (Char 1 Nullable),          |
|                   | is_correct (Boolean), marks_obtained (Float)                              |
+-------------------+---------------------------------------------------------------------------+
```

---

### 6.3 User Module Workflow
1. **Authentication & Profile Cycle:** Unauthenticated users register with email verification and log in. Authenticated students update personal names, email identifiers, and change passwords with session preservation.
2. **Subject & Quiz Discovery:** The student dashboard presents categorized subjects with active quiz counters, live search filters, and overview cards detailing duration, total marks, question counts, and past personal best scores.
3. **Live Timed Quiz Engine:**
   - Navigating to `/quiz/<id>/take/` starts the countdown timer initialized with `duration_minutes * 60` seconds.
   - Questions display interactive radio selector cards styled for mobile and desktop screens.
   - The JavaScript timer actively counts down, triggers visual alerts when `time_remaining <= 60s`, and initiates automatic form submission if the timer reaches zero.
   - Client-side navigation guards (`beforeunload` event listeners) prevent accidental page exits or accidental progress abandonment.
4. **Instant Diagnostic Review & Historical Log:**
   - Immediate redirect to `/results/<attempt_id>/` showcasing performance cards (Marks, Percentage, Status Badge, Time Elapsed).
   - Question-by-question review displaying the student's selected option alongside highlighted correct answer keys and educational explanations.
   - Historical log table at `/history/` summarizing all previous attempts with timestamps and direct review links.

---

### 6.4 Admin Module Workflow
1. **Administrative KPI Dashboard:** Displays global system metrics: Total Subjects, Quizzes, Questions, Registered Students, Total Attempts, Platform Pass Rates, and live activity streams.
2. **Subject Management (CRUD):** Add, modify, inspect, or delete subject categories linked with Bootstrap icons.
3. **Quiz Management (CRUD):** Define exam title, instructions, subject association, duration limits, passing percentage benchmarks, and publication visibility.
4. **Question Bank Management (CRUD):** Author multiple-choice questions, configure options A through D, map the correct answer key, assign numerical marks, and attach solution rationale. Supports a rapid "Save and Add Another" authoring workflow.
5. **User Management & Examination History:** Inspect registered student profiles, review their individual test histories, and manage user accounts with self-deletion safeguards.
6. **Comprehensive Analytics & Result Reporting:** Filter platform-wide quiz attempt records by quiz title, student name, and pass/fail status with immediate deep-dive drill-downs.

---

### 6.5 Scoring and Evaluation Engine Logic

```python
# Pseudocode representation of the Auto-Evaluation Engine
def evaluate_quiz_submission(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_published=True)
    questions = quiz.questions.all()
    
    total_marks_possible = 0
    total_score_obtained = 0
    correct_count = 0
    incorrect_count = 0
    unanswered_count = 0
    
    user_answers = []
    
    for question in questions:
        total_marks_possible += question.marks
        user_choice = request.POST.get(f"question_{question.id}", "").strip()
        
        if not user_choice:
            unanswered_count += 1
            is_corr = False
            marks = 0
            user_choice = None
        elif user_choice == question.correct_option:
            correct_count += 1
            is_corr = True
            marks = question.marks
            total_score_obtained += marks
        else:
            incorrect_count += 1
            is_corr = False
            marks = 0
            
        user_answers.append(UserAnswer(
            question=question,
            selected_option=user_choice,
            is_correct=is_corr,
            marks_obtained=marks
        ))
        
    percentage = (total_score_obtained / total_marks_possible) * 100
    passed = percentage >= quiz.pass_percentage
    
    # Persist attempt and bulk-insert individual user answers
    attempt = QuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        score=total_score_obtained,
        total_score=total_marks_possible,
        percentage=round(percentage, 2),
        passed=passed,
        correct_count=correct_count,
        incorrect_count=incorrect_count,
        unanswered_count=unanswered_count,
        time_taken_seconds=int(request.POST.get('time_taken_seconds', 0))
    )
    for ua in user_answers:
        ua.attempt = attempt
    UserAnswer.objects.bulk_create(user_answers)
    
    return redirect('result_detail', attempt_id=attempt.id)
```

---

## 7. Dataset / Tools & Technologies

### 7.1 Software Specification
- **Programming Language:** Python 3.12+ (Object-Oriented, Dynamic Typing)
- **Web Framework:** Django 5.x (High-level Python Web Framework with MVT pattern)
- **Database Engine:** SQLite 3 (ACID-compliant relational database engine)
- **Frontend Technologies:**
  - Semantic HTML5 & CSS3
  - Bootstrap 5.3.3 (Responsive Grid & Component UI)
  - Bootstrap Icons 1.11.3 (Vector Iconography)
  - Vanilla JavaScript ES6+ (DOM Manipulation, Live Timer, Event Listeners)
  - Google Fonts (Plus Jakarta Sans Typography)
- **Operating System Compatibility:** Cross-Platform (Linux / macOS / Microsoft Windows 10/11)
- **Development & Version Control Tools:** Visual Studio Code / Antigravity IDE, Git, GitHub, PIP Package Manager

### 7.2 Hardware Specifications

```
+-----------------------------------------------------------------------------------------------+
|                                    HARDWARE REQUIREMENTS                                      |
+---------------------+-----------------------------------+-------------------------------------+
| Parameter           | Minimum Specification             | Recommended Specification           |
+---------------------+-----------------------------------+-------------------------------------+
| Processor (Server)  | Dual-Core CPU @ 2.0 GHz           | Quad-Core Intel Core i5/i7 / Ryzen 5|
| System Memory (RAM) | 2 GB RAM                          | 8 GB DDR4/DDR5 RAM                  |
| Storage Space       | 1 GB available disk space         | 50 GB NVMe Solid State Drive (SSD)  |
| Client Device       | Any modern PC, Tablet, Smartphone | Desktop / Laptop with 1080p Display |
| Network Connection  | Broadband / 4G (1 Mbps download)  | High-Speed Internet (10+ Mbps)      |
+---------------------+-----------------------------------+-------------------------------------+
```

---

## 8. Expected Results & Applications

### 8.1 Anticipated Outcomes & Usability Improvements
1. **Zero-Latency Grading:** Complete eradication of manual paper evaluation delays; comprehensive result calculation executed instantaneously upon test submission.
2. **Complete Data Integrity and Security:** Encrypted credential protection, automated CSRF verification across POST payloads, and strict role segregation eliminating unauthorized exam tampering.
3. **Enhanced Pedagogical Diagnostics:** Real-time visibility into correct solutions, chosen alternatives, and educational rationale fostering formative assessment self-improvement.
4. **Administrative Productivity:** Accelerated test generation, flexible question banking, and simplified metric extraction through unified management dashboards.

### 8.2 Real-World Application Scenarios
- **Higher Education Institutions & Universities:** Conducting internal sessional assessments, mid-term online quizzes, departmental mock tests, and tutorial evaluations.
- **Competitive Coaching & Test-Prep Centers:** Administering high-frequency practice exams for competitive engineering, medical, and civil services assessments.
- **Corporate Training & Human Resource Onboarding:** Conducting technical onboarding evaluations, compliance comprehension assessments, and employee skill verification tests.

---

## 9. Gantt Chart (Project Implementation Timeline)

The following multi-week project implementation schedule delineates the key phases, milestones, and task deliverables from initial requirement elicitation to final system deployment:

```
+----+------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| ID | Phase / Project Task Name          | W01 | W02 | W03 | W04 | W05 | W06 | W07 | W08 | W09 | W10 | W11 | W12 |
+----+------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 1  | Requirement Analysis & Feasibility | [X] | [X] |     |     |     |     |     |     |     |     |     |     |
| 2  | Database Schema & Relational Design|     | [X] | [X] |     |     |     |     |     |     |     |     |     |
| 3  | Auth & Access Control Module       |     |     | [X] | [X] |     |     |     |     |     |     |     |     |
| 4  | Admin Management CRUD Module       |     |     |     | [X] | [X] | [X] |     |     |     |     |     |     |
| 5  | User Dashboard & Quiz Engine UI    |     |     |     |     | [X] | [X] | [X] |     |     |     |     |     |
| 6  | Timer Logic & Auto-Grading Engine  |     |     |     |     |     |     | [X] | [X] |     |     |     |     |
| 7  | Diagnostic Review & History Module |     |     |     |     |     |     |     | [X] | [X] |     |     |     |
| 8  | Integration & Automated Unit Tests |     |     |     |     |     |     |     |     | [X] | [X] |     |     |
| 9  | System Deployment & Final Tuning   |     |     |     |     |     |     |     |     |     |     | [X] |     |
| 10 | Documentation & Final Presentation |     |     |     |     |     |     |     |     |     |     | [X] | [X] |
+----+------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
```

---

## 10. References

1. A. Holovaty and J. Kaplan-Moss, *The Definitive Guide to Django: Web Development Done Right*, 2nd ed. New York, NY, USA: Apress, 2009.
2. D. Higgins, "Computer-Based Assessment: A review of current practices and future potential in higher education," *IEEE Transactions on Learning Technologies*, vol. 12, no. 3, pp. 312–324, Jul.–Sep. 2019.
3. R. S. Pressman and B. R. Maxim, *Software Engineering: A Practitioner's Approach*, 9th ed. New York, NY, USA: McGraw-Hill Education, 2020.
4. M. D. R. Ramos, P. A. C. Silva, and E. S. Ferreira, "Design and Evaluation of Web-Based Automated Multiple Choice Assessment Systems," in *Proc. IEEE Global Engineering Education Conference (EDUCON)*, Porto, Portugal, 2021, pp. 784–791.
5. V. Bushuev, K. Morozov, and T. Popova, "Architecture and Security Considerations for Web-Based Testing Engines in Higher Education," *IEEE Access*, vol. 9, pp. 104250–104261, 2021.
6. P. Spachos, L. Liang, and K. N. Plataniotis, "Wireless and Web-Based Automated Assessment Infrastructure for Remote Educational Environments," *IEEE Transactions on Education*, vol. 64, no. 4, pp. 389–397, Nov. 2021.
7. J. Owens, *SQLite Database System: Design and Implementation*, 2nd ed. Boston, MA, USA: Sibsatis Press, 2020.
8. M. Otto and J. Thornton, *Bootstrap: Responsive Web Framework Documentation and Design Specifications*, San Francisco, CA, USA: GitHub Inc., 2024.

---

```
========================================================================================
                          END OF PROJECT SYNOPSIS REPORT
========================================================================================
```
