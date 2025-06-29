from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('topic-quiz/', views.topic_quiz_view, name='topic_quiz'),
]
