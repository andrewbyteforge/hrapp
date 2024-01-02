# logging_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('log/', views.log_message, name='log_message'),   
    path('error_page', views.error_page, name='error_page'),  
]
