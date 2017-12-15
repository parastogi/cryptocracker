# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .forms import ContestForm, QuestionFormOneWord, QuestionFormObjective
from django.http import HttpResponse, JsonResponse
from crypto.decorators import login_required
from crypto.models import Profile
from .models import Contests,Questions,Leaderboard,Registrations,Team
from datetime import datetime, date ,time
from django.shortcuts import redirect
from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from operator import itemgetter
import json
import os
import random
import subprocess
from django.contrib.auth.models import User
# Create your views here.

def past (request):
    past_contest=Contests.objects.filter(end_time__lt=timezone.localtime())
    try:
        profile=Profile.objects.get(user=request.user)
    except:
        return render(request,'quiz/past.html',{'past_contest':past_contest})
    # print past_contest
    return render(request,'quiz/past.html',{'past_contest':past_contest,'profile':profile})

def live (request):
    live_contest=Contests.objects.filter(start_time__lt=timezone.localtime(),end_time__gt=timezone.localtime())
    for l in live_contest:
        print l.start_time,"st"
    print timezone.now()
    try:
        profile=Profile.objects.get(user=request.user)

    except:
        return render(request,'quiz/live.html',{'live_contest':live_contest})

    return render(request,'quiz/live.html',{'live_contest':live_contest,'profile':profile})

def future (request):
    future_contest=Contests.objects.filter(start_time__gt=timezone.localtime())
    try:
        profile=Profile.objects.get(user=request.user)

    except:
        return render(request,'quiz/future.html',{'future_contest':future_contest})

    return render(request,'quiz/future.html',{'future_contest':future_contest,'profile':profile})

@login_required
def register(request,hello):
    profile=Profile.objects.get(user=request.user)
    contest=Contests.objects.get(pk=hello)
    all_user=User.objects.all()
    register=[]
    for use in all_user:
        reg=Registrations.objects.filter(c_id=contest,u_id=use)
        if not reg:
            register.append(use)
    print register
    return render(request,'quiz/register.html',{'profile':profile,'contest':contest,'register':register})

@login_required
def registeration(request,hello):
    profile=Profile.objects.get(user=request.user)
    contest=Contests.objects.get(pk=hello)
    teamname=request.POST.get('teamname')
    team1=request.POST.getlist('team')
    print team1
    team=Team.objects.create(
        c_id=contest,
        name=teamname,
        captain=request.user
    )
    for x in team1:
        user=User.objects.get(pk=x.encode('ascii','ignore'))
        reg=Registrations.objects.create(
            c_id=contest,
            u_id=user,
            team=team
        )
        team.members.add(user)
    return redirect('/quiz/'+str(hello)+'/')

def contest(request,hello):
    contest=Contests.objects.get(pk=hello)
    if contest.end_time < timezone.now():
        return render(request,"crypto/forbiden.html")
    else:
        prizes=contest.prizes
        prizes=[z.encode('ascii','ignore') for z in prizes.split('/')]
        print prizes
        description=contest.description
        description=[z.encode('ascii','ignore') for z in description.split('/')]
        rules=contest.rules
        rules=[z.encode('ascii','ignore') for z in rules.split('/')]
        try:
            profile=Profile.objects.get(user=request.user)
        except:
            return render(request,  'quiz/contest.html',{'contest':contest,'prizes':prizes,'description':description,'rules':rules})
        register=Registrations.objects.filter(c_id=contest,u_id=request.user)
        print(register)
        start=contest.start_time
        end= contest.end_time
        e_day=end.day
        e_month=end.month
        e_year=end.year
        e_hour=end.hour
        e_minute=end.minute
        s_day=end.day
        s_month=start.month
        s_year=start.year
        s_hour=start.hour
        s_minute=start.minute
        print register[0].finished
        end_string_date=str(e_year)+"-"+str(e_month)+"-"+str(e_day)+" "+str(e_hour)+":"+str(e_minute)
        string_date=str(s_year)+"-"+str(s_month)+"-"+str(s_day)+" "+str(s_hour)+":"+str(s_minute)
        return render(request,  'quiz/contest.html',{'contest':contest,'end_string_date':end_string_date,'string_date':string_date,'prizes':prizes,'profile':profile,'description':description,'rules':rules,'register':register[0]})

