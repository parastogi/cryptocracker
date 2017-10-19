from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError
from datetime import datetime, date ,time
import datetime

class ContestForm(forms.Form):
    name=forms.CharField(label='Contest Name', max_length=100,widget=forms.TextInput(attrs={'placeholder':'Name'}))
    ctype=forms.ChoiceField(label='Type of Contest',choices=(('OWA','One Word Answer'),('MCQ','Multiple Choice Correct'),('M','Mixed')),required=True)
    startdate=forms.DateTimeField(label='Start Date',widget=forms.SelectDateWidget(attrs={'placeholder':'StartDate'}))
    starttime=forms.TimeField(label='Start Time',widget=forms.TimeInput(attrs={'placeholder':'StartTime'}))
    enddate=forms.DateTimeField(label='Start Date',widget=forms.SelectDateWidget(attrs={'placeholder':'EndDate'}))
    endtime=forms.TimeField(label='Start Time',widget=forms.TimeInput(attrs={'placeholder':'EndTime'}))
    enable_negative=forms.BooleanField(label='Enable_Negative',required=False)
    description=forms.CharField(label='description',max_length=1500,widget=forms.Textarea(attrs={'placeholder':'Description'}))
    rules=forms.CharField(label='rules',max_length=1000,widget=forms.Textarea(attrs={'placeholder':'Description'}))
    prizes=forms.CharField(label='prizes',max_length=1000,widget=forms.Textarea(attrs={'placeholder':'1st Prize \n2nd Prize \n3rd Prize\neg:\nRs10000/-\nRs7000/-\nRs5000/-\n'}))

    def clean(self):
        sdate=self.cleaned_data.get("startdate")
        stime=self.cleaned_data.get("starttime")
        today=datetime.datetime.now()
        k1=stime.hour
        k2=stime.minute
        k3=stime.second
        date=datetime.datetime.combine(sdate,time(k1,k2,k3))
        edate=self.cleaned_data.get("enddate")
        etime=self.cleaned_data.get("endtime")
        k1=etime.hour
        k2=etime.minute
        k3=etime.second
        end_date=datetime.datetime.combine(edate,time(k1,k2,k3))
        print date, end_date
        if(date<today):
            raise forms.ValidationError("Invalid Contest Start Date")
        elif(date>end_date):
            raise forms.ValidationError("Start Date but me before End Date")
        return self.cleaned_data

class QuestionFormOneWord(forms.Form):
    problem_statement=forms.CharField(label='question',max_length=2000,widget=forms.Textarea(attrs={'placeholder':'Description'}))
    answer=forms.CharField(label='answer',max_length=1000)
    image=forms.FileField(label='img')
    score=forms.IntegerField(label='score')

class QuestionFormObjective(forms.Form):
    problem_statement=forms.CharField(label='question',max_length=2000,widget=forms.Textarea(attrs={'placeholder':'Description'}))
    image=forms.FileField(required=False)
    answer=forms.CharField(label='answer',max_length=1000)
    option1=forms.CharField(label='option1',max_length=250)
    option2=forms.CharField(label='option2',max_length=250)
    option3=forms.CharField(label='option3',max_length=250,required=False)
    option4=forms.CharField(label='option4',max_length=250,required=False)
    option5=forms.CharField(label='option5',max_length=250,required=False)
    score=forms.IntegerField(label='score')

    def __init__(self, *args, **kwargs):
        super(QuestionFormObjective, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'accept': 'image/*'})
