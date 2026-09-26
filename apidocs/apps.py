from django.apps import AppConfig


class ApidocsConfig(AppConfig):
    # App exclusivo da plataforma de APIs.
    # Não possui models nem migrações: não altera o banco compartilhado.
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apidocs'
    verbose_name = 'Documentação das APIs'
