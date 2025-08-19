from django.urls import path
from empresaprimaria.api.views import empresaprimaria


urlpatterns = [
    path('EmpresaPrimaria/', empresaprimaria, name="EmpresaPrimaria"),
]