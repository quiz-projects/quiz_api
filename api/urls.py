from django.urls import path
from .views import (
    QuizListView,
    QuestionListView,
    TopicListView,
    OptionListView,
    CheckAnswerView,
    StudentListView,
)

urlpatterns = [
    path('student/', StudentListView.as_view()),
    path('student/<int:pk>/', StudentListView.as_view()),
    path('quiz/', QuizListView.as_view()),
    path('topic/<int:quiz_id>/', TopicListView.as_view()),
    path('question/<int:topic_id>/', QuestionListView.as_view()),
    path('option/<int:question_id>/', OptionListView.as_view()),
    path('check/', CheckAnswerView.as_views())
]