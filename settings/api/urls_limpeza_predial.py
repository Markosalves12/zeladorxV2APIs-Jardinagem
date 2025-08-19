from django.urls import path
from settings.api.views_limpeza_predial import (SettingServicosGerenteLimpezaPredialDetail,
                                           ListSettingServicosGerenteLimpezaPredial,
                                           SettingServicosGerenteLimpezaPredialUpdate)


urlpatterns = [
    path('ListSettingServicosGerenteLimpezaPredial/', ListSettingServicosGerenteLimpezaPredial.as_view(), name="ListSettingServicosGerenteLimpezaPredial"),
    path('SettingServicosGerenteLimpezaPredialUpdate/<str:id_random>/', SettingServicosGerenteLimpezaPredialUpdate, name="SettingServicosGerenteLimpezaPredialUpdate"),
    path('SettingServicosGerenteLimpezaPredialDetail/<str:id_random>/', SettingServicosGerenteLimpezaPredialDetail, name="SettingServicosGerenteLimpezaPredialDetail"),
]