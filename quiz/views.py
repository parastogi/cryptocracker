# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .forms import ContestForm
from django.http import HttpResponse
from crypto.decorators import login_required
# Create your views here.
def past (request):
    return render(request,'quiz/past.html')

def live (request):
    return render(request,'quiz/live.html')

def future (request):
    return render(request,'quiz/future.html')

@login_required
def create_contest(request):
    if request.method == 'POST':
        form = ContestForm(request.POST)
        if form.is_valid():

            return HttpResponse('Filled completely')

    else:
        form = ContestForm()

    return render(request, 'crypto/create_contest.html', {'form': form})
