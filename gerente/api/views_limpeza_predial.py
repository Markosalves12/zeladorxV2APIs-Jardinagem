from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from gerente.api.serializers import GerenteSerializer
from gerente.models import Gerente
from permissionscontrol.utils import validate_permissions
from utils.views import GenericDetailView, GenericAlterStatusView, GenericFilteredListView


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GerenteLimpezaPredialDetail(request, id_random):
    return GenericDetailView(
        request=request,
        model=Gerente,
        serializer_class=GerenteSerializer,
        filters={"id_random": id_random},
        permission_type="limpeza_predial",
        permission_to_access=["282: Pode visualizar colaboradores"],
        forbidden_message="Você não tem permissão para visualizar colaboradores de limpeza predial."
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def GerenteLimpezaPredialUpdate(request, id_random):
    user_id_random = request.user.id_random

    has_permission = validate_permissions(
        request=request,
        userid=user_id_random,
        permission_type='limpeza_predial',
        permission_to_access=['281: Pode editar colaboradores']
    )

    if not has_permission:
        return Response(
            {"detail": "Você não tem permissão para editar colaboradores de limpeza predial."},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        colaborador = Gerente.objects.get(id_random=id_random)
    except Gerente.DoesNotExist:
        return Response(
            {"detail": "Colaborador de limpeza predial não encontrada."},
            status=status.HTTP_404_NOT_FOUND
        )

    # Impede edição do campo 'status' (caso esteja na requisição)
    if 'status' in request.data:
        return Response(
            {"detail": "O campo 'status' não pode ser alterado por esta rota."},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = GerenteSerializer(colaborador, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "success": True,
                "message": "Colaborador de limpeza predial atualizada com sucesso.",
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



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def GerenteLimpezaPredialAlterStatus(request, id_random):
    return GenericAlterStatusView(
        request=request,
        model=Gerente,
        filters={'id_random': id_random},
        permission_type='limpeza_predial',
        desmobilize_permission='284: Pode desmobilizar colaboradores',
        rehabilitate_permission='285: Pode reabilitar colaboradores',
        not_found_message='Colaborador de limpeza predial não encontrado.',
        success_message='Status do colaborador atualizado com sucesso.'
    )


# Response: https://gist.github.com/mitchtabian/ae03573737067c9269701ea662460205
# Url: https://<your-domain>/api/blog/list
# Headers: Authorization: Token <token>
class ListGerenteLimpezaPredial(GenericFilteredListView):
    model_class = Gerente
    serializer_class = GerenteSerializer
    permission_type = 'limpeza_predial'
    permission_code = '282: Pode visualizar colaboradores'
    search_fields = ('username', 'email', 'empresasecundaria', 'is_superuser', 'status')
    empresa_filter_paths = (
        'empresasecundaria__empresaprimaria__id_random',
        'empresasecundaria__id_random',
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(empresasecundaria__setor__setor='Limpeza predial')
