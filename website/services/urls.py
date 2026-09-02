from services import views
from django.urls import include
from django.contrib import admin
from django.urls import path
from services import views
 
urlpatterns = [
    path('', views.services, name="services"),
    path('web-development', views.web_development, name="web-development"),
    path('application-development', views.app_development, name="application-development"),
    path('digital-marketing', views.digital_marketing, name="digital-marketing"),
    path('ui-ux', views.ui_ux, name="ui-ux"),
    path('custom-software', views.new_soft1, name="custom-software"),
    path('technical-consultation', views.new_consult, name="technical-consultation"),
    
]