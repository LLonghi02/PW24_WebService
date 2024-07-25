class CustomRouter:
    def db_for_read(self, model, **hints):
        return None

    def db_for_write(self, model, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in ['auth', 'admin', 'contenttypes', 'sessions', 'migrations']:
            return False
        return True