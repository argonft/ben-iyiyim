from django.db import models

# Create your models here.
class Person(models.Model):
    isim = models.CharField(max_length=100)
    adres = models.CharField(max_length=256)
    tel = models.CharField(max_length=30)
    durum = models.CharField(max_length=100)
