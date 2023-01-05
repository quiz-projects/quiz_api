from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status



from .serializers import (
    QuizSerializer, 
    QuizTopicSerializer,
    TopicSerializer,
    QuestionSerializer, 
    OptionSerializer, 
    StudentSerializer,
    ResultSerializer,
    ResultDetailSerializer,
    TopicQuestionSerializer
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
    def get(self, request: Request, pk):
        topic_filter = Topic.objects.get(id = pk)
        topic = TopicSerializer(topic_filter)
        topic_q = TopicQuestionSerializer(topic_filter)

        quiz_filter = Quiz.objects.get(id = topic.data['quiz'])
        quiz = QuizSerializer(quiz_filter)

        data = {
            'quiz':{
                'title': quiz.data['title'],
                'description': quiz.data['description'],
                'topic': topic_q.data
            }
        }

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
        result = Result.objects.filter(student = data['student'])
        if result:
            result2 = result.filter(topic = data["topic"])
            if result2:
                serializer1 = ResultSerializer(result2[0], many = False)

                return Response(serializer1.data)
            else:
                serializer = ResultSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors)
        else:
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
