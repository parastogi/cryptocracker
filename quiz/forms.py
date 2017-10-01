from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError
from datetime import datetime, date ,time
import datetime
class ContestForm(forms.Form):
    name=forms.CharField(label='Contest Name', max_length=100,widget=forms.TextInput(attrs={'placeholder':'Name'}))
    ctype=forms.ChoiceField(label='Type of Contest',choices=(('OWA','One Word Answer'),('MCQ','Multiple Choice Correct'),('M','Mixed')),required=True)
    startdate=forms.DateTimeField(label='Start Date',widget=forms.SelectDateWidget(attrs={'placeholder':'StartDate'}))
    duration=forms.TimeField(label='Duration',widget=forms.TextInput(attrs={'placeholder':'Duration'}))
    starttime=forms.TimeField(label='Start Time',widget=forms.TimeInput(attrs={'placeholder':'StartTime'}))
    enable_negative=forms.BooleanField(label='Enable_Negative')
    description=forms.CharField(label='description',max_length=1500,widget=forms.Textarea(attrs={'placeholder':'Description'}))
    rules=forms.CharField(label='rules',max_length=200,widget=forms.Textarea(attrs={'placeholder':'Description'}))
    def clean(self):
        sdate=self.cleaned_data.get("startdate")
        stime=self.cleaned_data.get("starttime")
        today=datetime.datetime.now()
        k1=stime.hour
        k2=stime.minute
        k3=stime.second
        date=datetime.datetime.combine(sdate,time(k1,k2,k3))
        print date
        print today
        if(date<today):
            raise forms.ValidationError("Invalid Contest Start Date")
        return self.cleaned_data
#######TO DO
######ADD VALIDATIONS
