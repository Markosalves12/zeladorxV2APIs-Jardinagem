from django.urls import path
from settings.api.views_jardinagem import (SettingServicosGerenteJardinagemDetail,
                                           ListSettingServicosGerenteJardinagem,
                                           SettingServicosGerenteJardinagemUpdate)


urlpatterns = [
    path('ListSettingServicosGerenteJardinagem/', ListSettingServicosGerenteJardinagem.as_view(), name="ListSettingServicosGerenteJardinagem"),
    path('SettingServicosGerenteJardinagemUpdate/<str:id_random>/', SettingServicosGerenteJardinagemUpdate, name="SettingServicosGerenteJardinagemUpdate"),
    path('SettingServicosGerenteJardinagemDetail/<str:id_random>/', SettingServicosGerenteJardinagemDetail, name="SettingServicosGerenteJardinagemDetail"),
]