from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from permissionscontrol.api.serializers_limpeza_predial import PermissionsLimpezaPredialSerializer, PermissionsAccessLimpezaPredialSerializer
from permissionscontrol.models import PermissionsLimpezaPredial, PermissionsAccessLimpezaPredial
from utils.views import GenericDetailView, GenericUpdateView, GenericFilteredListView

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def PermissionsAccessLimpezaPredialDetail(request, id_random):
    return GenericDetailView(
        request=request,
        model=PermissionsAccessLimpezaPredial,
        serializer_class=PermissionsAccessLimpezaPredialSerializer,
        filters={"id_random": id_random},
        permission_type="limpeza_predial",
        permission_to_access=["301: Pode visualizar permissões de limpeza predial"],
        forbidden_message="Você não tem permissão para visualizar permissões de limpeza predial."
    )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def PermissionsAccessLimpezaPredialUpdate(request, id_random):
    return GenericUpdateView(
        request=request,
        model=PermissionsAccessLimpezaPredial,
        serializer_class=PermissionsAccessLimpezaPredialSerializer,
        filters={"id_random": id_random},
        permission_type="limpeza_predial",
        permission_to_access=["300: Pode editar permissões de limpeza predial"],
        forbidden_message="Você não tem permissão para editar permissões de limpeza predial.",
        not_found_message="Permissão de limpeza predial não encontrada."
    )




# Response: https://gist.github.com/mitchtabian/ae03573737067c9269701ea662460205
# Url: https://<your-domain>/api/blog/list
# Headers: Authorization: Token <token>
class ListPermissionsLimpezaPredial(ListAPIView):
    serializer_class = PermissionsLimpezaPredialSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('id_random', 'Permissions',)

    def get_queryset(self):
        return PermissionsLimpezaPredial.objects.all()


class ListPermissionsAccessLimpezaPredial(GenericFilteredListView):
    model_class = PermissionsAccessLimpezaPredial
    serializer_class = PermissionsAccessLimpezaPredialSerializer
    permission_type = 'limpeza_predial'
    permission_code = '301: Pode visualizar permissões de limpeza predial'
    search_fields = ('id_random', 'Gerente', 'Permissions',)
    empresa_filter_paths = (
        'Gerente__empresasecundaria__empresaprimaria__id_random',
        'Gerente__empresasecundaria__id_random',
    )
    extra_filters = {
        'Gerente__empresasecundaria__setor__setor': 'Limpeza predial',
        'Gerente__status': 'Mobilizado',
    }