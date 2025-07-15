from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from unidade.api.serializers import UnidadeSerializer
from unidade.models import Unidade
from django.db import router
from django.contrib.admin.utils import NestedObjects
from empresasecundario.utils import define_empresas
from permissionscontrol.utils import validate_permissions
from rest_framework.exceptions import PermissionDenied


from utils.views import GenericDetailView, GenericUpdateView

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UnidadeDetail(request, id_random):
    return GenericDetailView(
        request=request,
        model=Unidade,
        serializer_class=UnidadeSerializer,
        filters={"id_random": id_random},
        permission_type="especials",
        permission_to_access=["342: Pode visualizar unidades"],
        forbidden_message="Você não tem permissão para visualizar esta unidade."
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def UnidadeUpdate(request, id_random):
    return GenericUpdateView(
        request=request,
        model=Unidade,
        serializer_class=UnidadeSerializer,
        filters={"id_random": id_random},
        permission_type="especials",
        permission_to_access=["341: Pode editar unidades"],
        forbidden_message="Você não tem permissão para editar esta unidade.",
        not_found_message="Unidade não encontrada."
    )




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def UnidadeAlterStatus(request, id_random):
    userid = request.user.id_random

    try:
        unidade = Unidade.objects.get(id_random=id_random)
    except Unidade.DoesNotExist:
        return Response(
            {"detail": "Unidade não encontrada."},
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
            permission_type='especials',
            permission_to_access=['344: Pode desmobilizar unidades']
        )
        if not permission_desmobilize:
            return Response(
                {"detail": "Você não tem permissão para desmobilizar esta unidade."},
                status=status.HTTP_403_FORBIDDEN
            )

    elif new_status == 'Mobilizado':
        permission_rehabilitate = validate_permissions(
            request=request,
            userid=userid,
            permission_type='especials',
            permission_to_access=['345: Pode reabilitar unidades']
        )
        if not permission_rehabilitate:
            return Response(
                {"detail": "Você não tem permissão para reabilitar esta unidade."},
                status=status.HTTP_403_FORBIDDEN
            )

    unidade.status = new_status
    unidade.save()

    return Response(
        {
            "success": True,
            "message": f"Status da área atualizado para '{new_status}'.",
            "data": {
                "id_random": unidade.id_random,
                "status": unidade.status
            }
        },
        status=status.HTTP_200_OK
    )



# Response: https://gist.github.com/mitchtabian/ae03573737067c9269701ea662460205
# Url: https://<your-domain>/api/blog/list
# Headers: Authorization: Token <token>
class ListUnidade(ListAPIView):
    serializer_class = UnidadeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('id_random', 'nome', 'linkmapajardinagem', 'linkmapalimnpezapredial', 'empresasecundaria', 'status')

    def get_queryset(self):
        user_id_random = self.request.user.id_random

        # Verifica permissão
        if not validate_permissions(
            request=self.request,
            userid=user_id_random,
            permission_type='especials',
            permission_to_access=['342: Pode visualizar unidades']
        ):
            raise PermissionDenied("Você não tem permissão para visualizar unidades.")

        empresas = define_empresas(request=self.request, userid=user_id_random)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        empresas_secundarias_ids = empresas['empresas_secundarias_ids']
        unidades_secundarias_ids = empresas['unidades_secundarias_ids']

        return Unidade.objects.filter(
            empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            empresasecundaria__id_random__in=empresas_secundarias_ids,
            id_random__in=unidades_secundarias_ids
        ).distinct()


def flatten_nested(obj_list, depth=0):
    """
    Converte estrutura aninhada do Django Admin (nested()) em lista formatada.
    """
    flat = []
    for item in obj_list:
        if isinstance(item, list):
            flat.extend(flatten_nested(item, depth + 1))
        else:
            flat.append(f"{'  ' * depth}- {str(item)}")
    return flat


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def IfDeleteUnidade(request, id_random):
    user_id_random = request.user.id_random

    permission_view = validate_permissions(
        request=request,
        userid=user_id_random,
        permission_type='jardinagem',
        permission_to_access=['297: Pode visualizar unidades']
    )

    if not permission_view:
        return Response(
            {"detail": "Você não tem permissão para visualizar unidades de jardinagem."},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        unidade = Unidade.objects.get(id_random=id_random)
    except Unidade.DoesNotExist:
        return Response(
            {"detail": "Unidade não encontrada."},
            status=status.HTTP_404_NOT_FOUND
        )

    # Coleta recursiva dos objetos que seriam deletados
    collector = NestedObjects(using=router.db_for_write(Unidade))
    collector.collect([unidade])

    # Gera uma versão plana da hierarquia de objetos
    nested_tree = collector.nested()
    deletions_list = flatten_nested(nested_tree)

    return Response({
        "unidade": str(unidade),
        "resumo": {
            model.__name__: len(objs)
            for model, objs in collector.model_objs.items()
        },  # dicionário {Modelo: [objs]}
        "objetos_em_cascata": deletions_list
    }, status=status.HTTP_200_OK)