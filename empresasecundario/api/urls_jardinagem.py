from django.urls import path
from empresasecundario.api.views_jardinagem import (ListEmpresaSecundariaJardinagem, EmpresaSecundariaJardinagemDetail,
                                                    EmpresaSecundariaJardinagemUpdate, EmpresaSecundariaJardinagemAlterStatus,
                                                    CreateEmpresaSecundariaJardinagem, IfDeleteEmpresaSecundariaJardinagem,
                                                    ListEmpresaSecundariaJardinagemFromForms, DeleteEmpresaSecundariaJardinagem)


urlpatterns = [
    path('ListEmpresaSecundariaJardinagem/', ListEmpresaSecundariaJardinagem.as_view(), name="ListEmpresaSecundariaJardinagem"),
    path('EmpresaSecundariaJardinagemDetail/<str:id_random>/', EmpresaSecundariaJardinagemDetail, name="EmpresaSecundariaJardinagemDetail"),
    path('EmpresaSecundariaJardinagemUpdate/<str:id_random>/', EmpresaSecundariaJardinagemUpdate, name="EmpresaSecundariaJardinagemUpdate"),
    path('EmpresaSecundariaJardinagemAlterStatus/<str:id_random>/', EmpresaSecundariaJardinagemAlterStatus, name="EmpresaSecundariaJardinagemAlterStatus"),
    path('CreateEmpresaSecundariaJardinagem/', CreateEmpresaSecundariaJardinagem, name="CreateEmpresaSecundariaJardinagem"),
    path('IfDeleteEmpresaSecundariaJardinagem/<str:id_random>/', IfDeleteEmpresaSecundariaJardinagem, name="IfDeleteEmpresaSecundariaJardinagem"),
    path('ListEmpresaSecundariaJardinagemFromForms/', ListEmpresaSecundariaJardinagemFromForms.as_view(),
         name="ListEmpresaSecundariaJardinagemFromForms"),
    path('DeleteEmpresaSecundariaJardinagem/<str:id_random>/', DeleteEmpresaSecundariaJardinagem, name="DeleteEmpresaSecundariaJardinagem"),
]