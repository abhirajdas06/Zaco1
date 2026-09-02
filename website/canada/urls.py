from . import views
from django.urls import include
from django.contrib import admin
from django.urls import path
 
urlpatterns = [
    path('', views.canada_home,name="canada_home"),
    path('about/', views.canada_about,name="canada_about"),
    path('services/', views.canada_services,name="canada_service"),
    path('website_development/', views.canada_web,name="canada_web"),
    path('seo/', views.canada_seo,name="canada_seo"),
    path('smm/', views.canada_smm,name="canada_smm"),
    path('custom_software/', views.canada_sd,name="canada_sd"),
    path('digital_marketing/', views.canada_dm,name="canada_dm"),
    path('technical-consultancy/', views.canada_tc,name="canada_tc"),
    path('contact/', views.canada_contact,name="canada_contact"),

    
    
]