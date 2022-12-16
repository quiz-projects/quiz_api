from django.urls import path
from .views import QuizListView, QuestionListView, TopicListView

urlpatterns = [
    path('quiz/', QuizListView.as_view()),
    path('topic/', TopicListView.as_view()),
    path('topic/<int:pk>/', TopicListView.as_view()),
    path('quiz/<int:pk>/', QuestionListView.as_view()),
]