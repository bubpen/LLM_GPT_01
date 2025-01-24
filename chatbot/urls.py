from django.urls import path
from . import views

app_name = 'chatbot'
urlpatterns = [
    path('', views.question_list, name = 'question_list'),
    path('question/', views.question, name = 'question'),
    path('question/<int:pk>/', views.answer, name = 'answer'),
]
