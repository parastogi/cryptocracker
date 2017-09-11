# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from quiz.models import Contests
# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User)
    roll=models.IntegerField()
    phone=models.CharField(max_length=12)
    is_admin=models.ForeignKey(Contests,on_delete=models.CASCADE,blank=True,null=True)
