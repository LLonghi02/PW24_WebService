#Classe per forzare la non creazione delle tabelle di Django utilizzate per operazioni di "Servizio"
class CustomRouter:
    def db_for_read(self, model, **hints):
        return None

    def db_for_write(self, model, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in ['auth', 'admin', 'contenttypes', 'sessions']: #Se è presente una delle seguenti parole nel nome della tabella, non viene eseguita la sua migrazione
            return False
        return True