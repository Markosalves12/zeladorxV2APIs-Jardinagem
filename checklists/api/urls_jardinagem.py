from django.urls import path
from checklists.api.views_jardinagem import (CheckListJardinagemDetails, ListCheckListJardinagem,
                                             CreateCheckListJardinagem, CheckListJardinagemUpdate,
                                             ListCheckListJardinagemByServico, IfDeleteCheckListJardins,
                                             DeleteCheckListJardins)


urlpatterns = [
    path('ListCheckListJardinagem/', ListCheckListJardinagem.as_view(), name="ListCheckListJardinagem"),
    path('CheckListJardinagemDetails/<str:id_random>/', CheckListJardinagemDetails, name="CheckListJardinagemDetails"),
    path('CreateCheckListJardinagem/<str:id_random>/', CreateCheckListJardinagem, name="CreateCheckListJardinagem"),
    path('CheckListJardinagemUpdate/<str:id_random>/', CheckListJardinagemUpdate, name="CheckListJardinagemUpdate"),
    path('ListCheckListJardinagemByServico/<str:id_random>/', ListCheckListJardinagemByServico, name="ListCheckListJardinagemByServico"),
    path('IfDeleteCheckListJardins/<str:id_random>/', IfDeleteCheckListJardins, name="IfDeleteCheckListJardins"),
    path('DeleteCheckListJardins/<str:id_random>/', DeleteCheckListJardins, name="DeleteCheckListJardins"),
]