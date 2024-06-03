"""
URL configuration for myproject project.

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
from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from myapp.views import ( # type: ignore
    cittadini_list,
    ospedali_list,
    ricoveri_list,
    patologie_list,
    patologie_ricovero_list,
    patologie_croniche_list,
    patologie_mortali_list,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cittadini/', cittadini_list),
    path('ospedali/', ospedali_list),
    path('ricoveri/', ricoveri_list),
    path('patologie/', patologie_list),
    path('patologie_ricovero/', patologie_ricovero_list),
    path('patologie_croniche/', patologie_croniche_list),
    path('patologie_mortali/', patologie_mortali_list),
]
