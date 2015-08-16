# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import repoze, job, tema, rozklad, uchni, journal, journal_edit
from django.views.generic import TemplateView

urlpatterns = patterns('Klas_Predmet',
    url((r'^$'), TemplateView.as_view(template_name='home.html')),
    url(r'^repoze/$', repoze ),
    url(r'^job/$', job ),
    url(r'^tema/$', tema ),
    url(r'^rozklad/$', rozklad ),
    url(r'^uchni/$', uchni ),
    url(r'^journal/$', journal ),
    url(r'^journal_edit/$', journal_edit ),

)