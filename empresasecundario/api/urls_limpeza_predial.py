from django.urls import path
from empresasecundario.api.views_limpeza_predial import (ListEmpresaSecundariaLimpezaPredial, EmpresaSecundariaLimpezaPredialDetail,
                                                    EmpresaSecundariaLimpezaPredialUpdate, EmpresaSecundariaLimpezaPredialAlterStatus)


urlpatterns = [
    path('ListEmpresaSecundariaLimpezaPredial/', ListEmpresaSecundariaLimpezaPredial.as_view(), name="ListEmpresaSecundariaLimpezaPredial"),
    path('EmpresaSecundariaLimpezaPredialDetail/<str:id_random>/', EmpresaSecundariaLimpezaPredialDetail, name="EmpresaSecundariaLimpezaPredialDetail"),
    path('EmpresaSecundariaLimpezaPredialUpdate/<str:id_random>/', EmpresaSecundariaLimpezaPredialUpdate, name="EmpresaSecundariaLimpezaPredialUpdate"),
    path('EmpresaSecundariaLimpezaPredialAlterStatus/<str:id_random>/', EmpresaSecundariaLimpezaPredialAlterStatus, name="EmpresaSecundariaLimpezaPredialAlterStatus"),
    # path('AreasAssociadasLocalidadeJardins/<str:id_random>/', AreasAssociadasLocalidadeJardins, name="AreasAssociadasLocalidadeJardins"),
]