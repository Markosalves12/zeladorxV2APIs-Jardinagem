from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from gerente.api.serializers import GerenteSerializer
from gerente.models import Gerente
from empresasecundario.utils import define_empresas
from permissionscontrol.utils import validate_permissions
from rest_framework.exceptions import PermissionDenied

from utils.views import GenericDetailView, GenericUpdateView, GenericAlterStatusView, GenericFilteredListView

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GerenteJardinsDetail(request, id_random):
    return GenericDetailView(
        request=request,
        model=Gerente,
        serializer_class=GerenteSerializer,
        filters={"id_random": id_random},
        permission_type="jardinagem",
        permission_to_access=["282: Pode visualizar colaboradores"],
        forbidden_message="Você não tem permissão para visualizar colaboradores de jardinagem."
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def GerenteJardinsUpdate(request, id_random):
    return GenericUpdateView(
        request=request,
        model=Gerente,
        serializer_class=GerenteSerializer,
        filters={"id_random": id_random},
        permission_type="jardinagem",
        permission_to_access=["281: Pode editar colaboradores"],
        forbidden_message="Você não tem permissão para editar colaboradores de jardinagem.",
        not_found_message="Colaborador de jardinagem não encontrado."
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def GerenteJardinsAlterStatus(request, id_random):
    return GenericAlterStatusView(
        request=request,
        model=Gerente,
        filters={'id_random': id_random},
        permission_type='jardinagem',
        desmobilize_permission='284: Pode desmobilizar colaboradores',
        rehabilitate_permission='285: Pode reabilitar colaboradores',
        not_found_message='Colaborador de jardinagem não encontrado.',
        success_message='Status do colaborador atualizado com sucesso.'
    )




# Response: https://gist.github.com/mitchtabian/ae03573737067c9269701ea662460205
# Url: https://<your-domain>/api/blog/list
# Headers: Authorization: Token <token>
class ListGerenteJardins(GenericFilteredListView):
    model_class = Gerente
    serializer_class = GerenteSerializer
    permission_type = 'jardinagem'
    permission_code = '282: Pode visualizar colaboradores'
    search_fields = ('username', 'email', 'empresasecundaria', 'is_superuser', 'status')
    empresa_filter_paths = (
        'empresasecundaria__empresaprimaria__id_random',
        'empresasecundaria__id_random',
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(empresasecundaria__setor__setor='Jardinagem')
