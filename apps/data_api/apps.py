from django.apps import AppConfig


class DataApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.data_api'

    def ready(self):
        from .scheduler import schedule_job
        schedule_job()
