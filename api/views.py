from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status



from .serializers import QuizSerializer, TopicSerializer,QuestionSerializer, OptionSerializer
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


# View for get all quiz
class QuizListView(APIView):
    def get(self, request: Request):
        '''gets all quiz objects return list of simple data'''
        quiz = Quiz.objects.all()
        serializer = QuizSerializer(quiz, many=True)
        return Response(serializer.data)
    
    def post(self, request: Request) -> Response:
        '''this fucntion creates quiz object'''
        quiz = QuizSerializer(data = request.data)

        if quiz.is_valid():
            quiz.save()
            return Response({'status': 'created'})
        return Response(quiz.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

class TopicListView(APIView):
    def get(self, request: Request, quiz_id) -> Response:
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except ObjectDoesNotExist:
            return Response({'status': f'{quiz_id} does not exists'})
        
        topics = quiz.topic.all()
        serializer = TopicSerializer(topics, many=True)

        return Response(serializer.data)

class QuestionListView(APIView):
    def get(self, request: Request, topic_id) -> Response:
        try:
            topic = Topic.objects.get(id=topic_id)
        except ObjectDoesNotExist:
            return Response({'status': f'{topic_id} does not exists'})
        
        questions = topic.question.all()
        serializer = QuestionSerializer(questions, many=True)

        return Response(serializer.data)
    
class OptionListView(APIView):
    def get(self, request: Request, question_id) -> Response:
        try:
            question = Question.objects.get(id=question_id)
        except ObjectDoesNotExist:
            return Response({'status': f'{question_id} does not exists'})
        
        options = question.option.all()
        serializer = OptionSerializer(options, many=True)

        return Response(serializer.data)

class CheckAnswerView(APIView):
    def post(self, request: Request) -> Response:
        telegram_id = request.data.get('telegram_id')
        topic_id = request.data.get('topic_id')
        question_id = request.data.get('question_id')
        option_id = request.data.get('option_id')
        
        student = Student.get(telegram_id = telegram_id)
        topic = Topic.objects.get(id=topic_id)
        question = Question.objects.get(id=question_id)
        option = Option.objects.get(id=option_id)

        result, created = Result.objects.get_or_create(student=student, topic=topic)

        if not created:
            score = result.score
            for i in result.resultdetail_set.all():
                if i.option.is_correct:
                    score += 1
            result.score = score
            result.save()

        resultdetail = ResultDetail.objects.create(result=result, question=question, option=option)

        return Response({'status': 'created'})


class GetResultView(APIView):
    def post(self, request: Request) -> Response:
        pass