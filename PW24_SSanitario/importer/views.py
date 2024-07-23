
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import JsonResponse
from .models import Cittadino, Ospedale, Ricovero, Patologia, PatologiaRicovero, PatologiaCronica, PatologiaMortale
import json
import logging

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

logger = logging.getLogger(__name__)

@csrf_exempt
def fetch_and_save(request):
    logger.info(f"Ricevuta una richiesta: {request.method}")

    if request.method == 'POST':
        logger.info("È una richiesta POST")
        # URL del web service remoto per ottenere i dati
        remote_url = 'https://servsanitariopw9.altervista.org/WS.php'

        try:
            # Effettua una richiesta POST per ottenere i dati
            response = requests.get(remote_url)
            response.raise_for_status()  # Solleva un'eccezione se la richiesta non ha successo
            data = response.json()

            # Inserisci i dati per il modello Cittadino
            for item in data.get('cittadini', []):
                Cittadino.objects.create(
                    CSSN=item['CSSN'],
                    nome=item['nome'],
                    cognome=item['cognome'],
                    dataNascita=item['dataNascita'],
                    luogoNascita=item['luogoNascita'],
                    indirizzo=item['indirizzo']
                )

            # Inserisci i dati per il modello Ospedale
            for item in data.get('ospedali', []):
                Ospedale.objects.create(
                    codice=item['codice'],
                    nome=item['nome'],
                    città=item['città'],
                    indirizzo=item['indirizzo'],
                    direttoreSanitario=item['direttoreSanitario']
                )

            # Inserisci i dati per il modello Ricovero
            for item in data.get('ricoveri', []):
                codOspedale = Ospedale.objects.get(codice=item['codOspedale'])
                paziente = Cittadino.objects.get(CSSN=item['paziente'])
                Ricovero.objects.create(
                    codOspedale=codOspedale,
                    cod=item['cod'],
                    paziente=paziente,
                    data=item['data'],
                    durata=item['durata'],
                    motivo=item['motivo'],
                    costo=item['costo']
                )

            # Inserisci i dati per il modello Patologia
            for item in data.get('patologie', []):
                Patologia.objects.create(
                    cod=item['cod'],
                    nome=item['nome'],
                    criticità=item['criticità']
                )

            # Inserisci i dati per il modello PatologiaRicovero
            for item in data.get('patologie_ricovero', []):
                codOspedale = Ospedale.objects.get(codice=item['codOspedale'])
                codRicovero = Ricovero.objects.get(cod=item['codRicovero'])
                codPatologia = Patologia.objects.get(cod=item['codPatologia'])
                PatologiaRicovero.objects.create(
                    codOspedale=codOspedale,
                    codRicovero=codRicovero,
                    codPatologia=codPatologia
                )

            # Inserisci i dati per il modello PatologiaCronica
            for item in data.get('patologie_croniche', []):
                codPatologia = Patologia.objects.get(cod=item['codPatologia'])
                PatologiaCronica.objects.create(
                    codPatologia=codPatologia
                )

            # Inserisci i dati per il modello PatologiaMortale
            for item in data.get('patologie_mortali', []):
                codPatologia = Patologia.objects.get(cod=item['codPatologia'])
                PatologiaMortale.objects.create(
                    codPatologia=codPatologia
                )

            return JsonResponse({"status": "dati migrati con successo"})
        except requests.RequestException as e:
            return JsonResponse({"status": "errore nel recupero dei dati", "error": str(e)}, status=500)
        except Exception as e:
            return JsonResponse({"status": "errore durante l'inserimento dei dati", "error": str(e)}, status=500)
    else:
        logger.info("Non è una richiesta POST")
        return JsonResponse({"status": "Metodo non supportato"}, status=405)
