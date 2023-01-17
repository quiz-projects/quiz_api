from .models import Quiz, Topic, Question, Option, Student, Result, ResultDetail
from rest_framework import serializers


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
            model = Student
            fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    quiz = serializers.SlugRelatedField(slug_field='title', queryset=Quiz.objects.all())
    class Meta:
        model = Topic
        fields = '__all__'



class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all())
        model = Question
        fields = '__all__'


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    student = serializers.SlugRelatedField(slug_field = 'telegram_id',queryset = Student.objects.all())
    topic = serializers.SlugRelatedField(slug_field='title',queryset = Topic.objects.all())
    class Meta:
        model = Result
        fields = '__all__'
    
class ResultDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultDetail
        fields = '__all__'

class QuizTopicSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(many=True, read_only=True)
    class Meta:
        model = Quiz
        fields = '__all__'

class QuestionOptionSerializer(serializers.ModelSerializer):
    option = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

class TopicQuestionSerializer(serializers.ModelSerializer):
    question = QuestionOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = '__all__'
