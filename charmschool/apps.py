from django.apps import AppConfig


class CharmschoolConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'charmschool'
    def ready(self):
        import charmschool.signals
