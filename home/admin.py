from django.contrib import admin
from .views import *
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']


class PersonAdmin(admin.ModelAdmin):
    list_display = ('isim', 'sehir', 'adres', 'tel', 'durum', 'created_at')
    list_filter = ('sehir', 'durum')
    search_fields = ('isim', 'sehir', 'adres', 'tel', 'durum')
    ordering = ('-created_at',)

admin.site.register(Person, PersonAdmin)
