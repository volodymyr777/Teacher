# -*- coding: utf-8 -*-
from django.forms.models import ModelForm

from .models import Tema, Rozklad
from django import forms

class TemaForm(ModelForm):
    class Meta:
        model = Tema
        fields = ('num', 'dat', 'tema', 'home')

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
    class Meta:
        fields = ('title', 'file')

class RozkladForm(ModelForm):
    num = forms.CharField(max_length=1)
    name = forms.CharField(max_length=10)
    class Meta:
        model = Rozklad
        fields = ('num', 'name')

