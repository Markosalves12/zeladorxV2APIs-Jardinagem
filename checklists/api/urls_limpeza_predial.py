from django.urls import path
from checklists.api.views_limpeza_predial import ListCheckListLimpezaPredial, ListCheckListDetailsLimpezaPredial


urlpatterns = [
    path('ListCheckListLimpezaPredial/', ListCheckListLimpezaPredial.as_view(), name="ListCheckListLimpezaPredial"),
    path('ListCheckListDetailsLimpezaPredial/<str:id_random>/', ListCheckListDetailsLimpezaPredial,
         name="ListCheckListDetailsLimpezaPredial"),
 ]