@login_required
def past_contest(request , hello):
    print hello," adsd"
    profile=Profile.objects.get(user=request.user)
    contest=Contests.objects.get(pk=hello)
    ques=Questions.objects.filter(contest_id=contest.pk)
    # question_number=1
    return render (request, 'quiz/past_contest.html',{'contest':contest,'ques':ques,'profile':profile})


@login_required
def live_contest(request,hello):
    # return HttpResponse("teri")
    profile=Profile.objects.get(user=request.user)
    contest=Contests.objects.get(pk=hello)
    ques=Questions.objects.filter(contest_id=contest.pk)
    length=len(ques)
    ques_pk=Questions.objects.filter(contest_id=contest.pk).values_list('pk',flat=True)
    random_ques_pk=random.sample(ques_pk,length)
    shuffed_questions=[]
    for x in random_ques_pk:
        shuffed_questions.append(Questions.objects.get(pk=x))
    end=contest.end_time
    now=timezone.now()
    diff=end-now
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if(contest.c_type == 1):
        return render (request,'quiz/live_contest.html',{'contest':contest,
                                                    'ques':shuffed_questions,
                                                    'profile':profile,
                                                    'days':days,
                                                    'hours':hours,
                                                    'minutes':minutes,
                                                    'seconds':seconds})
    else:
        return render (request,'quiz/live_contest_one_word.html',{'contest':contest,
                                                    'ques':shuffed_questions,
                                                    'profile':profile,
                                                    'days':days,
                                                    'hours':hours,
                                                    'minutes':minutes,
                                                    'seconds':seconds})
@login_required
def submit(request,hello):
    profile=Profile.objects.get(user=request.user)
    contest=Contests.objects.get(pk=hello)
    register=Registrations.objects.get(c_id=contest,u_id=request.user)
    register.finished=True
    register.save()

    print ("!!!")

    lead=Leaderboard.objects.filter(u_id=request.user,c_id=contest)
    total=0
    # sprint ("ASDS")
    for l in lead:
        ques=Questions.objects.get(pk=l.q_id.pk)
        score=ques.score
        if(contest.c_type == 0):
            if l.status == 'Correct':
                total += score - ques.negative*(l.attempts-1)
        elif(contest.c_type == 1):
            if l.status == 'Correct':
                total += score
    print ("qwewe")
    register.total_score=total
    register.save()
    print(total)
    data={'message':'you have submitted, cant enter again now','score':register.total_score}
    return HttpResponse(json.dumps(data),content_type="application/json")

@login_required
def past_leader(request,hello):
    profile=Profile.objects.get(user=request.user)
    contest=Contests.objects.get(pk=hello)
    leader=Leaderboard.objects.filter(contest_id=hello)

@login_required
def ajax_q(request,contest_id):
    user=request.user
    profile=Profile.objects.get(user=request.user)
    q = request.POST.get('question');
    ques=Questions.objects.get(pk=q)
    contest_id=Contests.objects.get(pk=ques.contest_id.pk)
    if(contest_id.c_type == 1):
        ans=0
        if( int(request.POST.get('answer')) == 1):
            ans=ques.options1
        elif( int(request.POST.get('answer')) == 2):
            ans=ques.options2
        elif( int(request.POST.get('answer')) == 3):
            ans=ques.options3
        elif( int(request.POST.get('answer')) == 4):
            ans=ques.options4
        elif( int(request.POST.get('answer')) == 5):
            ans=ques.options5
        lead = Leaderboard.objects.filter(c_id=contest_id.pk,q_id=ques.pk,u_id=user.pk)
        if lead:
            lead = lead[0]
            if ans == ques.option:
                lead.attempts+=1
                lead.status='Correct'
                lead.save()
            else:
                lead.attempts+=1
                lead.status='Wrong'
                lead.save()
        else:
            lead=Leaderboard(c_id=contest_id,q_id=ques,u_id=user)
            if ans == ques.option:
                lead.attempts+=1
                lead.status='Correct'
                lead.save()
            else:
                lead.attempts+=1
                lead.status='Wrong'
                lead.save()
        data = { 'status': lead.status }
        return HttpResponse(json.dumps(data), content_type='application/json')
    elif(contest_id.c_type == 0):
        ans = request.POST.get('answer')
        lead = Leaderboard.objects.filter(c_id=contest_id.pk,q_id=ques.pk,u_id=user.pk)
        # flag to check if already correct
        flag = 0
        if lead:
            lead = lead[0]
            if lead.status != 'Correct' :
                flag = 1
                if ans == ques.option:
                    lead.attempts += 1
                    lead.status = 'Correct'
                    lead.save()
                else:
                    lead.attempts+=1
                    lead.status = 'Wrong'
                    lead.save()
        else:
            lead=Leaderboard(c_id=contest_id,q_id=ques,u_id=user)
            if lead.status != 'Correct' :
                flag = 1
                if ans == ques.option:
                    lead.attempts += 1
                    lead.status = 'Correct'
                    lead.save()
                else:
                    lead.attempts+=1
                    lead.status = 'Wrong'
                    lead.save()
        if(lead.status == 'Wrong'):
            lead.status += ' Attempt, You may try again.'
        else:
            lead.status += ' Attempt, Check Leaderboard for updated Rank'
        if(flag == 0):
            lead.status = "Already Solved"
        data = { 'status': lead.status }
        return HttpResponse(json.dumps(data), content_type='application/json')





