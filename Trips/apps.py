from django.apps import AppConfig


class TripsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Trips'

    def ready(self):
        from . import signals