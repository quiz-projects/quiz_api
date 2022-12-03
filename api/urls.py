from django.urls import path
from .views import QuizListView

urlpatterns = [
    path('quiz/', QuizListView.as_view()),
]