from django.contrib import admin
from .models import  Student, QuizAttempt, Course, QuizResult, Quiz

# Register your models here
admin.site.register(Student)      
admin.site.register(QuizAttempt)  
admin.site.register(Course)
admin.site.register(QuizResult)

# Register Quiz only once with custom admin class
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['question', 'topic']
