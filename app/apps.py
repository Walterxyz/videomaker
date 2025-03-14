from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        from jobs import updater
        from .models import Servidor, AcessoServidores
        
        updater.att_servers(Servidor)
        updater.att_slots(AcessoServidores.objects.filter(inslots=True))
