from django.urls import path
from .views import QuizListView, QuestionListView

urlpatterns = [
    path('quiz/', QuizListView.as_view()),
    path('quiz/<int:pk>/', QuestionListView.as_view()),
]