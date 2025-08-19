from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from permissionscontrol.api.serializers_especials import PermissionsEspecialsSerializer, PermissionsAccessEspecialsSerializer
from permissionscontrol.models import PermissionsEspecials, PermissionsAccessEspecials
from empresasecundario.utils import define_empresas
from permissionscontrol.utils import validate_permissions
from rest_framework.exceptions import PermissionDenied



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def PermissionsAccessEspecialsDetail(request, id_random):
    user_id_random = request.user.id_random

    permission_view = validate_permissions(
        request=request,
        userid=user_id_random,
        permission_type='especials',
        permission_to_access=['301: Pode visualizar permissões especiais']
    )

    if not permission_view:
        return Response(
            {"detail": "Você não tem permissão para visualizar permissões especiais."},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        permission_especials = PermissionsAccessEspecials.objects.get(id_random=id_random)
    except PermissionsAccessEspecials.DoesNotExist:
        return Response(
            {"detail": "Permissão especial não encontrada."},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = PermissionsAccessEspecialsSerializer(permission_especials, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def PermissionsAccessEspecialsUpdate(request, id_random):
    user_id_random = request.user.id_random

    has_permission = validate_permissions(
        request=request,
        userid=user_id_random,
        permission_type='especials',
        permission_to_access=['300: Pode editar permissões especiais']
    )

    if not has_permission:
        return Response(
            {"detail": "Você não tem permissão para editar permissões especiais."},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        area = PermissionsAccessEspecials.objects.get(id_random=id_random)
    except PermissionsAccessEspecials.DoesNotExist:
        return Response(
            {"detail": "Permissão especial não encontrada."},
            status=status.HTTP_404_NOT_FOUND
        )

    # Impede edição do campo 'status' (caso esteja na requisição)
    if 'status' in request.data:
        return Response(
            {"detail": "O campo 'status' não pode ser alterado por esta rota."},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = PermissionsAccessEspecialsSerializer(area, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "success": True,
                "message": "Permissões especiais atualizada com sucesso.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    return Response(
        {
            "success": False,
            "message": "Erro de validação.",
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )


class ListPermissionsEspecials(ListAPIView):
    serializer_class = PermissionsEspecialsSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('id_random', 'Permissions',)

    def get_queryset(self):
        return PermissionsEspecials.objects.all()

    # Desativa paginação forçada pelo settings.py
    def paginate_queryset(self, queryset):
        return None


class ListPermissionsAccessEspecials(ListAPIView):
    serializer_class = PermissionsAccessEspecialsSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('id_random', 'Gerente', 'Permissions',)

    def get_queryset(self):
        user_id_random = self.request.user.id_random

        if not validate_permissions(
            request=self.request,
            userid=user_id_random,
            permission_type='especials',
            permission_to_access=['301: Pode visualizar permissões especiais']
        ):
            raise PermissionDenied("Você não tem permissão para visualizar permissões especiais.")

        empresas = define_empresas(request=self.request, userid=user_id_random)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        empresas_secundarias_ids = empresas['empresas_secundarias_ids']

        return PermissionsAccessEspecials.objects.filter(
            Gerente__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            Gerente__empresasecundaria__id_random__in=empresas_secundarias_ids,
            Gerente__status='Mobilizado'
        ).distinct()