# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .forms import ContestForm
from django.http import HttpResponse
from crypto.decorators import login_required
from crypto.models import Profile
from .models import Contests
from django.utils import timezone
# Create your views here.

def past (request):
    past_contest=Contests.objects.filter(start_time__lt=timezone.now())
    print past_contest
    return render(request,'quiz/past.html',{'past_contest':past_contest})

@login_required
def past_contest(request , hello):
    print hello," adsd"
    contest=Contests.objects.get(pk=hello)
    return render (request, 'quiz/contest.html',{'contest':contest})



def live (request):
    return render(request,'quiz/live.html')

def future (request):
    return render(request,'quiz/future.html')

@login_required
def create_contest(request):
    profile=Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ContestForm(request.POST)
        if form.is_valid():

            return HttpResponse('Filled completely')

    else:
        form = ContestForm()

    return render(request, 'crypto/create_contest.html', {'form': form,'profile':profile})
