from django.apps import AppConfig


class DbLoggerAppConfig(AppConfig):
    name = 'django_db_logger'
    verbose_name = "Database Logging"
    verbose_name_plural = "Database Logging"
    # Explicitly set default auto field type to avoid migrations in Django 3.2+
    default_auto_field = "django.db.models.AutoField"
