from django.urls import path

from . import views

app_name = 'apidocs'

urlpatterns = [
    path('', views.home, name='home'),
    path('docs/primeiros-passos/', views.getting_started, name='getting_started'),
    path('docs/<slug:plataforma>/', views.platform, name='platform'),
    path('docs/<slug:plataforma>/<slug:secao>/', views.section, name='section'),
]
