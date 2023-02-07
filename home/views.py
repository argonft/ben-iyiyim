from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.shortcuts import render, redirect
from .models import Person
from django.contrib import messages
import re

# Create your views here.
def index(request):
    return render(request, 'deprem.html')


def report(request):
    if request.method == 'POST':
        isim = request.POST["isim"]
        isim = "".join(x for x in isim if x.isalpha())
        sehir = request.POST["sehir"]
        sehir = "".join(x for x in sehir if x.isalpha())
        adres = request.POST["adres"]
        adres = "".join(x for x in adres if x.isalpha())
        durum = request.POST["durum"]
        durum = "".join(x for x in durum if x.isalpha())
        if "tel" in request.POST:
            tel = request.POST["tel"]
            tel = "".join(x for x in tel if x.isalpha())
        else:
            tel = "Yok"
    p = Person(isim=isim, sehir=sehir, adres=adres, tel=tel, durum=durum)
    p.save()
    messages.success(request, 'Kaydedildi.')

    return redirect('index')

def telKontrol(input):
    if re.match("^[A-Za-z0-9_-]*$", input) and len(input) > 9:
        return True
    else:
        return False

def isimKontrol(input):
    if re.match("^[A-Za-z0-9_-]*$", input) and len(input) > 2:
        return True
    else:
        return False

def search(request):
    if request.method == "GET":
        if 'isim' in request.GET and "tel" in request.GET:
            isim = request.GET.get('isim')
            tel = request.GET.get('tel')
            if telKontrol(tel) and isimKontrol(isim):
                reports = Person.objects.filter(isim__icontains=isim, tel__contains=tel)
            else:
                return HttpResponse("Input hatalı.")
        else:
            if 'isim' in request.GET:
                isim = request.GET.get('isim')
                if isimKontrol(isim):
                    reports = Person.objects.filter(isim__icontains=isim).order_by('created_at')[:10]
                else:
                    return HttpResponse("İsim en az 3 karakter olmalı.")
            elif 'tel' in request.GET:
                tel = request.GET.get('tel')
                print(tel)
                if telKontrol(tel):
                    reports = Person.objects.filter(tel__contains=tel).order_by('created_at')[:10]
                else:
                    return HttpResponse("Telefon numarası en az 10 hane girilmeli.")
            else:
                return HttpResponse("Arama yapmak için veri girişi yapın.")
        rlist = serialize('json', reports, fields=["isim", "sehir", "adres", "durum", "created_at"])
        return JsonResponse(rlist)
