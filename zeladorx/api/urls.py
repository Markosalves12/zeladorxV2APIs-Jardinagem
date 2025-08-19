from django.urls import path
from zeladorx.api.views import MyMacroServices


urlpatterns = [
    path('MyMacroServices/', MyMacroServices, name="MyMacroServices"),
]