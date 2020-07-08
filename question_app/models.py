from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Interview(models.Model):
    """ модель опросов """
    name = models.CharField('Имя опроса', max_length= 100)
    start_date = models.DateTimeField('Начало опроса', auto_now_add = False, blank=True)
    end_date = models.DateTimeField('Окончание опроса', auto_now_add = False, blank=True)
    status = models.CharField('статус Опроса', max_length= 100)
    creator = models.ForeignKey(User, verbose_name = 'Создатель опроса', on_delete= models.CASCADE)
    
    def __str__(self):
            return self.name


class Question(models.Model):
    """ модель вопросов в опросе """

    question_type= (
        ('text', 'text'),
        ('radio', 'radio'),
        ('checkbox', 'checkbox'),
    )

    interview = models.ForeignKey(Interview, verbose_name = 'Опрос', on_delete= models.CASCADE)
    text = models.CharField('Текст вопроса', max_length= 500)
    type_of = models.CharField(max_length=20, choices=question_type, verbose_name='Тип вопроса')

    def __str__(self):
           return self.text


class Answer(models.Model):
    text = models.CharField('Текст ответа', max_length= 500)
    respondent = models.ForeignKey(User, verbose_name = 'Респондент', on_delete= models.CASCADE)
    question = models.ForeignKey(Question, verbose_name = 'Вопрос', on_delete= models.CASCADE)

    def __str__(self):
           return self.text

