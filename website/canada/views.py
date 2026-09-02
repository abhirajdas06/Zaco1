from django.shortcuts import render

# Create your views here.
def canada_home(request):
    return render(request,'canada/index.html')

def canada_services(request):
    return render(request,"canada/canada-services.html")

def canada_about(request):
    return render(request,"canada/about.html")

def canada_web(request):
    return render(request,"canada/canada-webdevelopment.html")

def canada_seo(request):
    return render(request,"canada/canada_seo.html")

def canada_smm(request):
    return render(request,"canada/canada_smm.html")

def canada_sd(request):
    return render(request,"canada/canada_sd.html")

def canada_dm(request):
    return render(request,"canada/canada_dm.html")

def canada_tc(request):
    return render(request,"canada/canada-tc.html")

def canada_contact(request):
    return render(request,"canada/canada_contact.html")
