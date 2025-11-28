from django.apps import AppConfig


# Ready method to import signals
class EmployeesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employees'





    def ready(self):
        import employees.signals
