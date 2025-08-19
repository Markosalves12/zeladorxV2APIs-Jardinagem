from django.urls import path
from checklists.api.views_limpeza_predial import (ListCheckListLimpezaPredial, CheckListLimpezaPredialDetails,
                                                  CreateCheckListLimpezaPredial, CheckListLimpezaPredialUpdate,
                                                  ListCheckListLimpezaPredialByServico, IfDeleteCheckListLimpezaPredail,
                                                  DeleteCheckListLimpezaPredail)


urlpatterns = [
    path('ListCheckListLimpezaPredial/', ListCheckListLimpezaPredial.as_view(), name="ListCheckListLimpezaPredial"),
    path('CheckListLimpezaPredialDetails/<str:id_random>/', CheckListLimpezaPredialDetails,name="CheckListLimpezaPredialDetails"),
    path('CreateCheckListLimpezaPredial/<str:id_random>/', CreateCheckListLimpezaPredial, name="CreateCheckListLimpezaPredial"),
    path('CheckListLimpezaPredialUpdate/<str:id_random>/', CheckListLimpezaPredialUpdate, name="CheckListLimpezaPredialUpdate"),
    path('ListCheckListLimpezaPredialByServico/<str:id_random>/', ListCheckListLimpezaPredialByServico, name="ListCheckListLimpezaPredialByServico"),
    path('IfDeleteCheckListLimpezaPredail/<str:id_random>/', IfDeleteCheckListLimpezaPredail, name="IfDeleteCheckListLimpezaPredail"),
    path('DeleteCheckListLimpezaPredail/<str:id_random>/', DeleteCheckListLimpezaPredail,
         name="DeleteCheckListLimpezaPredail"),
]