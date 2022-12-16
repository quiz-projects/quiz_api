from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .serializers import QuizSerializer, TopicSerializer, QuestionSerializer, OptionSerializer, StudentSerializer, ResultSerializer, ResultDetailSerializer
# Create your views here.
from .models import Quiz, Topic, Question, Option, Student, Result, ResultDetail


# View for get all quiz
class QuizListView(APIView):
    def get(self, request: Request):
        quiz = Quiz.objects.all()
        serializer = QuizSerializer(quiz, many=True)
        return Response(serializer.data)

    def post(self, request: Request):
        data = request.data
        serializer = QuizSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class QuestionListView(APIView):
    pass


class TopicListView(APIView):
    pass

class CheckAnswerView(APIView):
    pass

class GetResultView(APIView):
    pass



   
    