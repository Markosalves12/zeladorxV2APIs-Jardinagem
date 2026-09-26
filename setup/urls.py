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

    # Portal de documentação (telas para o usuário)
    path('', include('apidocs.urls')),

    path('api/', include('authenticate.api.urls')),

    path('api/unidades/', include('unidade.api.urls')),

    path('api/localidades/', include('localidade.api.urls_jardinagem')),
    path('api/localidades/', include('localidade.api.urls_limpeza_predial')),

    path('api/areas/', include('areas.api.urls_jardinagem')),
    path('api/areas/', include('areas.api.urls_limpeza_predial')),

    path('api/empresas_secundarias/', include('empresasecundario.api.urls_jardinagem')),
    path('api/empresas_secundarias/', include('empresasecundario.api.urls_limpeza_predial')),


    path('api/catalogo_de_servicos/', include('catalogo_de_servicos.api.urls_jardinagem')),
    path('api/catalogo_de_servicos/', include('catalogo_de_servicos.api.urls_limpeza_predial')),

    path('api/settings/', include('settings.api.urls_jardinagem')),
    path('api/settings/', include('settings.api.urls_limpeza_predial')),

    path('api/terrenos/', include('terrenos.api.urls')),

    path('api/vegetacao/', include('vegetacao.api.urls')),

    path('api/gerentes/', include('gerente.api.urls_jardinagem')),
    path('api/gerentes/', include('gerente.api.urls_limpeza_predial')),

    path('api/servicos/agendados/', include('servicos.api.urls_jardinagem')),
    path('api/servicos/agendados/', include('servicos.api.urls_limpeza_predial')),

    path('api/servicos/fato/', include('servicos.api.urls_fato_servico_jardinagem')),
    path('api/servicos/fato/', include('servicos.api.urls_fato_servico_limpeza_predial')),

    path('api/servicos/configurados/', include('servicos.api.urls_configuracoes_jardinagem')),
    path('api/servicos/configurados/', include('servicos.api.urls_configuracoes_limpeza_predial')),


    path('api/permissions/', include('permissionscontrol.api.urls_jardinagem')),
    path('api/permissions/', include('permissionscontrol.api.urls_limpeza_predial')),
    path('api/permissions/', include('permissionscontrol.api.urls_especials')),

    path('api/checklist/', include('checklists.api.urls_jardinagem')),
    path('api/checklist/', include('checklists.api.urls_limpeza_predial')),

    path('api/semana/', include('semana.api.urls')),

    path('api/zeladorx/', include('zeladorx.api.urls')),

    path('api/zeladorx/', include('empresaprimaria.api.urls')),
]+static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)