@login_required
def create_contest(request):
    profile=Profile.objects.get(user=request.user)
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
        duration=end_date_time - start_date_time
        days, seconds = duration.days, duration.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        prizes=form.cleaned_data['prizes'].replace('\r\n','/')
        description=form.cleaned_data['description'].replace('\r\n','/')
        rules=form.cleaned_data['rules'].replace('\r\n','/')
        obj=Contests.objects.create(
            contest_name=form.cleaned_data['name'],
            description=description,
            rules=rules,
            c_type=choice,
            penalty=form.cleaned_data['enable_negative'],
            start_time=start_date_time,
            end_time=end_date_time,
            d_day=days,d_hour=hours,d_minute=minutes,
            prizes=prizes
                        )
        print "Done"
        return redirect('/quiz/'+'edit_contest/'+str(obj.pk))
        '''except:
            return HttpResponse('Unexpected Error')'''
    if form.errors:
        errors=form.errors
    return render(request, 'crypto/create_contest.html', {'form': form,'errors':errors,'profile':profile})


@login_required
def edit_contest(request,contest_id):
    # form1 = QuestionFormOneWord(request.POST or None,request.FILES)
    profile=Profile.objects.get(user=request.user)
    # form = QuestionFormObjective(request.POST or None,request.FILES)
    # errors1=None
    contest=Contests.objects.get(pk=contest_id)
    errors=None
    print contest.c_type
    c_type = str(contest.c_type) # done because templete doesnt do == op on integers

    if(c_type == '1'):
        if request.method == 'POST':
            form = QuestionFormObjective(request.POST,request.FILES)
            if(form.is_valid()):
                image=request.FILES['image']
                filename, file_extenstion=os.path.splitext(request.FILES['image'].name)
                full_path=settings.MEDIA_ROOT+"/"+contest_id
                url=settings.MEDIA_URL+filename
                if not os.path.isdir(full_path):
                    cmd="mkdir "+settings.MEDIA_ROOT+"/"+contest_id
                    subprocess.call(cmd,shell=True)
                fs = FileSystemStorage(full_path,url)
                file_name = fs.save(image.name, image)
                uploaded_file_url = "/media/"+contest_id+"/"+image.name
                print uploaded_file_url
                options1=form.cleaned_data['option1']
                options2=form.cleaned_data['option2']
                options3=form.cleaned_data['option3']
                options4=form.cleaned_data['option4']
                options5=form.cleaned_data['option5']
                obj=Questions.objects.create(
                                            contest_id=contest,
                                            image=uploaded_file_url,
                                            problem_type=False,
                                            problem_statement=form.cleaned_data['problem_statement'],
                                            score=form.cleaned_data['score'],
                                            option=form.cleaned_data['answer'],
                                            options1=options1,
                                            options2=options2,
                                            options3=options3,
                                            options4=options4,
                                            options5=options5,
                                    )
                print "HOGAYA"
                obj2=Contests.objects.get(pk=contest_id)
                obj2.total_score+=form.cleaned_data['score'];
                obj2.question_count+=1
                obj2.save();
                obj3=Questions.objects.filter(contest_id=contest_id)
                print obj3
                # return render(request,'/quiz/'+'edit_contest/'+str(obj.pk), {'form1': form1 ,'form2':form2,'obj':obj3})
                return redirect('/quiz/'+'edit_contest/'+str(obj2.pk))
            elif(form.errors):
                errors=form.errors
        else:
            form = QuestionFormObjective()
            obj=Contests.objects.get(pk=contest_id)
            questions=Questions.objects.filter(contest_id=contest_id)
            st=obj.start_time
            end_time=obj.end_time
            prizes=obj.prizes
            prizes=[z.encode('ascii','ignore') for z in prizes.split('/')]
            print prizes
            description=obj.description
            description=[z.encode('ascii','ignore') for z in description.split('/')]
            rules=obj.rules
            rules=[z.encode('ascii','ignore') for z in rules.split('/')]
            # details={'cname':obj.contest_name,'description':obj.description,'c_type':obj.c_type,'rules':obj.rules,'starttime':st,'endtime':end_time}
            return render(request, 'crypto/edit_contest.html',
                                            {'form':form,
                                            'details':obj,
                                            'questions':questions,
                                            'profile':profile,
                                            'prizes':prizes,
                                            'description':description,
                                            'rules':rules,
                                            'c_type':c_type})
    elif(c_type == '0'):
        if request.method == 'POST':
            form = QuestionFormOneWord(request.POST,request.FILES)
            if(form.is_valid()):
                image=request.FILES['image']
                filename, file_extenstion=os.path.splitext(request.FILES['image'].name)
                full_path=settings.MEDIA_ROOT+"/"+contest_id
                url=settings.MEDIA_URL+filename
                if not os.path.isdir(full_path):
                    cmd="mkdir "+settings.MEDIA_ROOT+"/"+contest_id
                    subprocess.call(cmd,shell=True)
                fs = FileSystemStorage(full_path,url)
                file_name = fs.save(image.name, image)
                uploaded_file_url = "/media/"+contest_id+"/"+image.name
                print uploaded_file_url
                asnwer=form.cleaned_data['answer']
                obj=Questions.objects.create(
                                contest_id = contest,
                                image = uploaded_file_url,
                                problem_type = True,
                                problem_statement=form.cleaned_data['problem_statement'],
                                score=form.cleaned_data['score'],
                                option=form.cleaned_data['answer'],
                                negative=form.cleaned_data['negative']
                            )
                print "HOGAYA"
                obj2 = Contests.objects.get(pk=contest_id)
                obj2.total_score += form.cleaned_data['score'];
                obj2.question_count += 1
                obj2.save();
                obj3 = Questions.objects.filter(contest_id=contest_id)
                print obj3
                # return render(request,'/quiz/'+'edit_contest/'+str(obj.pk), {'form1': form1 ,'form2':form2,'obj':obj3})
                return redirect('/quiz/'+'edit_contest/'+str(obj2.pk))
            elif(form.errors):
                errors=form.errors
        else:
            form = QuestionFormOneWord()
            obj = Contests.objects.get(pk = contest_id)
            questions = Questions.objects.filter(contest_id = contest_id)
            st = obj.start_time
            end_time = obj.end_time
            prizes = obj.prizes
            prizes = [z.encode('ascii','ignore') for z in prizes.split('/')]
            print prizes
            description = obj.description
            description = [z.encode('ascii','ignore') for z in description.split('/')]
            rules = obj.rules
            rules = [z.encode('ascii','ignore') for z in rules.split('/')]
            # details={'cname':obj.contest_name,'description':obj.description,'c_type':obj.c_type,'rules':obj.rules,'starttime':st,'endtime':end_time}
            return render(request, 'crypto/edit_contest.html',
                                            {'form':form,
                                            'details':obj,
                                            'questions':questions,
                                            'profile':profile,
                                            'prizes':prizes,
                                            'description':description,
                                            'rules':rules,
                                            'c_type':c_type})


