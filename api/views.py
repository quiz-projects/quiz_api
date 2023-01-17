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
        '''Creates student given body request
        request.data = {
            "first_name": "sanjarbek",
            "last_name": "saidov",
            "username": "sanjarbek",
            "telegram_id": 12345
        }
        '''

        data = request.data
        serializer = StudentSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def get(self, request:Request, pk):
        '''Returns student data given pk (pk is telegram_id)'''

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
        '''Returns all quiz objects'''

        quiz = Quiz.objects.all()
        serializer = QuizSerializer(quiz, many=True)

        return Response(serializer.data)

    def post(self, request: Request):
        '''Creates quiz given body data

        request.data = {
            "title": "python",
            "description": "for learning"
        }
        '''
        data = request.data
        serializer = QuizSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

class TopicListView(APIView):
    def get(self, request: Request, pk):
        '''Returns topic given the pk (pk is quiz id)'''

        quiz = Quiz.objects.get(id = pk)
        quiz_serializer = QuizTopicSerializer(quiz)

        return Response({
            'quiz': quiz_serializer.data
        })

    def post(self, request: Request):
        '''Creates Topic given body data

        request.data = {
            "title": "Built-in Functions.csv",
            "description": "this is description",
            "quiz": "python"
        }
        '''
        data = request.data
        serializer = TopicSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

class QuestionListView(APIView):
    def get(self, request: Request, topic_id: int, count: int):
        '''
        Returns random questions given topic_id and count (count for how many question needs to be send
        
        Also returns which quiz and topic datas
        
        Then Creates result object to store data for given params in query
        
        '''
        telegram_id = request.query_params.get('telegram_id')
        
        student = Student.objects.get(telegram_id=telegram_id)
        topic_filter = Topic.objects.get(id = topic_id)

        # Creates result for the given student and topic
        result = Result.objects.create(student=student, topic=topic_filter)

        # Random questions with the given number which is count
        question_filter = Question.objects.filter(topic=topic_filter).order_by('?')[:count]

        topic = TopicSerializer(topic_filter)
        questions = QuestionOptionSerializer(question_filter, many=True)
        topic_q = TopicSerializer(topic_filter)

        quiz_filter = Quiz.objects.get(title = topic.data['quiz'])
        quiz = QuizSerializer(quiz_filter)

        data = {
            'quiz':{
                'title': quiz.data['title'],
                'description': quiz.data['description'],
                'result': result.id,
                'topic': topic_q.data
            }
        }

        data['quiz']['topic']['question'] = questions.data

        return Response(data)

    def post(self, request: Request):
        '''Creates question for given data body
        
        request.data = {
            "title": "Ushbu code bajarganda natija nima chiqaradi?",
            "img": "https://telegra.ph/file/76631a635d49ca505c363.jpg",
            "option_type": "ochiq",
            "topic": "Built-in Functions.csv"
        }
        '''
        data = request.data
        serializer = QuestionSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

class OptionListView(APIView):
    def post(self, request: Request):
        '''Creates option object for given data body
        
        request.data = {
            "title": "A",
            "is_correct": True or False,
            "question": 1
        }
        '''
        data = request.data
        serializer = OptionSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            
        return Response(serializer.errors)
    
class ResultView(APIView):
    def get(self, request: Request, telegram_id, topic_id):
        '''Returns list of result data for given telegram_id and topic_id'''

        student = Student.objects.get(telegram_id = telegram_id)
        results = student.result_set.filter(topic = topic_id)
        
        result = ResultSerializer(results, many = True)
        student = StudentSerializer(student)

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
        '''Creates result object for given data body
        
        request.data = {
            "student": telegram_id,
            "topic": title
        }
        '''

        data = request.data
        serializer = ResultSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)

class ResultDetailView(APIView):
    def post(self, request:Request):
        '''Creates resultdetail object for given data body
        
        request.data = [ 
            {
                "option": id,
                "question": id,
                "result": id,
            },
            {
                "option": id,
                "question": id,
                "result": id,
            }
        ]
        '''
        data_list = request.data

        for data in data_list:
            option_id = data['option']
            option = Option.objects.get(id = option_id)

            if option.is_correct:
                result = Result.objects.get(id = data['result'])
                result.score += 1
                result.save()

        serializer = ResultDetailSerializer(data=data_list, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def get(self, requst:Request, pk):
        '''Returns option data for given pk (pk is option id)'''

        option = Option.objects.get(id = pk)
        serializer = OptionSerializer(option)

        return Response(serializer.data)


class CreateDabaseView(APIView):
    def post(self, request: Request, quiz_id: int) -> Response:
        '''Creates database for given csv file
        topic_name = file_name

        request.data = {
            "description": "",
            "option_type": ""
        }

        request.FILES['data'] => 
            header = id,question,option01,option02,option03,option04,answer,image_link
        '''

        description = request.data.get('description', 'Empty')
        option_type = request.data.get('option_type', 'ochiq')
        data = request.FILES['data']

        splitdata = data.read().decode().splitlines()
        spamreader = csv.reader(splitdata)

        topic_name = data.name.split('.')[0]
        header = next(spamreader)
        
        quiz = Quiz.objects.get(id=quiz_id)
        topic, created = Topic.objects.get_or_create(title = topic_name, description = description, quiz = quiz)
        
        for row in spamreader:
            question = Question.objects.create(title = row[1], option_type=option_type, img = row[-1], topic=topic)
            
            for i in range(2, 6):
                question.option.create(title = row[i], is_correct = row[i]==row[-2])
        
        serializer = TopicQuestionSerializer(topic)
        return Response(serializer.data)