from . import views
from django.urls import include
from django.contrib import admin
from django.urls import path
 
urlpatterns = [
    path('', views.uk_home,name="uk_home"),
    path('about/', views.uk_about,name="uk_about"),
    path('services/', views.uk_services,name="uk_service"),
    path('website_development/', views.uk_web,name="uk_web"),
    path('seo/', views.uk_seo,name="uk_seo"),
    path('smm/', views.uk_smm,name="uk_smm"),
    path('custom_software/', views.uk_sd,name="uk_sd"),
    path('digital_marketing/', views.uk_dm,name="uk_dm"),
    path('technical-consultancy/', views.uk_tc,name="uk_tc"),
    path('contact/', views.uk_contact,name="uk_contact"),

    
    
]