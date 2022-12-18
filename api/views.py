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
        print(pk)
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
                    'questions_index':list(range(0,len(question.data))),
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

class OptionListView(APIView):
    def post(self, request: Request):
        print('hi')
        data = request.data
        serializer = OptionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class CheckAnswerView(APIView):
    pass

class GetResultView(APIView):
    def get(self, request: Request, s_id, t_id):
        result_filter_student = Result.objects.filter(student = s_id)
        result_filter_topic = result_filter_student.filter(topic = t_id)
        result = ResultSerializer(result_filter_topic, many = True)

        student_filter = Student.objects.get(id = s_id)
        student = StudentSerializer(student_filter, many = False)

        data = {
            'student':{
                'id':student.data['id'],
                'first_name':student.data['first_name'],
                'last_name':student.data['last_name'],
                'telegram_id':student.data['telegram_id'],
                'username':student.data['username'],
                'results':result.data
            }
        }

        return Response(data)
    def post(self, request:Request):
        data = request.data
        serializer = ResultSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class ResultDetailView(APIView):
    def post(self, request:Request):
        data = request.data

        option_id = data['option']
        optoin = Option.objects.get(id = option_id)
        optoin_serializer = OptionSerializer(optoin, many = False)

        if optoin_serializer.data['is_correct'] == True:
            result = Result.objects.filter(id = data['result'])[0]
            result.score += 1
            result.save()
        serializer = ResultDetailSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def get(self, requst:Request, pk):
        option = Option.objects.get(id = pk)
        serializer = OptionSerializer(option, many = False)
        print(serializer.data)
        return Response(serializer.data)

class StudentListView(APIView):
    def post(self, request:Request):
        data = request.data
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def get(self, request:Request, pk):
        student = Student.objects.get(telegram_id = pk)
        serializer = StudentSerializer(student, many = False)
        return Response(serializer.data)



   
    