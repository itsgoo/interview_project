from datetime import datetime , timedelta
import pytz

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from .models import Interview, Question, Answer
from .serializers import InterviewSerializer, QuestionSerializer, AnswerSerializer

from django.contrib.auth.models import User


class InterviewList(APIView):
    # Список всех опросов. Если пользователь не зарегистрироваг, 
    # то выводятся только актуальные опросы
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):

        date_now = datetime.now()
        date_now_delta = date_now + timedelta(hours = 3)

        user = self.request.user
        if user.is_authenticated:
            interview_list = Interview.objects.all()
        else:
            interview_list = Interview.objects.filter(start_date__lt = date_now_delta, end_date__gte = date_now_delta)


        serializer = InterviewSerializer(interview_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        interview = InterviewSerializer(data=request.data)
        print('interview post: ', interview)

        if interview.is_valid():
            interview_saved = interview.save()
            return Response({"success": "Interview '{}' created successfully".format(interview_saved.name)})
        else:
            return Response({'ststus': 'Error'})

    def put(self, request, pk):
        saved_interview = get_object_or_404(Interview.objects.all(), pk=pk)
        data = request.data
        interview = InterviewSerializer(instance=saved_interview, data=data, partial=True)
        print('interview PUT', interview)

        if interview.is_valid():
            interview_saved = interview.save()
            return Response({"success": "Interview '{}' changed successfully".format(interview_saved.id)})
        else:
            return Response({'ststus': 'Error'})

    def delete(self, request, pk):
        # Get object with this pk
        delete_interview = get_object_or_404(Interview.objects.all(), pk=pk)
        delete_interview.delete()
        return Response({
            "message": "interview with id `{}` has been deleted.".format(pk)
        }, status=204)


class InterviewPage(APIView):
    # Страница опроса
    
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        one_interview = Question.objects.filter(interview = pk)
        serializer = QuestionSerializer(one_interview, many=True)
        return Response(serializer.data)


class QuestionPage(APIView):
    # Страница вопроса

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def get(self, request, pk):
        one_interview = Question.objects.filter(id = pk)
        serializer = QuestionSerializer(one_interview, many=True)
        return Response(serializer.data)

    def post(self, request):
            question_create = QuestionSerializer(data=request.data)
            print('question_create', question_create)
        
            if question_create.is_valid():
                question_saved = question_create.save()
                return Response({"success": "Interview '{}' created successfully".format(question_saved.id)})
            else:
                return Response({'ststus': 'Error'})

    def put(self, request, pk):
        saved_question = get_object_or_404(Question.objects.all(), pk=pk)
        data = request.data
        question = QuestionSerializer(instance=saved_question, data=data, partial=True)
        print('question PUT', question)

        if question.is_valid():
            question_saved = question.save()
            return Response({"success": "Question '{}' changed successfully".format(question_saved.id)})
        else:
            return Response({'ststus': 'Error'})

    def delete(self, request, pk):
        # Get object with this pk
        delete_question = get_object_or_404(Question.objects.all(), pk=pk)
        delete_question.delete()
        return Response({
            "message": "Question with id `{}` has been deleted.".format(pk)
        }, status=204)


class AnswerPage(APIView):
    # Страница ответа

    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        one_answer = Answer.objects.filter(id = pk)
        serializer = AnswerSerializer(one_answer, many=True)
        return Response(serializer.data)

    def post(self, request):
            answer_create = AnswerSerializer(data=request.data)

            respondent_id = request.data['respondent']     

            try:
                user_id = User.objects.get(id = respondent_id)
            except :
                user_id = 0
            
            if user_id == 0:
                print('not user_id')
                user = self.request.user
                if not user.is_authenticated:
                    print('User.is_authenticated when answer posted')
                    user = User(username= respondent_id, id = respondent_id)
                    user.is_staff = None
                    user.is_superuser = None
                    user.save()

            if answer_create.is_valid():
                answer_saved = answer_create.save()
                return Response({"success": "Answer '{}' created successfully".format(answer_saved.id)})
            else:
                return Response({'ststus': 'Error'})


class AnswerUserPage(APIView):
    # Страница включающая опросы и их вопросы и ответы 
    # для конкретного пользователя 
    
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, pk):
        all_interviews = Answer.objects.select_related('question').filter(respondent = pk)
        print('all_interviews', all_interviews)
        serializer = AnswerSerializer(all_interviews, many=True)
        return Response(serializer.data)