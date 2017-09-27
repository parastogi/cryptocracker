from django import forms
from django.contrib.admin.widgets import AdminDateWidget

class ContestForm(forms.Form):
    name=forms.CharField(label='Contest Name', max_length=100,widget=forms.TextInput(attrs={'placeholder':'Name'}))
    cid=forms.CharField(label='Contest Id',max_length=10,widget=forms.TextInput(attrs={'placeholder':'ID'}))
    ctype=forms.ChoiceField(label='Type of Contest',choices=(('OWA','One Word Answer'),('MCQ','Multiple Choice Correct'),('M','Mixed')),required=True)
    startdate=forms.DateTimeField(label='Start Date',widget=forms.TextInput(attrs={'placeholder':'StartDate'}))
    duration=forms.TimeField(label='Duration',widget=forms.TextInput(attrs={'placeholder':'Duration'}))
