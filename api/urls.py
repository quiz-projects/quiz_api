from django.urls import path
from .views import (
    QuizListView,
    QuestionListView,
    TopicListView,
    OptionListView,
    StudentListView,
    GetResultView,
    ResultDetailView,
    UpdateResultView,
    UpdateStudentView,
    CreateDabaseView
)

urlpatterns = [
    path('student/', StudentListView.as_view()),
    path('student/<int:pk>/', StudentListView.as_view()),
    path('quiz/', QuizListView.as_view()),
    path('topic/', TopicListView.as_view()),
    path('topic/<int:pk>/', TopicListView.as_view()),
    path('question/', QuestionListView.as_view()),
    path('question/<int:pk>/<int:count>/', QuestionListView.as_view()),
    path('option/', OptionListView.as_view()),
    path('result/',GetResultView.as_view()),
    path('result/<int:telegram_id>/<int:topic_id>/',GetResultView.as_view()),
    path('update_result/<int:pk>', UpdateResultView.as_view()),
    path('result_detail/', ResultDetailView.as_view()),
    path('result_detail/<int:pk>/', ResultDetailView.as_view()),
    path('updeteStudent/<int:pk>', UpdateStudentView.as_view()),
    path('create_database/<int:quiz_id>', CreateDabaseView.as_view())
]