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

class TopicListView(APIView):
    def get(self, request: Request, pk):
        topic_filter = Topic.objects.filter(quiz = pk)
        topic = TopicSerializer(topic_filter, many = True)

        quiz_filter = Quiz.objects.get(id = pk)
        quiz = QuizSerializer(quiz_filter, many = False)

        data = {
            'quiz':{
                'id':quiz.data['id'],
                'title':quiz.data['title'],
                'description':quiz.data['description'],
                'topics':topic.data
            }
        }

        return Response(data)

    def post(self, request: Request):
        data = request.data
        serializer = TopicSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class QuestionListView(APIView):
    def get(self, request: Request, pk):
        topic_filter = Topic.objects.get(id = pk)
        topic = TopicSerializer(topic_filter, many = False)

        question_filter = Question.objects.filter(topic = pk)
        question = QuestionSerializer(question_filter, many = True)

        quiz_filter = Quiz.objects.get(id = topic.data['quiz'])
        quiz = QuizSerializer(quiz_filter, many = False)

        data = {
            'quiz':{
                'title':quiz.data['title'],
                'description':quiz.data['description'],
                'topic':{
                    'id':topic.data['id'],
                    'title':topic.data['title'],
                    'description':topic.data['description'],
                    'questions':[]
                }
            }
        }
        
        for i in question.data:
            option_filter = Option.objects.filter(question = i['id'])
            option = OptionSerializer(option_filter, many = True)
            
            data['quiz']['topic']['questions'].append({
                'id':i['id'],
                'title':i['title'],
                'img':i['img'],
                'option_type':i["option_type"],
                "options":option.data
            })
            
        return Response(data)

    def post(self, request: Request):
        data = request.data
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class CheckAnswerView(APIView):
    pass

class GetResultView(APIView):
    def get(self, request: Request):
        pass
    def post(self, request: Request):
        pass



   
    