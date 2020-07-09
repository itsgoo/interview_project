from django.urls import path, include, re_path
from django.conf.urls import url
from .views import InterviewList, InterviewPage, QuestionPage, AnswerPage, AnswerUserPage
from rest_framework.authtoken.views import obtain_auth_token
from question_proj.yasg import urlpatterns as doc_urls


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # path('auth/token/', obtain_auth_token, name='token'),
    
    path('main/', include('rest_framework.urls')),

    path('interview-list/', InterviewList.as_view()),

    # Для удаления и обновления опроса
    path('interview-list/<int:pk>', InterviewList.as_view()),

    path('interview/<int:pk>', InterviewPage.as_view()),

    # Для создания вопроса
    path('question/', QuestionPage.as_view()),
    path('question/<int:pk>', QuestionPage.as_view()),

    path('answer/<int:pk>', AnswerPage.as_view()),
    path('answer/', AnswerPage.as_view()),
    path('answer-user/<int:pk>', AnswerUserPage.as_view()),


] 
urlpatterns += doc_urls