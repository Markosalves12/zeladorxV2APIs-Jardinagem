from django.urls import path
from empresasecundario.api.views_jardinagem import (ListEmpresaSecundariaJardins, EmpresaSecundariaJardinsDetail,
                                                    EmpresaSecundariaJardinsUpdate, EmpresaSecundariaJardinsAlterStatus)


urlpatterns = [
    path('ListEmpresaSecundariaJardins/', ListEmpresaSecundariaJardins.as_view(), name="ListEmpresaSecundariaJardins"),
    path('EmpresaSecundariaJardinsDetail/<str:id_random>/', EmpresaSecundariaJardinsDetail, name="EmpresaSecundariaJardinsDetail"),
    path('EmpresaSecundariaJardinsUpdate/<str:id_random>/', EmpresaSecundariaJardinsUpdate, name="EmpresaSecundariaJardinsUpdate"),
    path('EmpresaSecundariaJardinsAlterStatus/<str:id_random>/', EmpresaSecundariaJardinsAlterStatus, name="EmpresaSecundariaJardinsAlterStatus"),
    # path('AreasAssociadasLocalidadeJardins/<str:id_random>/', AreasAssociadasLocalidadeJardins, name="AreasAssociadasLocalidadeJardins"),
]