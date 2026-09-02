from . import views
from django.urls import include
from django.contrib import admin
from django.urls import path
 
urlpatterns = [
    path('', views.usa_home,name="usa_home"),
    path('about/', views.usa_about,name="usa_about"),
    path('services/', views.usa_services,name="usa_service"),
    path('website_development/', views.usa_web,name="usa_web"),
    path('seo/', views.usa_seo,name="usa_seo"),
    path('smm/', views.usa_smm,name="usa_smm"),
    path('custom_software/', views.usa_sd,name="usa_sd"),
    path('digital_marketing/', views.usa_dm,name="usa_dm"),
    path('technical-consultancy/', views.usa_ts,name="usa_ts"),
    path('contact/', views.usa_contact,name="usa_contact"),

    
    
]