# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .forms import ContestForm
from django.http import HttpResponse
from crypto.decorators import login_required
from crypto.models import Profile
from .models import Contests
from datetime import datetime, date ,time
from django.shortcuts import redirect
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
    form = ContestForm(request.POST or None)
    errors=None
    if form.is_valid():
        print "yes"
        st_time=form.cleaned_data['starttime']
        k1=st_time.hour
        k2=st_time.minute
        k3=st_time.second
        date=datetime.combine(form.cleaned_data['startdate'],time(k1,k2,k3))
        obj=Contests.objects.create(
            contest_name=form.cleaned_data['name'],
            description=form.cleaned_data['description'],
            rules=form.cleaned_data['rules'],
            penalty=form.cleaned_data['enable_negative'],
            start_time=date,
            duration=form.cleaned_data['duration']
            )
        print "Done"
        return redirect('/quiz/'+'edit_contest/'+str(obj.pk))
        '''except:
            return HttpResponse('Unexpected Error')'''
    if form.errors:
        errors=form.errors
    return render(request, 'crypto/create_contest.html', {'form': form,'errors':errors})

def edit_contest(request,contest_id):
    print "YO"
    obj=Contests.objects.get(pk=contest_id)
    st=obj.start_time
    dur=obj.duration
    print st,dur
    q1=dur.hour
    q2=dur.minute
    q3=dur.second
    print q1,q2,q3
    end_time=datetime.combine(st,time(q1,q2,q3));
    print end_time
    parm={'cname':obj.contest_name,'description':obj.description,'rules':obj.rules,'startdatetime':st,'endtime':end_time}
    return render(request, 'crypto/edit_contest.html',parm)
