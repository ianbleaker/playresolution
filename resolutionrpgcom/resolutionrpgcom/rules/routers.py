class RulesRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'rules':
            return 'rules'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'rules':
            return 'rules'
        return None

    def allow_relations(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'rules' or obj2._meta.app_label == 'rules':
            return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        if app_label == 'rules':
            return db == 'rules'
        return False