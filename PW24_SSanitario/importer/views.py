# importer/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Cittadino, Ospedale, Patologia, Ricovero, PatologiaRicovero
import json

@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Salvataggio dei dati ricevuti nel modello corrispondente
            
            # Esempio per Cittadino
            cittadino = Cittadino.objects.create(
                CSSN=data['CSSN'],
                nome=data['nome'],
                cognome=data['cognome'],
                dataNascita=data['dataNascita'],
                luogoNascita=data['luogoNascita'],
                indirizzo=data['indirizzo']
            )

            # Esempio per Ospedale
            ospedale = Ospedale.objects.create(
                codice=data['codice'],
                nome=data['nome'],
                città=data['città'],
                indirizzo=data['indirizzo'],
                direttoreSanitario_id=data['direttoreSanitario']
            )

            # E così via per gli altri modelli
            
            return JsonResponse({'message': 'Dati ricevuti e salvati con successo.'})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    else:
        return JsonResponse({'error': 'Richiesta non consentita.'}, status=405)
