from django.shortcuts import render

# Create your views here.
def usa_home(request):
    return render(request,'usa/index.html')

def usa_services(request):
    return render(request,"usa/usa-services.html")

def usa_about(request):
    return render(request,"usa/about.html")

def usa_web(request):
    return render(request,"usa/usa-webdevelopment.html")

def usa_seo(request):
    return render(request,"usa/usa_seo.html")

def usa_smm(request):
    return render(request,"usa/usa_smm.html")

def usa_ts(request):
    return render(request,"usa/usa_ts.html")

def usa_sd(request):
    return render(request,"usa/usa_sd.html")

def usa_dm(request):
    return render(request,"usa/usa_dm.html")

def usa_contact(request):
    return render(request,"usa/usa_contact.html")
