from django.apps import AppConfig

class AcademicsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.academics'  # Nome completo para o Django localizar a pasta
    label = 'academics'      # Identificador único para o banco de dados