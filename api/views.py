from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

import csv



from .serializers import (
    QuizSerializer, 
    QuizTopicSerializer,
    TopicSerializer,
    QuestionSerializer, 
    OptionSerializer, 
    StudentSerializer,
    ResultSerializer,
    ResultDetailSerializer,
    TopicQuestionSerializer,
    QuestionOptionSerializer
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
        serializer = StudentSerializer(student)
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
        # when user asks for topic result gonna create
        result = Result.objects.create()

        quiz = Quiz.objects.get(id = pk)
        quiz_serializer = QuizTopicSerializer(quiz)

        return Response({
            'quiz': quiz_serializer.data
        })

    def post(self, request: Request):
        data = request.data
        serializer = TopicSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class QuestionListView(APIView):
    def get(self, request: Request, pk: int, count: int):
        topic_filter = Topic.objects.get(id = pk)
        question_filter = Question.objects.filter(topic=topic_filter).order_by('?')[:count]

        topic = TopicSerializer(topic_filter)
        questions = QuestionOptionSerializer(question_filter, many=True)
        topic_q = TopicSerializer(topic_filter)

        quiz_filter = Quiz.objects.get(id = topic.data['quiz'])
        quiz = QuizSerializer(quiz_filter)

        data = {
            'quiz':{
                'title': quiz.data['title'],
                'description': quiz.data['description'],
                'topic': topic_q.data
            }
        }

        data['quiz']['topic']['question'] = questions.data

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
    
class GetResultView(APIView):
    def get(self, request: Request, telegram_id, topic_id):
        result_filter_student = Result.objects.filter(student = telegram_id)
        result_filter_topic = result_filter_student.filter(topic = topic_id)
        result = ResultSerializer(result_filter_topic, many = True)

        student_filter = Student.objects.get(id = telegram_id)
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


        


class UpdateResultView(APIView):
    def post(self, request: Request, pk) -> Request:
        result = Result.objects.get(id=pk)
        serializer = ResultSerializer(result, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class ResultDetailView(APIView): 
    def post(self, request:Request):
        data = request.data

        option_id = data['option']
        optoin = Option.objects.get(id = option_id)

        optoin_serializer = OptionSerializer(optoin)

        if optoin_serializer.data['is_correct']:
            result = Result.objects.get(id = data['result'])
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
        return Response(serializer.data)


class CreateDabaseView(APIView):
    def post(self, request: Request, quiz_id: int) -> Response:
        description = request.data.get('description', 'Empty')
        option_type = request.data.get('option_type', 'ochiq')
        data = request.FILES['data']

        splitdata = data.read().decode().splitlines()
        spamreader = csv.reader(splitdata)

        topic_name = data.name
        header = next(spamreader)
        
        quiz = Quiz.objects.get(id=quiz_id)
        topic, created = Topic.objects.get_or_create(title = topic_name, description = description, quiz = quiz)
        
        for row in spamreader:
            question = Question.objects.create(title = row[1], option_type=option_type, img = row[-1], topic=topic)
            
            for i in range(2, 6):
                question.option.create(title = row[i], is_correct = row[i]==row[-2])
        
        serializer = TopicQuestionSerializer(topic)
        return Response(serializer.data)