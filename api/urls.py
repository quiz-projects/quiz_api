from django.urls import path
from .views import (
    QuizListView,
    QuestionListView,
    TopicListView,
    OptionListView
)

urlpatterns = [
    path('quiz/', QuizListView.as_view()),
    path('topic/<int:quiz_id>/', TopicListView.as_view()),
    path('question/<int:topic_id>/', QuestionListView.as_view()),
    path('option/<int:question_id>/', OptionListView.as_view()),
]