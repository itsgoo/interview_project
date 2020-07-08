from django.contrib import admin
from .models import Interview, Question, Answer
# Register your models here.


class InterviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_date', 'end_date', 'status', 'creator')

admin.site.register(Interview, InterviewAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('interview', 'text', 'type_of')

admin.site.register(Question, QuestionAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'respondent', 'question')

admin.site.register(Answer, AnswerAdmin)