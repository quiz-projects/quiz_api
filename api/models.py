from django.db import models

class Student(models.Model):
    first_name  = models.CharField(max_length=200)
    last_name   = models.CharField(max_length=200, null=True, blank=True)
    username    = models.CharField(max_length=200, null=True, blank=True)
    telegram_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.first_name

# Create your models here.
class Quiz(models.Model):
    title       = models.CharField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title
class Topic(models.Model):
    title       = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    quiz        = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='topic')

    def __str__(self):
        return self.title

class Question(models.Model):
    title       = models.TextField()
    img         = models.TextField()
    option_type = models.CharField(max_length=200)

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='question')
    
    def __str__(self):
        return self.title

class Option(models.Model):
    title      = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    question   = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='option')

    def __str__(self):
        return self.title


class Result(models.Model):
    score   = models.IntegerField(default=0)
    count   = models.IntegerField(default=0)
    date    = models.DateTimeField(auto_now_add=True)

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    topic   = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.student.first_name
class ResultDetail(models.Model):
    result   = models.ForeignKey(Result, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option   = models.ForeignKey(Option, on_delete=models.CASCADE)

    def __str__(self):
        return self.result.student.first_name

class ExamResult(models.Model):
    score   = models.IntegerField(default=0)
    count   = models.IntegerField(default=0)
    date    = models.DateTimeField(auto_now_add=True)

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    topic   = models.ManyToManyField(Topic)
    current = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='current')

    def __str__(self):
        return self.student.first_name
    
class ExamResultDetail(models.Model):
    examresult   = models.ForeignKey(ExamResult, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option   = models.ForeignKey(Option, on_delete=models.CASCADE)

    def __str__(self):
        return self.examresult.student.first_name