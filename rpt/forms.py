from django import forms
from django.forms import *
from rpt.models import *

class StudentForm(ModelForm):
    class Meta:
        model = Student

