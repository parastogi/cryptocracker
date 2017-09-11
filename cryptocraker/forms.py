from django import forms
from djano.contrib.auth.models import User

 class SinupForm(form.ModelForm):
     username=forms.Charfield(max_length=128)
