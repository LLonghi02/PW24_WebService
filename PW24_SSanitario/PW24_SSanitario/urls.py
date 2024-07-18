# importer/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('receive-data/', views.receive_data, name='receive_data'),
    # Aggiungi altre viste URL se necessario
]
