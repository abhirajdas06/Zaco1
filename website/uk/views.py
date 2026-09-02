from django.shortcuts import render

# Create your views here.
def uk_home(request):
    return render(request,'uk/index.html')

def uk_services(request):
    return render(request,"uk/uk-services.html")

def uk_about(request):
    return render(request,"uk/about.html")

def uk_web(request):
    return render(request,"uk/uk-webdevelopment.html")

def uk_seo(request):
    return render(request,"uk/uk_seo.html")

def uk_smm(request):
    return render(request,"uk/uk_smm.html")

def uk_sd(request):
    return render(request,"uk/uk_sd.html")

def uk_dm(request):
    return render(request,"uk/uk_dm.html")

def uk_tc(request):
    return render(request,"uk/uk_tc.html")

def uk_contact(request):
    return render(request,"uk/uk_contact.html")
