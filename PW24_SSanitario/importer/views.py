
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import JsonResponse
from .models import Cittadino, Ospedale, Ricovero, Patologia, PatologiaRicovero, PatologiaCronica, PatologiaMortale
import json
import logging
from django.http import HttpResponse
from django.core.management import call_command


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

        # Variabile per tenere traccia dei dati salvati
        dati_migrati = {
            "Cittadino": [],
            "Ospedale": [],
            "Patologia": [],
            "PatologiaCronica": [],
            "PatologiaMortale": [],
            "Ricovero": [],
            "PatologiaRicovero": []
        }

        try:
            #Effettua una richiesta POST per ottenere i dati
            #response = requests.get(remote_url)
            #response.raise_for_status()  # Solleva un'eccezione se la richiesta non ha successo
            response = requests.get('http://localhost:8000/run-migrations/')
            #print(response.text)

            data = json.loads(request.body)

            print("Dati migrati iniziali:", dati_migrati)

            # Inserisci i dati per il modello Cittadino
            for cittadino_data in data.get('Cittadino', []):  # Assicurati che il nome del campo sia corretto
                ##print("Elaborando cittadino:", cittadino_data)  # Debugging: stampa il cittadino elaborato
                try:
                    cittadino, created = Cittadino.objects.update_or_create(
                        CSSN=cittadino_data.get('CSSN'),
                        defaults={
                            'nome': cittadino_data.get('nome'),
                            'cognome': cittadino_data.get('cognome'),
                            'dataNascita': cittadino_data.get('dataNascita'),
                            'luogoNascita': cittadino_data.get('luogoNascita'),
                            'indirizzo': cittadino_data.get('indirizzo')
                        }
                    )
                    dati_migrati["Cittadino"].append(cittadino_data)
                except Exception as e:
                    print(f"Errore durante l'elaborazione di {cittadino_data}: {e}")
                    return JsonResponse({'error': f"Errore durante l'elaborazione di {cittadino_data}: {e}"}, status=500)
            
            print("Dati migrati cittadini:", dati_migrati)

            # Inserisci i dati per il modello Ospedale
            for ospedale_data in data.get('Ospedale', []):
                try:
                    ospedale, created = Ospedale.objects.update_or_create(
                        codice=ospedale_data.get('codice'),
                        defaults={
                            'nome': ospedale_data.get('nome'),
                            'città': ospedale_data.get('città'),
                            'indirizzo': ospedale_data.get('indirizzo'),
                            'direttoreSanitario': Cittadino.objects.get(CSSN=ospedale_data.get('direttoreSanitario'))
                        }
                    )
                    dati_migrati["Ospedale"].append(ospedale_data)
                except Exception as e:
                    print(f"Errore durante l'elaborazione di {ospedale_data}: {e}")
                    return JsonResponse({'error': f"Errore durante l'elaborazione di {ospedale_data}: {e}"}, status=500)
            
            # Inserisci i dati per il modello Patologia
            for patologia_data in data.get('Patologia', []):
                try:
                    patologia, created = Patologia.objects.update_or_create(
                        cod=patologia_data.get('cod'),
                        defaults={
                            'nome': patologia_data.get('nome'),
                            'criticità': patologia_data.get('criticità')
                        }
                    )
                    dati_migrati["Patologia"].append(patologia_data)
                except Exception as e:
                    print(f"Errore durante l'elaborazione di {patologia_data}: {e}")
                    return JsonResponse({'error': f"Errore durante l'elaborazione di {patologia_data}: {e}"}, status=500)

            # Inserisci i dati per il modello PatologiaCronica
            for patologia_cronica_data in data.get('PatologiaCronica', []):
                try:
                    patologia_cronica, created = PatologiaCronica.objects.update_or_create(
                        codPatologia=Patologia.objects.get(cod=patologia_cronica_data.get('codPatologia')),
                    )
                    dati_migrati["PatologiaCronica"].append(patologia_cronica_data)
                except Exception as e:
                    print(f"Errore durante l'elaborazione di {patologia_cronica_data}: {e}")
                    return JsonResponse({'error': f"Errore durante l'elaborazione di {patologia_cronica_data}: {e}"}, status=500)

            # Inserisci i dati per il modello PatologiaMortale
            for patologia_mortale_data in data.get('PatologiaMortale', []):
                try:
                    patologia_mortale, created = PatologiaMortale.objects.update_or_create(
                        codPatologia=Patologia.objects.get(cod=patologia_mortale_data.get('codPatologia')),
                    )
                    dati_migrati["PatologiaMortale"].append(patologia_mortale_data)
                except Exception as e:
                    print(f"Errore durante l'elaborazione di {patologia_mortale_data}: {e}")
                    return JsonResponse({'error': f"Errore durante l'elaborazione di {patologia_mortale_data}: {e}"}, status=500)
            
            # Inserisci i dati per il modello Ricovero
            for ricovero_data in data.get('Ricovero', []):
                try:
                    ricovero, created = Ricovero.objects.update_or_create(
                        cod=ricovero_data.get('cod'),
                        defaults={
                            'codOspedale': Ospedale.objects.get(codice=ricovero_data.get('codOspedale')),
                            'paziente': Cittadino.objects.get(CSSN=ricovero_data.get('paziente')),
                            'data': ricovero_data.get('data'),
                            'durata': ricovero_data.get('durata'),
                            'motivo': ricovero_data.get('motivo'),
                            'costo': ricovero_data.get('costo')
                        }
                    )
                    dati_migrati["Ricovero"].append(ricovero_data)
                except Exception as e:
                    print(f"Errore durante l'elaborazione di {ricovero_data}: {e}")
                    return JsonResponse({'error': f"Errore durante l'elaborazione di {ricovero_data}: {e}"}, status=500)
            
            # Inserisci i dati per il modello PatologiaRicovero
            for patologia_ricovero_data in data.get('PatologiaRicovero', []):
                try:
                    patologia_ricovero, created = PatologiaRicovero.objects.update_or_create(
                        codOspedale=Ospedale.objects.get(codice=patologia_ricovero_data.get('codOspedale')),
                        codRicovero=Ricovero.objects.get(cod=patologia_ricovero_data.get('codRicovero')),
                        codPatologia=Patologia.objects.get(cod=patologia_ricovero_data.get('codPatologia'))
                    )
                    dati_migrati["PatologiaRicovero"].append(patologia_ricovero_data)
                except Exception as e:
                    print(f"Errore durante l'elaborazione di {patologia_ricovero_data}: {e}")
                    return JsonResponse({'error': f"Errore durante l'elaborazione di {patologia_ricovero_data}: {e}"}, status=500)

            print("Dati migrati:", dati_migrati)

            return JsonResponse({"status": "dati migrati con successo", "dati": dati_migrati})
        except requests.RequestException as e:
            return JsonResponse({"status": "errore nel recupero dei dati", "error": str(e)}, status=500)
        except Exception as e:
            return JsonResponse({"status": "errore durante l'inserimento dei dati", "dati": dati_migrati, "error": str(e)}, status=500)
    else:
        logger.info("Non è una richiesta POST")
        return JsonResponse({"status": "Metodo non supportato"}, status=405)
