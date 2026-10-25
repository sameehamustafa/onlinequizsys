import os
import django

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from django.contrib.auth.models import User
from quiz_app.models import Subject, Quiz, Question, QuizAttempt, UserAnswer


def seed():
    print("🚀 Seeding Quizify Database...")

    # 1. Create Superuser (Admin)
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@quizify.io',
            'first_name': 'System',
            'last_name': 'Administrator',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created or not admin_user.check_password('admin123'):
        admin_user.set_password('admin123')
        admin_user.save()
        print("✅ Superuser 'admin' created (Password: admin123)")
    else:
        print("ℹ️ Superuser 'admin' already exists.")

    # 2. Create Student User
    student_user, created = User.objects.get_or_create(
        username='student',
        defaults={
            'email': 'student@quizify.io',
            'first_name': 'Alex',
            'last_name': 'Morgan',
            'is_staff': False,
            'is_superuser': False,
        }
    )
    if created or not student_user.check_password('student123'):
        student_user.set_password('student123')
        student_user.save()
        print("✅ Student user 'student' created (Password: student123)")
    else:
        print("ℹ️ Student user 'student' already exists.")

    # 3. Create Subjects
    sub_python, _ = Subject.objects.get_or_create(
        name="Python Programming",
        defaults={
            'description': "Core Python syntax, data structures, OOP concepts, and standard library modules.",
            'icon': "bi-filetype-py"
        }
    )

    sub_web, _ = Subject.objects.get_or_create(
        name="Web Development",
        defaults={
            'description': "Frontend & Backend fundamentals including HTML5, CSS3, JavaScript, HTTP protocol, and RESTful APIs.",
            'icon': "bi-globe"
        }
    )

    sub_db, _ = Subject.objects.get_or_create(
        name="Database Management",
        defaults={
            'description': "Relational database concepts, SQL queries, normalization, indexing, and SQLite/PostgreSQL.",
            'icon': "bi-database"
        }
    )
    print("✅ Subjects created.")

    # 4. Create Quizzes & Questions
    
    # --- QUIZ 1: Python Fundamentals ---
    quiz_py1, _ = Quiz.objects.get_or_create(
        title="Python Fundamentals & Data Structures",
        subject=sub_python,
        defaults={
            'description': "Test your grasp on Python variables, lists, dictionaries, tuples, loops, and functions.",
            'duration_minutes': 10,
            'pass_percentage': 60,
            'is_published': True
        }
    )

    py_questions = [
        {
            'text': "Which of the following data types in Python is immutable?",
            'a': "List",
            'b': "Dictionary",
            'c': "Tuple",
            'd': "Set",
            'correct': "C",
            'marks': 1,
            'explanation': "Tuples in Python cannot be modified once created, making them immutable. Lists, sets, and dictionaries are mutable."
        },
        {
            'text': "What is the output of `bool([])` in Python?",
            'a': "True",
            'b': "False",
            'c': "None",
            'd': "TypeError",
            'correct': "B",
            'marks': 1,
            'explanation': "An empty list has a falsy boolean value in Python, so `bool([])` evaluates to False."
        },
        {
            'text': "Which built-in function returns both index and item while iterating over an iterable?",
            'a': "range()",
            'b': "zip()",
            'c': "enumerate()",
            'd': "map()",
            'correct': "C",
            'marks': 1,
            'explanation': "The `enumerate()` function adds a counter to an iterable and returns it as an enumerate object yielding (index, item) pairs."
        },
        {
            'text': "What does the `__init__` method represent in Python classes?",
            'a': "Class Destructor",
            'b': "Instance Initializer (Constructor)",
            'c': "Static Method",
            'd': "String Representation",
            'correct': "B",
            'marks': 1,
            'explanation': "`__init__` is the initializer method called automatically when a new instance of a class is created."
        },
        {
            'text': "How do you handle exceptions in Python?",
            'a': "try...catch",
            'b': "try...except",
            'c': "do...rescue",
            'd': "try...error",
            'correct': "B",
            'marks': 1,
            'explanation': "Python uses the `try...except...finally` block structure for error and exception handling."
        }
    ]

    for q_data in py_questions:
        Question.objects.get_or_create(
            quiz=quiz_py1,
            question_text=q_data['text'],
            defaults={
                'option_a': q_data['a'],
                'option_b': q_data['b'],
                'option_c': q_data['c'],
                'option_d': q_data['d'],
                'correct_option': q_data['correct'],
                'marks': q_data['marks'],
                'explanation': q_data['explanation']
            }
        )

    # --- QUIZ 2: Web Development & JavaScript ---
    quiz_web1, _ = Quiz.objects.get_or_create(
        title="Modern Web Development Essentials",
        subject=sub_web,
        defaults={
            'description': "Covers HTML5 semantic tags, CSS Box Model, JavaScript ES6 features, and HTTP methods.",
            'duration_minutes': 8,
            'pass_percentage': 50,
            'is_published': True
        }
    )

    web_questions = [
        {
            'text': "Which HTTP method is idempotent and primarily used to fetch resources from a server?",
            'a': "POST",
            'b': "GET",
            'c': "PATCH",
            'd': "CONNECT",
            'correct': "B",
            'marks': 1,
            'explanation': "GET requests are safe and idempotent; their sole purpose is to retrieve representations of resources."
        },
        {
            'text': "In CSS, what is the default value of the `position` property?",
            'a': "relative",
            'b': "absolute",
            'c': "static",
            'd': "fixed",
            'correct': "C",
            'marks': 1,
            'explanation': "HTML elements are positioned static by default; they are positioned according to the normal flow of the page."
        },
        {
            'text': "Which keyword declares a block-scoped variable that cannot be reassigned in JavaScript?",
            'a': "var",
            'b': "let",
            'c': "const",
            'd': "def",
            'correct': "C",
            'marks': 1,
            'explanation': "`const` declares a block-scoped variable whose identifier cannot be reassigned."
        },
        {
            'text': "Which HTML5 semantic element should encapsulate autonomous, self-contained composition?",
            'a': "<section>",
            'b': "<article>",
            'c': "<div>",
            'd': "<aside>",
            'correct': "B",
            'marks': 1,
            'explanation': "The `<article>` tag specifies independent, self-contained content such as a blog post or news story."
        }
    ]

    for q_data in web_questions:
        Question.objects.get_or_create(
            quiz=quiz_web1,
            question_text=q_data['text'],
            defaults={
                'option_a': q_data['a'],
                'option_b': q_data['b'],
                'option_c': q_data['c'],
                'option_d': q_data['d'],
                'correct_option': q_data['correct'],
                'marks': q_data['marks'],
                'explanation': q_data['explanation']
            }
        )

    # --- QUIZ 3: SQL & Database Design ---
    quiz_db1, _ = Quiz.objects.get_or_create(
        title="SQL Queries & Relational Database Design",
        subject=sub_db,
        defaults={
            'description': "Assess your skills on SQL queries, JOIN operations, primary/foreign keys, and aggregation.",
            'duration_minutes': 10,
            'pass_percentage': 60,
            'is_published': True
        }
    )

    db_questions = [
        {
            'text': "Which SQL clause is used to filter groups returned by a GROUP BY clause?",
            'a': "WHERE",
            'b': "HAVING",
            'c': "ORDER BY",
            'd': "LIMIT",
            'correct': "B",
            'marks': 1,
            'explanation': "`HAVING` filters aggregated records resulting from `GROUP BY`, whereas `WHERE` filters rows before grouping."
        },
        {
            'text': "Which type of JOIN returns all records when there is a match in either left or right table?",
            'a': "INNER JOIN",
            'b': "LEFT JOIN",
            'c': "FULL OUTER JOIN",
            'd': "CROSS JOIN",
            'correct': "C",
            'marks': 1,
            'explanation': "`FULL OUTER JOIN` combines the results of both LEFT and RIGHT joins, returning all matched and unmatched rows from both tables."
        },
        {
            'text': "What constraint uniquely identifies each record in a database table?",
            'a': "FOREIGN KEY",
            'b': "CHECK",
            'c': "PRIMARY KEY",
            'd': "DEFAULT",
            'correct': "C",
            'marks': 1,
            'explanation': "A PRIMARY KEY constraint uniquely identifies each row in a table and cannot contain NULL values."
        }
    ]

    for q_data in db_questions:
        Question.objects.get_or_create(
            quiz=quiz_db1,
            question_text=q_data['text'],
            defaults={
                'option_a': q_data['a'],
                'option_b': q_data['b'],
                'option_c': q_data['c'],
                'option_d': q_data['d'],
                'correct_option': q_data['correct'],
                'marks': q_data['marks'],
                'explanation': q_data['explanation']
            }
        )

    print("✅ Quizzes and Questions created.")

    # 5. Seed a Sample Attempt for the Student
    if not QuizAttempt.objects.filter(user=student_user, quiz=quiz_py1).exists():
        attempt = QuizAttempt.objects.create(
            user=student_user,
            quiz=quiz_py1,
            score=4.0,
            total_score=5.0,
            percentage=80.0,
            passed=True,
            correct_count=4,
            incorrect_count=1,
            unanswered_count=0,
            time_taken_seconds=142
        )
        questions = quiz_py1.questions.all()
        for idx, q in enumerate(questions):
            # simulate 1 incorrect
            chosen = q.correct_option if idx != 1 else ('A' if q.correct_option != 'A' else 'B')
            is_corr = chosen == q.correct_option
            UserAnswer.objects.create(
                attempt=attempt,
                question=q,
                selected_option=chosen,
                is_correct=is_corr,
                marks_obtained=q.marks if is_corr else 0
            )
        print("✅ Sample quiz attempt created for user 'student'.")

    print("\n🎉 Database Seeding Completed Successfully!")
    print("--------------------------------------------------")
    print("🔑 Login Credentials:")
    print("   Admin Account   : username = admin   | password = admin123")
    print("   Student Account : username = student | password = student123")
    print("--------------------------------------------------")


if __name__ == '__main__':
    seed()
