from django.apps import AppConfig


class ImcConfig(AppConfig):
    name = 'imc'

    def ready(self):
        import imc.signals
