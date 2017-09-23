from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control

class Contests(models.Model):
    contest_name=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    question_count=models.IntegerField(default=0)
    penalty=models.IntegerField(default=0)
    start_time=models.DateTimeField()
    duration=models.DateTimeField()
    total_score=models.IntegerField(default=0)

class Questions(models.Model):
    contest_id=models.ForeignKey(Contests,on_delete=models.CASCADE)
    u_id=models.ForeignKey(User,on_delete=models.CASCADE)
    problem_id=models.CharField(max_length=50)
    problem_statement=models.CharField(max_length=2000)
    answer=models.CharField(max_length=1000)
    announcement=models.CharField(max_length=2000)
    score=models.IntegerField(default=0)
    attempts=models.IntegerField(default=0)
    wrong=models.IntegerField(default=0)


class Registrations(models.Model):
    c_id=models.ForeignKey(Contests,on_delete=models.CASCADE)
    u_id=models.ForeignKey(User,on_delete=models.CASCADE)
    total_score=models.IntegerField(default=0)
