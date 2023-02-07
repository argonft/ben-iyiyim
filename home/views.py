from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.shortcuts import render
from .models import Person
from django.db.models import Q
from datetime import datetime
import json

# Create your views here.
def index(request):
    return render(request, 'deprem.html')

def report(request):
    if request.method == 'POST':
        isim = request.POST["isim"]
        sehir = request.POST["sehir"]
        adres = request.POST["adres"]
        durum = request.POST["durum"]
        if "tel" in request.POST:
            tel = request.POST["tel"]
        else:
            tel = "Yok"
    p = Person(isim=isim, sehir=sehir, adres=adres, tel=tel, durum=durum)
    p.save()
    return HttpResponse("Kaydedildi.")

def telKontrol(input):
    if len(input) > 9:
        return True
    else:
        return False

def search(request):
    if request.method == "GET":
        if 'isim' in request.GET and "tel" in request.GET:
            if telKontrol(request.GET.get("tel")):
                reports = Person.objects.filter(isim__icontains=request.GET.get('isim'), tel__contains=request.GET.get('tel'))
            else:
                return HttpResponse("Telefon numarası en az 10 hane girilmeli.")
        else:
            if 'isim' in request.GET:
                reports = Person.objects.filter(isim__icontains=request.GET.get('isim')).order_by('created_at')[:10]
            elif 'tel' in request.GET:
                if telKontrol(request.GET.get("tel")):
                    reports = Person.objects.filter(tel__contains=request.GET.get('tel')).order_by('created_at')[:10]
                else:
                    return HttpResponse("Telefon numarası en az 10 hane girilmeli.")
            else:
                reports = Person.objects.order_by('created_at')[:50]
        rlist = serialize('json', reports, fields=["isim", "sehir", "adres", "durum", "created_at"])
        return HttpResponse(rlist)
