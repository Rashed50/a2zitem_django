from django.apps import AppConfig


class ClientpageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clientpage'
    verbose_name = 'Client Page'
    
    def ready(self):
        pass
