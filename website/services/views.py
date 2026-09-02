from django.shortcuts import render
from home.views import subs

# Create your views here.
def services(request):
    a = subs(request)
    return render(request,"service.html")

def web_development(request):
    return render(request,"services/new-soft.html")


def app_development(request):
    return render(request,"services/new-app.html")


def digital_marketing(request):
    return render(request,"services/new-digital.html")

def ui_ux(request):
    return render(request,"services/new-ui.html")

def new_soft1(request):
    return render(request,"services/new-software.html")

def new_consult(request):
    return render(request,"services/new-consult.html")

