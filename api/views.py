from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status



from .serializers import (
    QuizSerializer, 
    TopicSerializer,
    QuestionSerializer, 
    OptionSerializer, 
    StudentSerializer,
    ResultDetailSerializer
)
# Create your views here.

from .models import (
    Quiz, 
    Topic, 
    Question, 
    Option,
    Student,
    Result,
    ResultDetail
)

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

class UpdateStudentView(APIView):
    def post(self, request:Request, pk):
        data = request.data
        student = Student.objects.get(id = pk)
        student.question_list = data["question_list"]
        student.save()
        return Response({"question_list":student.question_list})

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

class ResultDetailView(APIView): 
    def post(self, request:Request):
        data = request.data

        option_id = data['option']
        optoin = Option.objects.get(id = option_id)
        optoin_serializer = OptionSerializer(optoin, many = False)

        if optoin_serializer.data['is_correct'] == True:
            result = Result.objects.get(id = data['result'])
            result.score += 1
            result.save()
        serializer = ResultDetailSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def get(self, requst:Request, pk):
        print(pk)
        option = Option.objects.get(id = pk)
        serializer = OptionSerializer(option, many = False)
        return Response(serializer.data)


class GetResultView(APIView):
    def post(self, request: Request) -> Response:
        pass