@login_required
def leaderboard(request,hello):
    # WARNING DONT USE C_ID in query set because of earlier blunders
    print hello
    obj1 = Leaderboard.objects.filter(c_id = hello)
    lboard_obj = obj1.order_by('q_id')
    # print
    participation = obj1.order_by('u_id')
    # print (participation)
    user_ids = []
    for i in participation:
        user_id = i.u_id
        if(user_id not in user_ids):
            user_ids.append(user_id)
    questions_obj = Questions.objects.filter(contest_id = hello).order_by('contest_id')
    noq = len(questions_obj)
    lboard_data = []
    score = []
    for i in user_ids:
        dict2 = {}
        dict2['user_id'] = i
        dict2['name'] = i.first_name + " " +i.last_name
        op = 1
        total = 0
        quest = []
        for j in questions_obj:
            f = 0
            score.append(j.score)
            qdict = {}
            for k in lboard_obj:
                # print k.q_id,j.pk
                if( i == k.u_id and str(j.pk) == str(k.q_id)):
                    # print "Match"
                    f = 1

                    if(k.status == 'Correct'):
                        total += j.score
                        qdict['correct'] = 1
                        qdict['score']
                    else:
                        qdict['correct'] = 0
                    break
            # to see if attempted or not
            print f
            if(f == 0):
                qdict['notattempt'] = 1
                qdict['correct'] = 0
            else:
                qdict['notattempt'] = 0
            qdict['NO'] = op
            op += 1
            quest.append(qdict)
        quest = sorted(quest,key = itemgetter('NO'))
        dict2['quest'] = quest
        dict2['total'] = total
        lboard_data.append(dict2)
        print dict2
    lboard_data = sorted(lboard_data, key=itemgetter('total'),reverse=True)
    t1 = lboard_data[0]['total']
    ranknow = 1
    rankeffective = 1
    leng = len(lboard_data)
    lboard_data[0]['rank'] = 1
    for i in range (1,leng):
        rankeffective += 1
        if(t1 > lboard_data[i]['total']):
            lboard_data[i]['rank'] = rankeffective
            ranknow = rankeffective
            t1 = lboard_data[i]['total']
        else:
            lboard_data[i]['rank'] = ranknow
    print(lboard_data)
    questions = []
    t_score = 0
    for i in range(1,noq+1):
        questions.append(str(i)+"["+str(score[i-1])+"]")
        t_score += score[i-1]
    questions = sorted(questions)
    print questions
    # print (questions)
    contest_obj = Contests.objects.get(pk = hello)
    contest_data = {'contest_name':contest_obj.contest_name, 'contest_type':contest_obj.c_type}
    return render(request, 'quiz/showleaderboard.html',{'contest_data':contest_data,
                                                        'lboard_data':lboard_data,
                                                        'questions':questions,
                                                        't_score':t_score})


