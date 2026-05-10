class AuthRouter:
    router_app_labels = {'auth', 'contenttypes', 'sessions', 'admin'}
    session_models = {'alumnosession'}

    def db_for_read(self, model, **hints):
        if model._meta.model_name in self.session_models:
            return 'session'
        if model._meta.app_label in self.router_app_labels:
            return 'default'
        return 'default'
    
    def db_for_write(self, model, **hints):
        if model._meta.model_name in self.session_models:
            return 'session'
        if model._meta.app_label in self.router_app_labels:
            return 'default'
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.router_app_labels or
            obj2._meta.app_label in self.router_app_labels
        ):
            return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name in self.session_models:
            return db == 'session'
        if app_label in self.router_app_labels:
            return db == 'default'
        if db == 'session':
            return False
        return db == 'default'