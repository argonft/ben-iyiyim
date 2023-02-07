from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.shortcuts import render
from .models import Person
from django.db.models import Q
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

def search(request):
    fs = ["isim", "sehir", "adres", "durum"]
    if request.method == "GET":
        if 'isim' in request.GET and "tel" in request.GET:
            if len(request.GET.get('tel')) > 5:
                reports = Person.objects.filter(isim__icontains=request.GET.get('isim'), tel__contains=request.GET.get('tel'))
                fs.append("tel")
        else:
            if 'isim' in request.GET:
                reports = Person.objects.filter(isim__icontains=request.GET.get('isim')).order_by('created_at')[:10]
            if 'tel' in request.GET:
                if len(request.GET.get('tel')) > 5:
                    reports = Person.objects.filter(tel__contains=request.GET.get('tel')).order_by('created_at')[:10]
                    fs.append("tel")
                else:
                    return HttpResponse("Telefon numarası en az 6 hane girilmeli.")
        if reports is None:
            reports = Person.objects.order_by('created_at')[:50]
        rlist = serialize('json', reports, fields=fs)
        return HttpResponse(rlist)