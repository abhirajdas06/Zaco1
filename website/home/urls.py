from home import views
from django.urls import include
from django.contrib import admin
from django.urls import path
 
urlpatterns = [

    path('', views.index,name="home"),
    path('about', views.about,name="about"),
    path('contact', views.contact, name="contact"),
    path('subscribe', views.subscribe, name="subscribe"),
    path('thank-you', views.thank_you, name="thank_you"),
    path('technologies', views.technologies, name="technologies"),
    path('technologies/frontend', views.frontend, name="frontend"),
    path('technologies/backend', views.backend, name="backend"),
    path('technologies/database', views.database, name="database"),
    path('solutions', views.solutions, name="solutions"),
    path('solutions/asset-management', views.asset_management, name="asset-management"),
    path('blog/', include('blog.urls')),
    path('blog/search', views.search, name="search"),
    path('terms-and-conditions', views.terms_conditions, name="terms_conditions"),
    path('faq', views.faq, name="faq"),
    path('hosting', views.new_hosting, name="hosting"),
    path('web_hosting_plus', views.web_hosting_plus, name="web_hosting_plus"),
    path('web_hosting', views.web_hosting, name="web_hosting"),
    path('shared_hosting',views.shared_hosting,name='shared_hosting'),
    # path('software', views.software, name="software"),
    # path('web-dev', views.web_dev, name="web-dev"),
    # path('app-dev',views.app_dev, name="app-dev"),
    # path('digital-marketing',views.digital_marketing,name="digital-marketing",),
    # path('tech-consult',views.tech_consultation,name="tech-consult",),
    # path('dg-m', views.dg_m, name="dg-m"),
    path('android-app', views.android_app, name="android-app"),
    path('ecommerce', views.ecommerce, name="ecommerce"),
    path('form', views.form, name="form"),
]