from django.urls import path
from authenticate.api.views import CustomAuthToken


urlpatterns = [
    path('login', CustomAuthToken.as_view(), name="login"),  # -> see accounts/api/views.py for response and url info
]