from wsgiref.util import request_uri
from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from .forms import SubscibersForm
from website.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from blog.models import Post


# home canada

#newsletter
def subs(request):   
    if request.method == 'POST':
        form = SubscibersForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Subscription Successful')
            return redirect('/')

    else:
        form = SubscibersForm()
        context = {
        'form': form,
        }
        


# Create your views here.
def index(request):
    a = subs(request)
    return render(request,"index-6.html")

def about(request):
    a = subs(request)
    return render(request,"about.html")

def service(request):
    a = subs(request)
    return render(request,"canada/service.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('mail')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if len(name) < 2 or len(email) < 3 or len(subject) < 2:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact.objects.create(name=name, email=email, phone=phone, subject=subject, message=message)
            contact.save()

            # Sending email (your existing code)
            emailhead = 'Inquiry from Zaco Infotech Website'
            newline = '\n'
            emailmessage = f"Name: {name}{newline}Email: {email}{newline}Contact: {phone}{newline}Subject: {subject}{newline}Inquiry: {message}"
            from_email = 'noreply@zacoinfotech.com'
            send_mail(emailhead, emailmessage, from_email, ['info@zacoinfotech.com'], fail_silently=False)

            messages.success(request, "Thank you for your submission. A member of our team will be in touch with you shortly.")

            return redirect('/contact')
    else:
        return render(request, "contact.html")

        


def technologies(request):
    a = subs(request)
    return render(request,"technologies/technologies.html") 

def frontend(request):
    return render(request,"technologies/frontend.html") 

def backend(request):
    return render(request,"technologies/backend.html") 

def database(request):
    return render(request,"technologies/database.html") 

def solutions(request):
    a = subs(request)
    return render(request,"") 

def asset_management(request):
    return render(request,"services/asset-management.html")



def terms_conditions(request):
    return render(request,"terms-condition.html")

def faq(request):
    return render(request,"faq.html")

def new_hosting(request):
    return render(request,"hosting.html")

def web_hosting_plus(request):
    return render(request,"web_hosting_plus.html")

def web_hosting(request):
    return render(request,"web_hosting.html")

def shared_hosting(request):
    return render(request,"shared_hosting.html")


def search(request):    
    query=request.GET['query']
    
    if len(query)>5:
        post_list= []
    else:
        post_listTitle= Post.objects.filter(title__icontains=query)
        post_listContent= Post.objects.filter(content__icontains=query)
        # post_listCategory= Post.objects.filter(category__icontains=query)
        post_list= post_listTitle.union(post_listContent)
        
    params={'post_list': post_list, 'query':query}
    return render(request,"search.html", params)  

# def web_dev(request):
#     return render(request,"web-dev.html")

# def app_dev(request):
#     return render(request,"app-dev.html")

# def digital_marketing(request):
#     return render(request,"digital-marketing.html")

# def tech_consultation(request):
#     return render(request,"tech-consult.html")

# def dg_m(request):
#     return render(request,"dg-m.html")

def android_app(request):
    return render(request,"services/android-app.html")
    
def ecommerce(request):
    return render(request,"services/ecommerce-dev.html")

def form(request):
    return render(request,"contact-form.html")