def live_leaderboard(request, hello):
    print hello
    obj1 = Leaderboard.objects.filter(c_id = hello)
    lboard_obj = obj1.order_by('q_id')
    # print
    participation = obj1.order_by('u_id')
    # print (participation)
    user_ids = []
    for i in participation:
        user_id = i.u_id
        if(user_id not in user_ids):
            user_ids.append(user_id)
    questions_obj = Questions.objects.filter(contest_id = hello).order_by('contest_id')
    noq = len(questions_obj)
    lboard_data = []
    score = []
    for i in user_ids:
        dict2 = {}
        dict2['user_id'] = i
        dict2['name'] = i.first_name + " " + i.last_name
        op = 1
        total = 0
        quest = []
        for j in questions_obj:
            f = 0
            score.append(j.score)
            qdict = {}
            for k in lboard_obj:
                # print k.q_id,j.pk
                if( i == k.u_id and str(j.pk) == str(k.q_id)):
                    # print "Match"
                    f = 1
                    if(k.status == 'Correct'):
                        total += j.score - j.negative * (k.attempts - 1)
                        qdict['correct'] = 1
                        qdict['effective'] = j.score - j.negative * (k.attempts - 1)
                    else:
                        qdict['correct'] = 0
                    qdict['negative']  = -1*(k.attempts -1)
                    break
            # to see if attempted or not
            print f
            if(f == 0):
                qdict['notattempt'] = 1
                qdict['correct'] = 0
            else:
                qdict['notattempt'] = 0
            qdict['NO'] = op
            op += 1
            quest.append(qdict)
        quest = sorted(quest,key = itemgetter('NO'))
        dict2['quest'] = quest
        dict2['total'] = total
        lboard_data.append(dict2)
        print dict2
    lboard_data = sorted(lboard_data, key=itemgetter('total'),reverse=True)
    t1 = lboard_data[0]['total']
    ranknow = 1
    rankeffective = 1
    leng = len(lboard_data)
    lboard_data[0]['rank'] = 1
    for i in range (1,leng):
        rankeffective += 1
        if(t1 > lboard_data[i]['total']):
            lboard_data[i]['rank'] = rankeffective
            ranknow = rankeffective
            t1 = lboard_data[i]['total']
        else:
            lboard_data[i]['rank'] = ranknow
    print(lboard_data)
    questions = []
    t_score = 0
    for i in range(1,noq+1):
        questions.append(str(i)+"["+str(score[i-1])+"]")
        t_score += score[i-1]
    questions = sorted(questions)
    print questions
    # print (questions)
    contest_obj = Contests.objects.get(pk = hello)
    contest_data = {'contest_name':contest_obj.contest_name,'contest_id':contest_obj.pk, 'contest_type':contest_obj.c_type}
    return render(request, 'quiz/showleaderboard_one_word.html',
                                                        {'contest_data':contest_data,
                                                        'lboard_data':lboard_data,
                                                        'questions':questions,
                                                        't_score':t_score})


