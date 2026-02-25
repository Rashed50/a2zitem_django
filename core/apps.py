from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        pass
        ##? Religion Signals
        # import core.signals.ReligionSignals
        # import core.signals.CountrySignals