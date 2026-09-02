from . import views
from django.urls import path
from django.urls import include


urlpatterns = [
    path('', views.PostList.as_view(), name='blog'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='blog-single'),
    path('summernote/', include('django_summernote.urls')),

]