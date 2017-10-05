from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from PIL import Image
class Contests(models.Model):
    contest_admin=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    contest_name=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    rules=models.CharField(max_length=200,default="Some rules")
    question_count=models.IntegerField(default=0)
    c_type=models.IntegerField(default=2)
    penalty=models.BooleanField(default=0)
    end_time=models.DateTimeField(null=True)
    start_time=models.DateTimeField(null=True)
    d_day=models.CharField(max_length=2,null=True)
    d_hour=models.CharField(max_length=2,null=True)
    d_minute=models.CharField(max_length=2,null=True)
    total_score=models.IntegerField(default=0)
    contestants=models.IntegerField(null=True)
    def __str__(self):
        return self.total_score & self.c_type & self.contest_name & self.description & self.end_time & self.start_time & self.rules

class Questions(models.Model):
    contest_id=models.ForeignKey(Contests,on_delete=models.CASCADE)
    image=models.FileField(null=True,upload_to='media')
    problem_type=models.BooleanField(default=True)
    options=models.CharField(null=True,max_length=1000)
    problem_statement=models.CharField(max_length=2000)
    answer=models.CharField(max_length=1000)
    announcement=models.CharField(max_length=2000)
    score=models.IntegerField(default=0)

class solution(models.Model):
    q_id=models.ForeignKey(Questions,on_delete=models.CASCADE)
    option=models.CharField(max_length=1000)

STATUS=(
('C','Correct'),
('W','Wrong')
)

class leaderboard(models.Model):
    c_id=models.ForeignKey(Contests,on_delete=models.CASCADE)
    q_id=models.ForeignKey(Questions,on_delete=models.CASCADE)
    u_id=models.ForeignKey(User,on_delete=models.CASCADE)
    attempts=models.IntegerField(null=True)
    status=models.CharField(max_length=10,choices=STATUS)


class Registrations(models.Model):
    c_id=models.ForeignKey(Contests,on_delete=models.CASCADE)
    u_id=models.ForeignKey(User,on_delete=models.CASCADE)
    total_score=models.IntegerField(default=0)
