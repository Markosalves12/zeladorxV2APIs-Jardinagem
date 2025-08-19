from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from permissionscontrol.api.serializers_jardinagem import PermissionsJardinagemSerializer, PermissionsAccessJardinagemSerializer
from permissionscontrol.models import PermissionsJardinagem, PermissionsAccessJardinagem
from empresasecundario.utils import define_empresas
from utils.views import GenericDetailView, GenericUpdateView, GenericFilteredListView


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def PermissionsAccessJardinagemDetail(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericDetailView(
        request=request,
        model=PermissionsAccessJardinagem,
        serializer_class=PermissionsAccessJardinagemSerializer,
        filters={"id_random": id_random},
        permission_type="jardinagem",
        permission_to_access=["301: Pode visualizar permissões de jardinagem"],
        forbidden_message="Você não tem permissão para visualizar permissões de jardinagem.",
        access_filters={
            "Gerente__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Gerente__empresasecundaria__id_random__in": empresas_secundarias_ids,
            "Gerente__empresasecundaria__setor__setor": 'Jardinagem',
            "Gerente__status": 'Mobilizado'
        }
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def PermissionsAccessJardinagemUpdate(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericUpdateView(
        request=request,
        model=PermissionsAccessJardinagem,
        serializer_class=PermissionsAccessJardinagemSerializer,
        filters={"id_random": id_random},
        permission_type="jardinagem",
        permission_to_access=["300: Pode editar permissões de jardinagem"],
        forbidden_message="Você não tem permissão para editar permissões de jardinagem.",
        not_found_message="Permissão de jardinagem não encontrada.",
        access_filters={
            "Gerente__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Gerente__empresasecundaria__id_random__in": empresas_secundarias_ids,
            "Gerente__empresasecundaria__setor__setor": 'Jardinagem',
            "Gerente__status": 'Mobilizado'
        },
        public_endpoint=False,
    )




class ListPermissionsJardinagem(ListAPIView):
    serializer_class = PermissionsJardinagemSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('id', 'id_random', 'Permissions',)

    def get_queryset(self):
        return PermissionsJardinagem.objects.order_by('Permissions')

    # Desativa paginação forçada pelo settings.py
    def paginate_queryset(self, queryset):
        return None



class ListPermissionsAccessJardinagem(GenericFilteredListView):
    model_class = PermissionsAccessJardinagem
    serializer_class = PermissionsAccessJardinagemSerializer
    permission_type = 'jardinagem'
    permission_code = '301: Pode visualizar permissões de jardinagem'
    search_fields = ('id', 'id_random', 'Gerente', 'Permissions',)
    empresa_filter_paths = (
        'Gerente__empresasecundaria__empresaprimaria__id_random',
        'Gerente__empresasecundaria__id_random',
    )
    extra_filters = {
        'Gerente__empresasecundaria__setor__setor__in': ['Jardinagem'],
        'Gerente__status': 'Mobilizado',
    }
    forbidden_message="Você não tem permissão para visualziar permissões de usuários"