def get_live_leaderboard(request,hello):
    obj1 = Leaderboard.objects.filter(c_id = hello)
    lboard_obj = obj1.order_by('q_id')
    participation = obj1.order_by('u_id')
    user_ids = []
    for i in participation:
        user_id = i.u_id
        if(user_id not in user_ids):
            user_ids.append(user_id)
    questions_obj = Questions.objects.filter(contest_id = hello).order_by('contest_id')
    noq = len(questions_obj)
    lboard_data = []
    score = []
    for i in user_ids:
        dict2 = {}
        dict2['user_id'] = i
        dict2['name'] = i.first_name + " " + i.last_name
        op = 1
        total = 0
        quest = []
        for j in questions_obj:
            f = 0
            score.append(j.score)
            qdict = {}
            for k in lboard_obj:
                # print k.q_id,j.pk
                if( i == k.u_id and str(j.pk) == str(k.q_id)):
                    # print "Match"
                    f = 1
                    if(k.status == 'Correct'):
                        total += j.score - j.negative * (k.attempts - 1)
                        qdict['correct'] = 1
                        qdict['effective'] = j.score - j.negative * (k.attempts - 1)
                        qdict['negative']  = -1*(k.attempts -1)
                    else:
                        qdict['correct'] = 0
                        qdict['negative']  = -1*(k.attempts)
                    break
            # to see if attempted or not
            print f
            if(f == 0):
                qdict['notattempt'] = 1
                qdict['correct'] = 0
            else:
                qdict['notattempt'] = 0
            qdict['NO'] = op
            op += 1
            quest.append(qdict)
        quest = sorted(quest,key = itemgetter('NO'))
        dict2['quest'] = quest
        dict2['total'] = total
        lboard_data.append(dict2)
        print dict2
    lboard_data = sorted(lboard_data, key=itemgetter('total'),reverse=True)
    t1 = lboard_data[0]['total']
    ranknow = 1
    rankeffective = 1
    leng = len(lboard_data)
    lboard_data[0]['rank'] = 1
    for i in range (1,leng):
        rankeffective += 1
        if(t1 > lboard_data[i]['total']):
            lboard_data[i]['rank'] = rankeffective
            ranknow = rankeffective
            t1 = lboard_data[i]['total']
        else:
            lboard_data[i]['rank'] = ranknow
    print(lboard_data)
    questions = []
    t_score = 0
    for i in range(1,noq+1):
        questions.append(str(i)+"["+str(score[i-1])+"]")
        t_score += score[i-1]
    questions = sorted(questions)
    print questions
    html = render_to_string('quiz/leaderboard_one_word.html',
                                                        {'lboard_data':lboard_data,
                                                        'questions':questions,
                                                        't_score':t_score},request)
    data = {'html' : html}
    return HttpResponse(json.dumps(data),content_type="application/json")
