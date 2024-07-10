"""
URL configuration for servSanitario project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from appSanitario import views

#from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('migrazione/', views.migrazione_dati, name='migrazione_dati'),
    path('cittadini/', views.cittadini_list, name='cittadini_list'),
    path('ospedali/', views.ospedali_list, name='ospedali_list'),
    path('ricoveri/', views.ricoveri_list, name='ricoveri_list'),
    path('patologie/', views.patologie_list, name='patologie_list'),
    path('patologie-ricovero/', views.patologie_ricovero_list, name='patologie_ricovero_list'),
    path('patologie-croniche/', views.patologie_croniche_list, name='patologie_croniche_list'),
    path('patologie-mortali/', views.patologie_mortali_list, name='patologie_mortali_list'),
    path('migra-dati/', views.migrazione_dati, name='migra-dati'),
]
