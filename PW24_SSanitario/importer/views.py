
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import JsonResponse
from .models import Cittadino, Ospedale, Ricovero, Patologia, PatologiaRicovero, PatologiaCronica, PatologiaMortale
import json
import logging
from django.http import HttpResponse
from django.core.management import call_command

"""def cittadini_list(request):
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
    return JsonResponse(patologie_mortali, safe=False)"""

logger = logging.getLogger(__name__) #creazione dell'oggetto per generare messaggi sul log

def migrate(request):
    call_command('migrate')
    return HttpResponse("Migrazioni eseguite con successo!")

@csrf_exempt
def fetch_and_save(request):
    logger.info(f"Ricevuta una richiesta: {request.method}")

    if request.method == 'POST':
        logger.info("È una richiesta POST")
        # URL del web service remoto per ottenere i dati
        #remote_url = 'https://servsanitariopw9.altervista.org/WS.php'

        try:
            #Effettua una richiesta POST per ottenere i dati
            #response = requests.get(remote_url)
            #response.raise_for_status()  # Solleva un'eccezione se la richiesta non ha successo
            data = json.loads(request.body)
            #data = response.json()

            # Inserisci i dati per il modello Cittadino
            for cittadino_data in data.get('cittadini', []):
                Cittadino.objects.update_or_create(
                    CSSN=cittadino_data.get('CSSN'),
                    defaults={
                        'nome': cittadino_data.get('nome'),
                        'cognome': cittadino_data.get('cognome'),
                        'dataNascita': cittadino_data.get('dataNascita'),
                        'luogoNascita': cittadino_data.get('luogoNascita'),
                        'indirizzo': cittadino_data.get('indirizzo')
                    }
                )

            # Inserisci i dati per il modello Ospedale
            for ospedale_data in data.get('ospedali', []):
                Ospedale.objects.update_or_create(
                    codice=ospedale_data.get('codice'),
                    defaults={
                        'nome': ospedale_data.get('nome'),
                        'città': ospedale_data.get('città'),
                        'indirizzo': ospedale_data.get('indirizzo'),
                        'direttoreSanitario': Cittadino.objects.get(CSSN=ospedale_data.get('direttoreSanitario'))
                    }
                )

            # Inserisci i dati per il modello Ricovero
            for ricovero_data in data.get('ricoveri', []):
                Ricovero.objects.update_or_create(
                    cod=ricovero_data.get('cod'),
                    defaults={
                        'codOspedale': Ospedale.objects.get(codice=ricovero_data.get('codOspedale')),
                        'paziente': Cittadino.objects.get(CSSN=ricovero_data.get('paziente')),
                        'date': ricovero_data.get('date'),
                        'durata': ricovero_data.get('durata'),
                        'motivo': ricovero_data.get('motivo'),
                        'costo': ricovero_data.get('costo')
                    }
                )

            # Inserisci i dati per il modello Patologia
            for patologia_data in data.get('patologie', []):
                Patologia.objects.update_or_create(
                    cod=patologia_data.get('cod'),
                    defaults={
                        'nome': patologia_data.get('nome'),
                        'criticità': patologia_data.get('criticità')
                    }
                )

            # Inserisci i dati per il modello PatologiaRicovero
            for patologia_ricovero_data in data.get('patologie_ricoveri', []):
                PatologiaRicovero.objects.update_or_create(
                    codOspedale=Ospedale.objects.get(codice=patologia_ricovero_data.get('codOspedale')),
                    codRicovero=Ricovero.objects.get(cod=patologia_ricovero_data.get('codRicovero')),
                    codPatologia=Patologia.objects.get(cod=patologia_ricovero_data.get('codPatologia'))
                )

            # Inserisci i dati per il modello PatologiaCronica
            for patologia_cronica_data in data.get('patologie_croniche', []):
                PatologiaCronica.objects.update_or_create(
                    codPatologia=Patologia.objects.get(cod=patologia_cronica_data.get('codPatologia')),
                )

            # Inserisci i dati per il modello PatologiaMortale
            for patologia_mortale_data in data.get('patologie_mortali', []):
                PatologiaMortale.objects.update_or_create(
                    codPatologia=Patologia.objects.get(cod=patologia_mortale_data.get('codPatologia')),
                )
            
            #response = requests.get('http://localhost:8000/run-migrations/')
            #print(response.text)

            return JsonResponse({"status": "dati migrati con successo"})
        except requests.RequestException as e:
            return JsonResponse({"status": "errore nel recupero dei dati", "error": str(e)}, status=500)
        except Exception as e:
            return JsonResponse({"status": "errore durante l'inserimento dei dati", "error": str(e)}, status=500)
    else:
        logger.info("Non è una richiesta POST")
        return JsonResponse({"status": "Metodo non supportato"}, status=405)
