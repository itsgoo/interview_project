from rest_framework import serializers

from .models import Interview, Question, Answer
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """ Сериализация юзера  """
    class Meta:
        model = User
        fields = ['id', 'username']
        

    
    
        

class InterviewSerializer(serializers.ModelSerializer):
    """ Сериализация опроса """

    start_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S" )
    end_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Interview
        fields = ['name', 'start_date', 'end_date', 'status', 'creator']

    def create(self, validated_data):
        return Interview.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.status = validated_data.get('status', instance.status)
        instance.creator = validated_data.get('creator', instance.creator)
        instance.save()
        return instance







        

class QuestionSerializer(serializers.ModelSerializer):
    """ Сериализация ответа  """

    class Meta:
        model = Question
        fields = ['interview', 'text', 'type_of', 'id']
        

    
    def create(self, validated_data):
        return Question.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.type_of = validated_data.get('type_of', instance.type_of)
        instance.save()
        return instance




class AnswerSerializer(serializers.ModelSerializer):
    """ Сериализация ответа  """
    question = QuestionSerializer()
    respondent = UserSerializer()
    class Meta:
        model = Answer
        fields = ['text', 'respondent', 'question']
        

    
    def create(self, validated_data):
        return Answer.objects.create(**validated_data)





