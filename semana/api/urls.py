from django.urls import path
from semana.api.views import ListDiasDaSemana


urlpatterns = [
    path('ListDiasDaSemana/', ListDiasDaSemana.as_view(), name="ListDiasDaSemana"),
 ]