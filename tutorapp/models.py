from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    total_quizzes = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    roll_number = models.CharField(max_length=20, default="N/A")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    TOPIC_CHOICES = [
        ("Python", "Python"),
        ("Maths", "Maths"),
        ("AI", "AI"),
        ("DBMS", "DBMS"),
        ("ML", "ML"),
        ("DSA", "DSA"),
    ]

    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, default='A')  # A, B, C, D me se
    topic = models.CharField(max_length=100, choices=TOPIC_CHOICES, default='Python')

    def __str__(self):
        return f"{self.question[:50]}..."  # pehle 50 chars dikha dega

    @property
    def get_options(self):
        """Template ke liye options ko list me dega, jisse template me loop kar sako."""
        return [
            f"A) {self.option_a}",
            f"B) {self.option_b}",
            f"C) {self.option_c}",
            f"D) {self.option_d}",
        ]


class QuizAttempt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, null=True, blank=True)  # ✅ ye null rehne do
    selected_option = models.CharField(max_length=255)
    is_correct = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    feedback_text = models.TextField(null=True, blank=True)

    @property
    def topic(self):
        return self.quiz.topic if self.quiz else 'General'


class QuizResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    percentage = models.FloatField()
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.score}/{self.total_questions}"


@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance, name=instance.username, email=instance.email)