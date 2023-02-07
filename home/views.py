from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.core.serializers import serialize
from django.shortcuts import render, redirect
from .models import Person
from django.contrib import messages
from django.utils.html import format_html
import re

def remove_html_markup(s):
    clean = re.compile('<.*?>')
    return str(re.sub(clean, '', str(s)))

def telKontrol(input):
    if re.match("^[0-9]+$", input) and len(input) > 9:
        return True
    else:
        return False

def textKontrol(input):
    if len(input) > 2:
        return True
    else:
        return False

# Create your views here.
def index(request):
    return render(request, 'deprem.html')

def report(request):
    if request.method == 'POST':
        isim = remove_html_markup(format_html(request.POST["isim"]))
        sehir = remove_html_markup(format_html(request.POST["sehir"]))
        adres = remove_html_markup(format_html(request.POST["adres"]))
        durum = remove_html_markup(format_html(request.POST["durum"]))
        if "tel" in request.POST:
            tel = request.POST["tel"]
        else:
            tel = "Yok"
        if telKontrol(tel) and textKontrol(isim) and textKontrol(sehir) and textKontrol(adres) and textKontrol(durum):
            p = Person(isim=isim, sehir=sehir, adres=adres, tel=tel, durum=durum)
            p.save()
            messages.success(request, 'Kaydedildi.')
        else:
            return HttpResponseBadRequest("Giriş yapılan bilgilerde desteklenmeyen karakterler var.")
    return redirect('index')

def search(request):
    if request.method == "GET":
        if 'isim' in request.GET and "tel" in request.GET:
            isim = remove_html_markup(format_html(request.GET.get('isim')))
            tel = remove_html_markup(format_html(request.GET.get('tel')))
            if len(isim) > 2 and telKontrol(tel):
                reports = Person.objects.filter(isim__icontains=isim, tel__contains=tel)
            else:
                return HttpResponseBadRequest("Input hatalı.")
        else:
            if 'isim' in request.GET:
                isim = format_html(request.GET.get('isim'))
                print(len(isim))
                if len(isim) > 2:
                    reports = Person.objects.filter(isim__icontains=isim).order_by('created_at')[:10]
                else:
                    return HttpResponseBadRequest('İsim 2 karakterden uzun olmalı.')
            elif 'tel' in request.GET:
                tel = format_html(request.GET.get('tel'))
                if telKontrol(tel):
                    reports = Person.objects.filter(tel__contains=tel).order_by('created_at')[:10]
                else:
                    return HttpResponseBadRequest("Telefon numarası bilgileri hatalı.")
            else:
                return HttpResponse("Arama yapmak için veri girişi yapın.")
        rlist = serialize('json', reports, fields=["isim", "sehir", "adres", "durum", "created_at"], use_natural_primary_keys=True)
        return HttpResponse(rlist, content_type="application/json")
