from django.db import models
from django.utils import timezone
# Create your models here.

class Person(models.Model):
    isim = models.CharField(max_length=100)
    sehir = models.CharField(max_length=100, default="Yok")
    adres = models.CharField(max_length=256)
    tel = models.CharField(max_length=11, default="Yok")
    durum = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
