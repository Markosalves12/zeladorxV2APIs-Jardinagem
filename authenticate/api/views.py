from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from gerente.models import Gerente
from notifications.utils import enviar_notificacao
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from authenticate.models import PasswordResetToken


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user

        return Response({
            'token': token.key,
            'id_random': getattr(user, 'id_random', None),
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'is_superuser': user.is_superuser
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Deleta o token do usuário para invalidar autenticação futura
            request.user.auth_token.delete()
            return Response({"detail": "Logout realizado com sucesso."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Erro ao fazer logout."}, status=status.HTTP_400_BAD_REQUEST)


# POST /api/auth/reset-password/
# {
#   "email": "exemplo@email.com"
# }

class ResetPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response(
                {"detail": "O campo 'email' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            gerente = Gerente.objects.get(email=email)
        except Gerente.DoesNotExist:
            return Response(
                {"detail": "Usuário com esse e-mail não foi encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Criar token de redefinição
        reset_token = PasswordResetToken(user=gerente)
        reset_token.save()

        # Envio do e-mail
        enviar_notificacao(
            destinatario=[email],
            assunto="Alteração de senha",
            contexto={
                'username': gerente.username,
                'email': gerente.email,
                'randon_token': reset_token.reset_token
            },
            template='notifications/reset_password.html'
        )

        return Response(
            {
                "message": "Token enviado para o e-mail.",
                "url_token": reset_token.url_token
            },
            status=status.HTTP_200_OK
        )


# Função normal que substitui a APIView
@api_view(['POST'])
@permission_classes([AllowAny])
def ConfirmarTrocaSenhaAPIView(request, url_token):
    email = request.data.get('email')
    reset_token = request.data.get('reset_token')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')

    # Validações
    if not all([email, reset_token, new_password, confirm_password]):
        return Response(
            {"detail": "Todos os campos são obrigatórios."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        reset_token_obj = PasswordResetToken.objects.get(url_token=url_token)
    except PasswordResetToken.DoesNotExist:
        return Response({"detail": "URL inválida."}, status=status.HTTP_400_BAD_REQUEST)

    if reset_token_obj.user.email != email:
        return Response({"detail": "Email inválido."}, status=status.HTTP_400_BAD_REQUEST)

    if reset_token_obj.reset_token != reset_token:
        return Response({"detail": "Token inválido."}, status=status.HTTP_400_BAD_REQUEST)

    if reset_token_obj.is_expired():
        return Response({"detail": "Token expirado."}, status=status.HTTP_400_BAD_REQUEST)

    if new_password != confirm_password:
        return Response({"detail": "Senhas não conferem."}, status=status.HTTP_400_BAD_REQUEST)

    # Atualizar a senha
    try:
        user = Gerente.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        # Deletar o token após o uso
        reset_token_obj.delete()

        return Response({"detail": "Senha redefinida com sucesso."}, status=status.HTTP_200_OK)
    except Gerente.DoesNotExist:
        return Response({"detail": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)