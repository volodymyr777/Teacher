# -*- coding: utf-8 -*-
from django.db import models
import datetime

class Tema(models.Model):
    num = models.CharField(max_length=3)
    dat = models.DateField(null=True)
    tema = models.TextField()
    home = models.TextField()
    def __str__(self):
        return str(self.dat)+'->'+self.tema
    class Meta():
        db_table = 'tema'

class Uch(models.Model):
    pib = models.CharField(
        max_length=50,
        unique = True
    )
    def __str__(self):
        return self.pib
    class Meta():
        db_table = 'uch'
        ordering = ('pib',)

class Journal(models.Model):
    uch = models.ForeignKey(Uch)
    tema = models.ForeignKey(Tema)
    ocinka = models.CharField(max_length=2)
    comment = models.TextField()
    def __str__(self):
        return str(self.tema)+'->'+str(self.uch)+'->'+self.ocinka+'->'+self.comment
    class Meta():
        db_table = 'journal'

class DataR(models.Model):
    dat = models.DateField()
    def __str__(self):
        return str(self.dat)
    class Meta():
        db_table = 'datar'
        ordering = ('dat',)

class DataJ(models.Model):
    dat = models.DateField()
    num = models.IntegerField()
    name = models.CharField(max_length=15)
    def __str__(self):
        return str(self.dat)
    class Meta():
        db_table = 'dataj'
        ordering = ('dat',)

class Rozklad(models.Model):
    num = models.IntegerField()
    name = models.CharField(max_length=15)
    def __str__(self):
        return self.name
    class Meta():
        db_table = 'rozklad'
        ordering = ('num',)
