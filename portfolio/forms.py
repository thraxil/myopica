from django import forms
from models import *
from django.forms import ModelForm

class AddImageForm(ModelForm):
    class Meta:
        model = Image
        exclude = ('ahash','extension')
