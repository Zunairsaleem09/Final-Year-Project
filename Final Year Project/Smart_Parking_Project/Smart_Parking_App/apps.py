from django.apps import AppConfig


class SmartParkingAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Smart_Parking_App"

    def ready(self):
        import Smart_Parking_App.signals