from django.contrib import admin
from .views import *
# Register your models here.

class PersonAdmin(admin.ModelAdmin):
    list_display = ('isim', 'sehir', 'adres', 'tel', 'durum', 'created_at')
    list_filter = ('sehir', 'durum')
    search_fields = ('isim', 'sehir', 'adres', 'tel', 'durum')
    ordering = ('-created_at',)

admin.site.register(Person, PersonAdmin)