from django.urls import path
from empresasecundario.api.views_limpeza_predial import (ListEmpresaSecundariaLimpezaPredial,
                                                         EmpresaSecundariaLimpezaPredialDetail,
                                                         EmpresaSecundariaLimpezaPredialUpdate,
                                                         EmpresaSecundariaLimpezaPredialAlterStatus,
                                                         CreateEmpresaSecundariaLimpezaPredial,
                                                         IfDeleteEmpresaSecundariaLimpezaPredial,
                                                         ListEmpresaSecundariaLimpezaPredialFromForms,
                                                         DeleteEmpresaSecundariaLimpezaPredial)


urlpatterns = [
    path('ListEmpresaSecundariaLimpezaPredial/', ListEmpresaSecundariaLimpezaPredial.as_view(), name="ListEmpresaSecundariaLimpezaPredial"),
    path('EmpresaSecundariaLimpezaPredialDetail/<str:id_random>/', EmpresaSecundariaLimpezaPredialDetail, name="EmpresaSecundariaLimpezaPredialDetail"),
    path('EmpresaSecundariaLimpezaPredialUpdate/<str:id_random>/', EmpresaSecundariaLimpezaPredialUpdate, name="EmpresaSecundariaLimpezaPredialUpdate"),
    path('EmpresaSecundariaLimpezaPredialAlterStatus/<str:id_random>/', EmpresaSecundariaLimpezaPredialAlterStatus, name="EmpresaSecundariaLimpezaPredialAlterStatus"),
    path('CreateEmpresaSecundariaLimpezaPredial/', CreateEmpresaSecundariaLimpezaPredial, name="CreateEmpresaSecundariaLimpezaPredial"),
    path('IfDeleteEmpresaSecundariaLimpezaPredial/<str:id_random>/', IfDeleteEmpresaSecundariaLimpezaPredial, name="IfDeleteEmpresaSecundariaLimpezaPredial"),
    path('ListEmpresaSecundariaLimpezaPredialFromForms/', ListEmpresaSecundariaLimpezaPredialFromForms.as_view(), name="ListEmpresaSecundariaLimpezaPredialFromForms"),
    path('DeleteEmpresaSecundariaLimpezaPredial/<str:id_random>/', DeleteEmpresaSecundariaLimpezaPredial, name="DeleteEmpresaSecundariaLimpezaPredial"),
]