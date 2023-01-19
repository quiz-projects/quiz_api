from .models import Quiz, Topic, Question, Option, Student, Result, ResultDetail
from rest_framework import serializers

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'

class ResultDetailsSerializer(serializers.ModelSerializer):
    question =  QuestionSerializer()
    option = OptionSerializer()

    class Meta:
        model = ResultDetail
        fields = '__all__'

class ResultsSerializer(serializers.ModelSerializer):
    resultdetail_set = ResultDetailsSerializer(many=True)
    topic = TopicSerializer()

    class Meta:
        model = Result
        fields = '__all__'

class StudentsSerializer(serializers.ModelSerializer):
    result_set = ResultsSerializer(many=True)
    class Meta:
            model = Student
            fields = '__all__'