from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Quiz, QuizAttempt, Student, QuizResult
from .forms import StudentRegisterForm
from .ml_model.predict_feedback import get_feedback, generate_feedback_text
import json

# ✅ HOME PAGE
def home(request):
    return render(request, 'tutorapp/home.html')

# ✅ QUIZ VIEW - Random 5 questions from any topic
@login_required
def quiz_view(request):
    if not hasattr(request.user, 'student'):
        Student.objects.create(
            user=request.user,
            name=request.user.username,
            email=request.user.email or f"{request.user.username}@example.com"
        )

    student = request.user.student

    if request.method == 'POST':
        question_ids = request.POST.getlist('question_ids')
        score = 0
        unanswered = False
        topic_summary = {}

        for qid in question_ids:
            try:
                question = Quiz.objects.get(id=int(qid))
            except Quiz.DoesNotExist:
                continue

            selected_option = request.POST.get(str(qid))
            if selected_option is None:
                unanswered = True
                continue

            is_correct = selected_option == question.correct_option

            QuizAttempt.objects.create(
                student=student,
                quiz=question,
                selected_option=selected_option,
                is_correct=is_correct
            )

            topic = question.topic
            if topic not in topic_summary:
                topic_summary[topic] = {'correct': 0, 'total': 0}
            topic_summary[topic]['total'] += 1
            if is_correct:
                topic_summary[topic]['correct'] += 1
                score += 1

        if unanswered:
            questions = Quiz.objects.filter(id__in=question_ids)
            return render(request, 'tutorapp/quiz.html', {
                'questions': questions,
                'error': "Please answer all questions before submitting."
            })

        percentage = (score / len(question_ids)) * 100
        feedback = get_feedback(percentage)

        topic_feedback = {}
        topic_strength = {}
        for topic, val in topic_summary.items():
            acc = val['correct'] / val['total'] if val['total'] > 0 else 0
            topic_feedback[topic] = 'Strong' if acc >= 0.6 else 'Weak'
            topic_strength[topic] = round(acc, 2)

        QuizResult.objects.create(
            student=student,
            score=score,
            total_questions=len(question_ids),
            percentage=percentage,
            feedback=feedback
        )

        return render(request, 'tutorapp/feedback.html', {
            'score': score,
            'total': len(question_ids),
            'percentage': percentage,
            'feedback': feedback,
            'topic_feedback': topic_feedback,
            'topic_strength': json.dumps(topic_strength) if topic_strength else json.dumps({})
        })

    else:
        questions = Quiz.objects.order_by('?')[:5]
        return render(request, 'tutorapp/quiz.html', {'questions': questions})

# ✅ TOPIC QUIZ VIEW - Based on selected topic
@login_required
def topic_quiz_view(request):
    student = request.user.student
    selected_topic = request.GET.get('topic')

    if not selected_topic:
        return redirect('home')

    questions = Quiz.objects.filter(topic=selected_topic).order_by('?')[:5]

    if request.method == 'POST':
        score = 0
        unanswered = False
        topic_summary = {}

        for question in questions:
            selected_option = request.POST.get(str(question.id))

            if not selected_option:
                unanswered = True
                continue  # skip rest for this question

            is_correct = selected_option == question.correct_option

            QuizAttempt.objects.create(
                student=student,
                quiz=question,
                selected_option=selected_option,
                is_correct=is_correct
            )

            topic = question.topic
            if topic not in topic_summary:
                topic_summary[topic] = {'correct': 0, 'total': 0}
            topic_summary[topic]['total'] += 1
            if is_correct:
                topic_summary[topic]['correct'] += 1
                score += 1

        if unanswered:
            return render(request, 'tutorapp/topic_quiz.html', {
                'questions': questions,
                'selected_topic': selected_topic,
                'error': "Please answer all questions before submitting."
            })

        percentage = (score / len(questions)) * 100
        feedback = get_feedback(percentage)

        topic_feedback = {}
        topic_strength = {}
        for topic, val in topic_summary.items():
            acc = val['correct'] / val['total'] if val['total'] > 0 else 0
            topic_feedback[topic] = 'Strong' if acc >= 0.6 else 'Weak'
            topic_strength[topic] = round(acc, 2)

        QuizResult.objects.create(
            student=student,
            score=score,
            total_questions=len(questions),
            percentage=percentage,
            feedback=feedback
        )

        return render(request, 'tutorapp/feedback.html', {
            'score': score,
            'total': len(questions),
            'percentage': percentage,
            'feedback': feedback,
            'topic_feedback': topic_feedback,
            'topic_strength': json.dumps(topic_strength) if topic_strength else json.dumps({})
        })

    return render(request, 'tutorapp/topic_quiz.html', {
        'questions': questions,
        'selected_topic': selected_topic
    })


# ✅ STUDENT REGISTER
def register_view(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Student.objects.create(user=user, name=user.username, email=user.email)
            return redirect('login')
    else:
        form = StudentRegisterForm()
    return render(request, 'tutorapp/register.html', {'form': form})

# ✅ LOGIN
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('quiz')
    return render(request, 'tutorapp/login.html')

# ✅ LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')

# ✅ ADMIN DASHBOARD
def admin_dashboard(request):
    total_users = User.objects.count()
    total_students = Student.objects.count()
    total_quizzes = QuizAttempt.objects.count()
    total_score = sum([student.total_score for student in Student.objects.all()])

    average_score = (total_score / total_quizzes) if total_quizzes > 0 else 0
    top_students = Student.objects.order_by('-total_score')[:5]

    context = {
        'total_users': total_users,
        'total_students': total_students,
        'total_quizzes': total_quizzes,
        'average_score': round(average_score, 2),
        'top_students': top_students,
    }
    return render(request, 'tutorapp/admin_dashboard.html', context)
