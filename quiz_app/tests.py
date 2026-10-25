from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from quiz_app.models import Subject, Quiz, Question, QuizAttempt, UserAnswer


class QuizSystemTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create Admin and Regular Student User
        self.admin_user = User.objects.create_user(
            username='testadmin',
            email='admin@test.com',
            password='password123',
            is_staff=True,
            is_superuser=True
        )

        self.student_user = User.objects.create_user(
            username='teststudent',
            email='student@test.com',
            password='password123',
            is_staff=False
        )

        # Create Subject
        self.subject = Subject.objects.create(
            name='Computer Science',
            description='Fundamentals of CS',
            icon='bi-laptop'
        )

        # Create Quiz
        self.quiz = Quiz.objects.create(
            subject=self.subject,
            title='CS Basics',
            description='Test your CS fundamentals',
            duration_minutes=15,
            pass_percentage=50,
            is_published=True
        )

        # Create Questions
        self.q1 = Question.objects.create(
            quiz=self.quiz,
            question_text='What is 2 + 2?',
            option_a='3',
            option_b='4',
            option_c='5',
            option_d='6',
            correct_option='B',
            marks=1,
            explanation='2 + 2 equals 4.'
        )

        self.q2 = Question.objects.create(
            quiz=self.quiz,
            question_text='Which is a boolean value?',
            option_a='True',
            option_b='Hello',
            option_c='123',
            option_d='None of the above',
            correct_option='A',
            marks=1,
            explanation='True is a boolean value.'
        )

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newstudent',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newstudent').exists())

    def test_user_login_and_redirect(self):
        response = self.client.post(reverse('login'), {
            'username': 'teststudent',
            'password': 'password123'
        })
        self.assertRedirects(response, reverse('user_dashboard'))

    def test_admin_login_and_redirect(self):
        response = self.client.post(reverse('login'), {
            'username': 'testadmin',
            'password': 'password123'
        })
        self.assertRedirects(response, reverse('admin_dashboard'))

    def test_admin_access_control_for_students(self):
        self.client.login(username='teststudent', password='password123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertRedirects(response, reverse('user_dashboard'))

    def test_admin_can_access_admin_dashboard(self):
        self.client.login(username='testadmin', password='password123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Platform Overview & Management')

    def test_quiz_submission_and_evaluation(self):
        self.client.login(username='teststudent', password='password123')
        
        # Submit answers: q1 correct ('B'), q2 incorrect ('C')
        post_data = {
            f'question_{self.q1.id}': 'B',
            f'question_{self.q2.id}': 'C',
            'time_taken_seconds': 45
        }
        response = self.client.post(reverse('submit_quiz', kwargs={'quiz_id': self.quiz.id}), post_data)
        
        attempt = QuizAttempt.objects.filter(user=self.student_user, quiz=self.quiz).first()
        self.assertIsNotNone(attempt)
        self.assertRedirects(response, reverse('result_detail', kwargs={'attempt_id': attempt.id}))
        
        # Verify calculated values
        self.assertEqual(attempt.score, 1.0)
        self.assertEqual(attempt.total_score, 2.0)
        self.assertEqual(attempt.percentage, 50.0)
        self.assertTrue(attempt.passed)
        self.assertEqual(attempt.correct_count, 1)
        self.assertEqual(attempt.incorrect_count, 1)

    def test_subject_crud_admin(self):
        self.client.login(username='testadmin', password='password123')
        
        # Create Subject
        response = self.client.post(reverse('admin_subject_create'), {
            'name': 'Mathematics',
            'description': 'Math Quiz Category',
            'icon': 'bi-calculator'
        })
        self.assertRedirects(response, reverse('admin_subject_list'))
        self.assertTrue(Subject.objects.filter(name='Mathematics').exists())

    def test_quiz_crud_admin(self):
        self.client.login(username='testadmin', password='password123')
        
        # Create Quiz
        response = self.client.post(reverse('admin_quiz_create'), {
            'subject': self.subject.id,
            'title': 'Advanced Algorithms',
            'description': 'Sorting, graphs, recursion',
            'duration_minutes': 20,
            'pass_percentage': 70,
            'is_published': True
        })
        new_quiz = Quiz.objects.filter(title='Advanced Algorithms').first()
        self.assertIsNotNone(new_quiz)
        self.assertRedirects(response, reverse('admin_question_list_by_quiz', kwargs={'quiz_id': new_quiz.id}))

    def test_question_crud_admin(self):
        self.client.login(username='testadmin', password='password123')
        
        # Create Question
        response = self.client.post(reverse('admin_question_create'), {
            'quiz': self.quiz.id,
            'question_text': 'What does HTML stand for?',
            'option_a': 'Hyper Text Markup Language',
            'option_b': 'High Tech Modern Language',
            'option_c': 'Hyperlink Text Module',
            'option_d': 'Home Tool Markup Language',
            'correct_option': 'A',
            'marks': 2,
            'explanation': 'HTML stands for Hyper Text Markup Language.'
        })
        self.assertRedirects(response, reverse('admin_question_list_by_quiz', kwargs={'quiz_id': self.quiz.id}))
        self.assertTrue(Question.objects.filter(question_text__contains='HTML').exists())

    def test_user_history_view(self):
        self.client.login(username='teststudent', password='password123')
        
        # Create an attempt
        attempt = QuizAttempt.objects.create(
            user=self.student_user,
            quiz=self.quiz,
            score=2.0,
            total_score=2.0,
            percentage=100.0,
            passed=True,
            correct_count=2
        )
        
        response = self.client.get(reverse('quiz_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CS Basics')
        self.assertContains(response, '100.0%')

    def test_admin_cannot_delete_self(self):
        self.client.login(username='testadmin', password='password123')
        response = self.client.post(reverse('admin_user_delete', kwargs={'user_id': self.admin_user.id}))
        self.assertRedirects(response, reverse('admin_user_list'))
        # Admin user still exists
        self.assertTrue(User.objects.filter(id=self.admin_user.id).exists())
