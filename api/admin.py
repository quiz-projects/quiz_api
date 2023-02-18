from django.contrib import admin
from .models import Quiz, Question, Option, Topic, Student, ResultDetail, Result, ExamResult, ExamResultDetail
# Register your models here.
admin.site.register([Question, Quiz, Option, Topic, Student, Result, ResultDetail, ExamResultDetail, ExamResult])
