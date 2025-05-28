from django.apps import AppConfig

class GasManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gas_management'
    
    def ready(self):
        import gas_management.signals
