from django.http import HttpResponse
from django.shortcuts import render
from .models import Person

# Create your views here.
def index(request):
    return render(request, 'staticfiles/index.html')

def report(request):
    if request.method == 'POST':
        name = request.POST["name"]
        sehir = request.POST["sehir"]
        adres = request.POST["adres"]
        durum = request.POST["durum"]
        if "tel" in request.POST:
            tel = request.POST["tel"]
        else:
            tel = "Yok"
    p = Person(isim=name, sehir=sehir, adres=adres, tel=tel, durum=durum)
    p.save()