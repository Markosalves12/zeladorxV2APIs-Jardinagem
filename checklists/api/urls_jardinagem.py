from django.urls import path
from checklists.api.views_jardinagem import ListCheckListDetailsJardinagem, ListCheckListJardinagem


urlpatterns = [
    path('ListCheckListJardinagem/', ListCheckListJardinagem.as_view(), name="ListCheckListJardinagem"),
    path('ListCheckListDetailsJardinagem/<str:id_random>/', ListCheckListDetailsJardinagem, name="ListCheckListDetailsJardinagem"),
 ]