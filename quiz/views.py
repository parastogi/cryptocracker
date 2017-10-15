# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .forms import ContestForm, QuestionFormOneWord, QuestionFormObjective
from django.http import HttpResponse
from crypto.decorators import login_required
from crypto.models import Profile
from .models import Contests,Questions
from datetime import datetime, date ,time
from django.shortcuts import redirect
from django.utils import timezone
# Create your views here.

def past (request):
    past_contest=Contests.objects.filter(start_time__lt=timezone.now())
    # print past_contest
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
        start_date_time=datetime.combine(form.cleaned_data['startdate'],time(k1,k2,k3))
        st_time=form.cleaned_data['endtime']
        k1=st_time.hour
        k2=st_time.minute
        k3=st_time.second
        choice=2
        Cont_type=form.cleaned_data['ctype'];
        if(Cont_type=='OWA'):
            choice=0
        elif(Cont_type=='MCQ'):
            choice=1
        end_date_time=datetime.combine(form.cleaned_data['enddate'],time(k1,k2,k3))
        obj=Contests.objects.create(
            contest_name=form.cleaned_data['name'],
            description=form.cleaned_data['description'],
            rules=form.cleaned_data['rules'],
            c_type=choice,
            penalty=form.cleaned_data['enable_negative'],
            start_time=start_date_time,
            end_time=end_date_time,
                        )
        print "Done"
        return redirect('/quiz/'+'edit_contest/'+str(obj.pk))
        '''except:
            return HttpResponse('Unexpected Error')'''
    if form.errors:
        errors=form.errors
    return render(request, 'crypto/create_contest.html', {'form': form,'errors':errors})

def edit_contest(request,contest_id):
    form1 = QuestionFormOneWord(request.POST or None,request.FILES)
    form2 = QuestionFormObjective(request.POST or None,request.FILES)

    errors1=None
    errors2=None

    if(form1.is_valid()):
        obj=Questions.objects.create(
        contest_id=contest_id,
        problem_type=True,
        problem_statement=form1.cleaned_data['problem_statement'],
        answer=form1.cleaned_datacleaned_data['answer'],
        score=form1.cleaned_data['score'],
        image=request.FILES['image']
        )
        obj2=Contests.objects.get(pk=contest_id)
        obj2.total_score+=form1.cleaned_data['score'];
        obj2.save();
        print "HOGAYA"
        obj3=Questions.objects.get(contest_id=contest_id)
        print obj3
        return render(request,'/quiz/'+'edit_contest/'+str(obj.pk), {'form1': form1 ,'form2':form2,'obj':obj3})
    elif(form1.errors):
        errors1=form1.errors
    if(form2.is_valid()):
        options=form2.cleaned_data['option1']+"//$$00//"+form2.cleaned_data['option2']+"//$$00//"+form2.cleaned_data['option3']+"//$$00//"+form2.cleaned_data['option4'];
        obj=Questions.objects.create(
        contest_id=contest_id,
        problem_type=False,
        problem_statement=form2.cleaned_data['problem_statement'],
        answer=form2.cleaned_data['answer'],
        score=form2.cleaned_data['score'],
        options=options,
        image=request.FILES['image']
        )
        print "HOGAYA"
        obj2=Contests.objects.get(pk=contest_id)
        obj2.total_score+=form1.cleaned_data['score'];
        obj2.save();
        obj3=Questions.objects.get(contest_id=contest_id)
        print obj3
        return render(request,'/quiz/'+'edit_contest/'+str(obj.pk), {'form1': form1 ,'form2':form2,'obj':obj3})
    elif(form2.errors):
        errors2=form2.errors
    print "NAHI HUA"
    print form1.errors
    print form2.errors
    obj=Contests.objects.get(pk=contest_id)
    st=obj.start_time
    end_time=obj.end_time
    details={'cname':obj.contest_name,'description':obj.description,'c_type':obj.c_type,'rules':obj.rules,'startdatetime':st,'endtime':end_time}
    return render(request, 'crypto/edit_contest.html',{'form1':form1,'form2':form2,'details':details,'errors1':errors1,'errors2':errors2})
