"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# imports para trabahar com media
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('zeladorxadministration/', admin.site.urls),
    path('', include('authenticate.urls')),
    path('api/', include('authenticate.api.urls')),

    # path('', include('calendario.urls_jardinagem')),
    # path('', include('calendario.urls_limpeza_predial')),

    # path('', include('unidade.urls')),
    path('api/unidades/', include('unidade.api.urls')),

    # path('', include('localidade.urls_jardinagem')),
    # path('', include('localidade.urls_limpeza_predial')),
    path('api/localidades/', include('localidade.api.urls_jardinagem')),
    path('api/localidades/', include('localidade.api.urls_limpeza_predial')),

    path('api/areas/', include('areas.api.urls_jardinagem')),
    path('api/areas/', include('areas.api.urls_limpeza_predial')),

    # path('', include('empresasecundario.urls_jardinagem')),
    # path('', include('empresasecundario.urls_limpeza_predial')),
    path('api/empresas_secundarias/', include('empresasecundario.api.urls_jardinagem')),
    path('api/empresas_secundarias/', include('empresasecundario.api.urls_limpeza_predial')),


    # path('', include('catalogo_de_servicos.urls_jardinagem')),
    # path('', include('catalogo_de_servicos.urls_limpeza_predial')),
    path('api/catalogo_de_servicos/', include('catalogo_de_servicos.api.urls_jardinagem')),
    path('api/catalogo_de_servicos/', include('catalogo_de_servicos.api.urls_limpeza_predial')),

    # path('', include('terrenos.urls')),
    #
    # path('', include('vegetacao.urls')),
    path('api/vegetacao/', include('vegetacao.api.urls')),


    # path('', include('gerente.urls_jardinagem')),
    # path('', include('gerente.urls_limpeza_predial')),
    path('api/gerentes/', include('gerente.api.urls_jardinagem')),
    path('api/gerentes/', include('gerente.api.urls_limpeza_predial')),


    # path('', include('servicos.urls_jardinagem')),
    # path('', include('servicos.urls_limpeza_predial')),
    path('api/servicos/agendados/jardinagem/', include('servicos.api.urls_jardinagem')),
    path('api/servicos/agendados/limpeza_predial/', include('servicos.api.urls_limpeza_predial')),

    # path('', include('servicos.urls_configuracoes_limpeza_predial')),
    # path('', include('servicos.urls_configuracoes_jardinagem')),
    path('api/servicos/configurados/jardinagem/', include('servicos.api.urls_configuracoes_jardinagem')),
    # path('api/servicos/configurados/limpeza_predial/', include('servicos.api.urls_configuracoes_limpeza_predial')),

    # path('', include('relatorios.urls_jardinagem')),
    # path('', include('relatorios.urls_limpeza_predial')),

    # path('', include('dashboards.urls_jardinagem')),
    # path('', include('dashboards.urls_limpeza_predial')),

    # path('', include('processos.urls')),

    # path('', include('settings.urls_jardinagem')),
    # path('', include('settings.urls_limpeza_predial')),

    # path('', include('permissionscontrol.urls_jardinagem')),
    # path('', include('permissionscontrol.urls_limpeza_predial')),
    # path('', include('permissionscontrol.urls_especials')),
    path('api/permissions/', include('permissionscontrol.api.urls_jardinagem')),
    path('api/permissions/', include('permissionscontrol.api.urls_limpeza_predial')),
    path('api/permissions/', include('permissionscontrol.api.urls_especials')),


    # path('', include('history.urls_limpeza_predial')),
    # path('', include('history.urls_jardinagem')),


    # path('', include('schedules.urls')),

    # path('', include('kanban.urls_jardinagem')),
    # path('', include('kanban.urls_limpeza_predial')),

    # path('', include('chats.urls')),

    # path('', include('checklists.urls_jardinagem')),
    # path('', include('checklists.urls_limpeza_predial')),
    path('api/checklist/', include('checklists.api.urls_jardinagem')),
    path('api/checklist/', include('checklists.api.urls_limpeza_predial')),

    # path('', include('medidor.urls')),

    # path('', include('gantt.urls_jardinagem')),
    # path('', include('gantt.urls_limpeza_predial')),

    # path('', include('notifications.urls_jardinagem')),
    # path('', include('notifications.urls_limpeza_predial')),

    # path('', include('mapas.urls_jardinagem')),
    # path('', include('mapas.urls_limpeza_predial')),

    # path('', include('retornos.urls_jardinagem')),
    # path('', include('retornos.urls_limpeza_predial')),

    path('api/semana/', include('semana.api.urls')),
]+static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)