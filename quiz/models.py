from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

from django.views.decorators.cache import cache_control

class Contests(models.Model):
    contest_admin=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contest_name=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    rules=models.CharField(max_length=1000)
    question_count=models.IntegerField(default=0)
    c_type=models.IntegerField(default=2)
    penalty=models.FloatField(default=0)
    end_time=models.DateTimeField(null=True)
    start_time=models.DateTimeField(null=True)
    d_day=models.CharField(max_length=2, null=True)
    d_hour=models.CharField(max_length=2, null=True)
    d_minute=models.CharField(max_length=2, null=True)
    total_score=models.FloatField(default=0)
    contestants=models.IntegerField(null=True)
    prizes=models.CharField(max_length=1000, null=True)
    def __str__(self):
        return str(self.contest_name)

class Questions(models.Model):
    contest_id=models.ForeignKey(Contests, on_delete=models.CASCADE)
    image=models.CharField(max_length=1000, null=True)
    problem_type=models.BooleanField(default=True)
    options1=models.CharField(null=True, max_length=1000)
    options2=models.CharField(null=True, max_length=1000)
    options3=models.CharField(null=True, max_length=1000)
    options4=models.CharField(null=True, max_length=1000)
    options5=models.CharField(null=True, max_length=1000)
    problem_statement=models.CharField(max_length=2000)
    announcement=models.CharField(max_length=2000)
    score=models.FloatField(default=0)
    option=models.CharField(max_length=1000,null=True)
    negative=models.FloatField(null=True)
    def __str__(self):
        return str(self.pk)

STATUS=(
('C','Correct'),
('W','Wrong')
)

from crypto.models import *
class Team(models.Model):
    c_id=models.ForeignKey(Contests,on_delete=models.CASCADE)
    members=models.ManyToManyField(User,related_name='members')
    name=models.CharField(max_length=100)
    captain=models.ForeignKey(User,on_delete=models.CASCADE, related_name='captain', null=True)

class Leaderboard(models.Model):
    c_id=models.ForeignKey(Contests, on_delete=models.CASCADE)
    q_id=models.ForeignKey(Questions, on_delete=models.CASCADE)
    u_id=models.ForeignKey(User, on_delete=models.CASCADE)
    attempts=models.IntegerField(default=0)
    status=models.CharField(max_length=10, choices=STATUS)
    def __str__(self):
        return 'User_id = {}, Question_ID = {}, Status = {}'.format(self.u_id, self.q_id, self.status)


class Registrations(models.Model):
    c_id=models.ForeignKey(Contests,on_delete=models.CASCADE)
    u_id=models.ForeignKey(User,on_delete=models.CASCADE)
    total_score=models.IntegerField(default=0)
    team=models.ForeignKey(Team,null=True)
    finished=models.BooleanField(default=False)
    def __str__(self):
        return ' U_id = {},team = {}'.format( self.u_id, self.team)
