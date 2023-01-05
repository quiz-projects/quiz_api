from django.urls import path
from .views import (
    QuizListView,
    QuestionListView,
    TopicListView,
    OptionListView,
    StudentListView,
    ResultDetailView,
    UpdateStudentView,
)

urlpatterns = [
    path('student/', StudentListView.as_view()),
    path('student/<int:pk>/', StudentListView.as_view()),
    path('quiz/', QuizListView.as_view()),
    path('topic/', TopicListView.as_view()),
    path('topic/<int:pk>/', TopicListView.as_view()),
    path('question/', QuestionListView.as_view()),
    path('question/<int:pk>/', QuestionListView.as_view()),
    path('option/', OptionListView.as_view()),
    path('result_detail/', ResultDetailView.as_view()),
    path('result_detail/<int:pk>/', ResultDetailView.as_view()),
    path('updeteStudent/<int:pk>', UpdateStudentView.as_view()),
    # path('quiz/', QuizListView.as_view()),
    # path('topic/<int:quiz_id>/', TopicListView.as_view()),
    # path('question/<int:topic_id>/', QuestionListView.as_view()),
    # path('option/<int:question_id>/', OptionListView.as_view()),
]