from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from localidade.api.serializers_limpeza_predial import LocalidadeLimpezaPredialSerializer
from localidade.models_limpeza_predial import LocalidadeLimpezaPredial
from permissionscontrol.utils import validate_permissions
from utils.views import GenericDetailView, GenericUpdateView, GenericFilteredListView

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def LocalidadeLimpezaPredialDetail(request, id_random):
    return GenericDetailView(
        request=request,
        model=LocalidadeLimpezaPredial,
        serializer_class=LocalidadeLimpezaPredialSerializer,
        filters={"id_random": id_random},
        permission_type="limpeza_predial",
        permission_to_access=["292: Pode visualizar localidades"],
        forbidden_message="Você não tem permissão para visualizar localidades de limpeza predial."
    )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def LocalidadeLimpezaPredialUpdate(request, id_random):
    return GenericUpdateView(
        request=request,
        model=LocalidadeLimpezaPredial,
        serializer_class=LocalidadeLimpezaPredialSerializer,
        filters={"id_random": id_random},
        permission_type="limpeza_predial",
        permission_to_access=["291: Pode editar localidades"],
        forbidden_message="Você não tem permissão para editar localidades de limpeza predial.",
        not_found_message="Localidade de limpeza predial não encontrada."
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def LocalidadeLimpezaPredialAlterStatus(request, id_random):
    userid = request.user.id_random

    try:
        localidade = LocalidadeLimpezaPredial.objects.get(id_random=id_random)
    except LocalidadeLimpezaPredial.DoesNotExist:
        return Response(
            {"detail": "Localidade de limpeza predial não encontrada."},
            status=status.HTTP_404_NOT_FOUND
        )

    allowed_fields = {'status'}
    received_fields = set(request.data.keys())

    if not received_fields:
        return Response(
            {"detail": "O campo 'status' é obrigatório."},
            status=status.HTTP_400_BAD_REQUEST
        )

    extra_fields = received_fields - allowed_fields
    if extra_fields:
        return Response(
            {
                "detail": "Apenas o campo 'status' pode ser alterado nesta rota.",
                "campos_recebidos": list(received_fields)
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    new_status = request.data.get('status')

    if new_status not in ['Mobilizado', 'Desmobilizado']:
        return Response(
            {"detail": "Valor de status inválido. Use 'Mobilizado' ou 'Desmobilizado'."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if new_status == 'Desmobilizado':
        permission_desmobilize = validate_permissions(
            request=request,
            userid=userid,
            permission_type='jardinagem',
            permission_to_access=['295: Pode reabilitar localidades']
        )
        if not permission_desmobilize:
            return Response(
                {"detail": "Você não tem permissão para desmobilizar esta localidade."},
                status=status.HTTP_403_FORBIDDEN
            )

    elif new_status == 'Mobilizado':
        permission_rehabilitate = validate_permissions(
            request=request,
            userid=userid,
            permission_type='jardinagem',
            permission_to_access=['285: Pode reabilitar colaboradores']
        )
        if not permission_rehabilitate:
            return Response(
                {"detail": "Você não tem permissão para reabilitar esta localidade."},
                status=status.HTTP_403_FORBIDDEN
            )

    localidade.status = new_status
    localidade.save()

    return Response(
        {
            "success": True,
            "message": f"Status da localidade atualizado para '{new_status}'.",
            "data": {
                "id_random": localidade.id_random,
                "status": localidade.status
            }
        },
        status=status.HTTP_200_OK
    )



# Response: https://gist.github.com/mitchtabian/ae03573737067c9269701ea662460205
# Url: https://<your-domain>/api/blog/list
# Headers: Authorization: Token <token>
class ListLocalidadeLimpezaPredial(GenericFilteredListView):
    model_class = LocalidadeLimpezaPredial
    serializer_class = LocalidadeLimpezaPredialSerializer
    permission_type = 'limpeza_predial'
    permission_code = '292: Pode visualizar localidades'
    search_fields = ('id_random', 'nome', 'lat_med', 'long_med', 'unidade', 'status')
    empresa_filter_paths = (
        'unidade__empresasecundaria__empresaprimaria__id_random',
        'unidade__empresasecundaria__id_random',
    )
