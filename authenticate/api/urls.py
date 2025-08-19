from django.urls import path
from authenticate.api.views import CustomAuthToken, LogoutView, ResetPasswordAPIView, ConfirmarTrocaSenhaAPIView


urlpatterns = [
    path('login', CustomAuthToken.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('confirm-reset-password/<str:url_token>/', ConfirmarTrocaSenhaAPIView, name='confirm-reset-password'),
]