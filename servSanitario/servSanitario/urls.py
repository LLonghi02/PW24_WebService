
from django.contrib import admin
from django.urls import path
from servSanitario import views


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
