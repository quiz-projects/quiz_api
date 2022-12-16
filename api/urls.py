from django.urls import path
from .views import QuizListView, QuestionListView, TopicListView, OptionListView

urlpatterns = [
    path('quiz/', QuizListView.as_view()),
    path('topic/', TopicListView.as_view()),
    path('topic/<int:pk>/', TopicListView.as_view()),
    path('question/', QuestionListView.as_view()),
    path('question/<int:pk>/', QuestionListView.as_view()),
    path('option/', OptionListView.as_view()),
]