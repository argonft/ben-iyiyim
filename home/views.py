from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.shortcuts import render
from .models import Person
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
    if request.method == "GET":
        if 'isim' in request.GET:
            reports = Person.objects.defer("tel").filter(isim__contains=request.GET.get('isim')).order_by('created_at')[:10]
        elif 'tel' in request.GET:
            if len(request.GET.get('tel')) > 5:
                reports = Person.objects.filter(tel__contains=request.GET.get('tel')).order_by('created_at')[:10]
        else:
            reports = Person.objects.defer("tel").order_by('created_at')[:50]
        rlist = serialize('json', reports)
        return HttpResponse(rlist)