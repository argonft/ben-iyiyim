from rest_framework import serializers
from .models import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['isim', 'sehir', 'adres', 'tel', 'durum', 'created_at']
