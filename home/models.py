from django.db import models


class Person(models.Model):
    isim = models.CharField(max_length=100, help_text="Depremzedenin ismi")
    sehir = models.CharField(max_length=100, default="Yok", help_text="Depremzedenin bulunduğu şehir")
    adres = models.CharField(max_length=256, help_text="Depremzedenin bulunduğu adres")
    tel = models.CharField(max_length=13, help_text="Depremzedenin telefon numarası", null=True, blank=True)
    durum = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"

    def __str__(self):
        return self.isim