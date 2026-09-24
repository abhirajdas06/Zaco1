import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from blog.models import Post
from .forms import ContactForm, SubscibersForm
from .models import Contact, Subscribers

logger = logging.getLogger(__name__)


def _notify_team(subject, body, reply_to=None):
    """Email the lead recipients. Never raises: the lead is already saved in
    the database, so an SMTP outage must not turn into a 500 for the visitor.
    Returns True if the mail was handed to the mail server."""
    try:
        EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=settings.LEAD_NOTIFICATION_EMAILS,
            reply_to=[reply_to] if reply_to else None,
        ).send(fail_silently=False)
        return True
    except Exception:
        logger.exception('Could not send lead notification email: %s', subject)
        return False


def _safe_next(request, default):
    """Where to send the visitor back to after a form post (open-redirect safe)."""
    target = request.POST.get('next') or request.META.get('HTTP_REFERER') or default
    if url_has_allowed_host_and_scheme(
        target, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return target
    return default


# Create your views here.
def index(request):
    return render(request,"index-6.html")

def about(request):
    return render(request,"about.html")

def service(request):
    return render(request,"canada/service.html")


def contact(request):
    """Contact page (GET) and the endpoint every contact/enquiry form posts to."""
    if request.method != "POST":
        return render(request, "contact.html")

    back = _safe_next(request, '/contact')
    form = ContactForm(request.POST)

    if not form.is_valid():
        # Spam bots get a silent success so they don't learn what tripped us.
        if 'website' in form.errors:
            return redirect(back)
        first_error = next(iter(form.errors.values()))[0]
        messages.error(request, f"Please check the form and try again. {first_error}")
        return redirect(back)

    data = form.cleaned_data
    enquiry = data['message'] or '(no message provided)'
    Contact.objects.create(
        name=data['name'], email=data['mail'], phone=data['phone'],
        subject=data['subject'], message=enquiry,
    )

    _notify_team(
        subject=f"Website enquiry: {data['subject']} - {data['name']}",
        body="\n".join([
            f"Name: {data['name']}",
            f"Email: {data['mail']}",
            f"Phone: {data['phone']}",
            f"Subject: {data['subject']}",
            f"Page: {request.META.get('HTTP_REFERER', 'unknown')}",
            f"Ad tracking: {data['tracking'] or 'none'}",
            "",
            "Message:",
            enquiry,
        ]),
        reply_to=data['mail'],
    )

    messages.success(
        request,
        "Thank you for your submission. A member of our team will be in touch with you shortly.",
        extra_tags='lead',
    )
    return redirect(back)


@require_POST
def subscribe(request):
    """Newsletter signup - the target of every 'Enter your email address' form."""
    back = _safe_next(request, '/')
    form = SubscibersForm(request.POST)

    if not form.is_valid():
        messages.error(request, "Please enter a valid email address.")
        return redirect(back)

    email = form.cleaned_data['email']
    _, created = Subscribers.objects.get_or_create(email=email)
    if created:
        _notify_team(
            subject=f"New newsletter subscriber: {email}",
            body=f"{email} subscribed to the newsletter from {request.META.get('HTTP_REFERER', 'the website')}.",
            reply_to=email,
        )
    messages.success(request, "Subscription Successful")
    return redirect(back)


def technologies(request):
    return render(request,"technologies/technologies.html") 

def frontend(request):
    return render(request,"technologies/frontend.html") 

def backend(request):
    return render(request,"technologies/backend.html") 

def database(request):
    return render(request,"technologies/database.html") 

def solutions(request):
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