from django.apps import AppConfig


class TutorappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tutorapp'

    def ready(self):
        import tutorapp.signals

def ready(self):
    import tutorapp.signals