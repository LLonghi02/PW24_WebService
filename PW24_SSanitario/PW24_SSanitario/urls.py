"""
URL configuration for django_service project.

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
from importer.views import fetch_and_save
from importer.views import migrate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fetch-and-save/', fetch_and_save, name='fetch_and_save'), #Mapping dell'applicazione per recuperare i dati dalla servlet e salvarli sul database
    path('run-migrations/', migrate, name='run-migrations'), #Mapping della view utilizzata per eseguire la migrazione dei dati]
