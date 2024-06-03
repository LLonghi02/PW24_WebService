from django.http import JsonResponse # type: ignore
from .models import Cittadino, Ospedale, Ricovero, Patologia, PatologiaRicovero, PatologiaCronica, PatologiaMortale

def cittadini_list(request):
    cittadini = list(Cittadino.objects.values())
    return JsonResponse(cittadini, safe=False)

def ospedali_list(request):
    ospedali = list(Ospedale.objects.values())
    return JsonResponse(ospedali, safe=False)

def ricoveri_list(request):
    ricoveri = list(Ricovero.objects.values())
    return JsonResponse(ricoveri, safe=False)

def patologie_list(request):
    patologie = list(Patologia.objects.values())
    return JsonResponse(patologie, safe=False)

def patologie_ricovero_list(request):
    patologie_ricovero = list(PatologiaRicovero.objects.values())
    return JsonResponse(patologie_ricovero, safe=False)

def patologie_croniche_list(request):
    patologie_croniche = list(PatologiaCronica.objects.values())
    return JsonResponse(patologie_croniche, safe=False)

def patologie_mortali_list(request):
    patologie_mortali = list(PatologiaMortale.objects.values())
    return JsonResponse(patologie_mortali, safe=False)
