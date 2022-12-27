from django.contrib import admin
from .models import Quiz, Question, Option, Topic
# Register your models here.
admin.site.register([Question, Quiz, Option, Topic])
