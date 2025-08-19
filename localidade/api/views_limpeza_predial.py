from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from localidade.api.serializers_limpeza_predial import LocalidadeLimpezaPredialSerializer
from localidade.models_limpeza_predial import LocalidadeLimpezaPredial
from utils.views import (GenericDetailView, GenericUpdateView, GenericFilteredListView, GenericCreateView,
                         GenericAlterStatusView, GenericIfDeleteView, GenericDeleteView)
from empresasecundario.utils import define_empresas
from unidade.models import Unidade


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateLocalidadeLimpezaPredial(request):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    foreign_key_validations = [
        {
            "coluna": "unidade",
            "model": Unidade,
            "filters": {
                "empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
                "empresasecundaria__id_random__in": empresas_secundarias_ids,
                "empresasecundaria__status__in": ["Mobilizado",],
                "status__in": ['Mobilizado'],
            },
            "error_message": "A unidade selecionada está desmobilizada ou não pertence às empresas que você gerencia."
        },
    ]

    return GenericCreateView(
        request=request,
        model_class=LocalidadeLimpezaPredial,
        serializer_class=LocalidadeLimpezaPredialSerializer,
        permission_type="limpeza_predial",
        permission_to_access=['290: Pode criar novas localidades'],
        forbidden_message="Você não tem permissão para criar localidades de limpeza predial.",
        foreign_key_validations=foreign_key_validations,
        public_endpoint=False
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def LocalidadeLimpezaPredialDetail(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericDetailView(
        request=request,
        model=LocalidadeLimpezaPredial,
        serializer_class=LocalidadeLimpezaPredialSerializer,
        filters={"id_random": id_random},
        permission_type="limpeza_predial",
        permission_to_access=["292: Pode visualizar localidades"],
        forbidden_message="Você não tem permissão para visualizar localidades de limpeza predial.",
        access_filters={
            "unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        }
    )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def LocalidadeLimpezaPredialUpdate(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericUpdateView(
        request=request,
        model=LocalidadeLimpezaPredial,
        serializer_class=LocalidadeLimpezaPredialSerializer,
        filters={"id_random": id_random},
        permission_type="limpeza_predial",
        permission_to_access=["291: Pode editar localidades"],
        forbidden_message="Você não tem permissão para editar localidades de limpeza predial.",
        not_found_message="Localidade de limpeza predial não encontrada.",
        access_filters={
            "unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        public_endpoint=False,
    )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def LocalidadeLimpezaPredialAlterStatus(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericAlterStatusView(
        request=request,
        model=LocalidadeLimpezaPredial,
        filters={"id_random": id_random},
        permission_type="limpeza_predial",
        desmobilize_permission='294: Pode desmobilizar localidades',
        rehabilitate_permission='295: Pode reabilitar localidades',
        not_found_message="Localidade de limpeza predial não encontrada.",
        success_message="Status da área de jardinagem atualizado com sucesso.",
        access_filters={
            "unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        public_endpoint=False
    )



# Headers: Authorization: Token <token>
class ListLocalidadeLimpezaPredial(GenericFilteredListView):
    model_class = LocalidadeLimpezaPredial
    serializer_class = LocalidadeLimpezaPredialSerializer
    permission_type = 'limpeza_predial'
    permission_code = '292: Pode visualizar localidades'
    search_fields = ('id', 'id_random', 'nome', 'lat_med', 'long_med', 'unidade', 'status',)
    empresa_filter_paths = (
        'unidade__empresasecundaria__empresaprimaria__id_random',
        'unidade__empresasecundaria__id_random',
    )
    forbidden_message = "Você não tem permissão para visualizar localidades de limpeza predial.",

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def IfDeleteLocalidadeLimpezaPredial(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericIfDeleteView(
        request,
        model=LocalidadeLimpezaPredial,
        id_random=id_random,
        permission_type='limpeza_predial',
        permission_to_access=['293: Pode excluir localidades'],
        access_filters={
            "unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        forbidden_message="Você não tem permissão para excluir esta localidade de limpeza predial."
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteLocalidadeLimpezaPredial(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericDeleteView(
        request,
        model=LocalidadeLimpezaPredial,
        id_random=id_random,
        permission_type='limpeza_predial',
        permission_to_access=['293: Pode excluir localidades'],
        access_filters={
            "unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        forbidden_message="Você não tem permissão para excluir esta localidade de limpeza predial."
    )

class ListLocalidadeLimpezaPredialFromForms(GenericFilteredListView):
    model_class = LocalidadeLimpezaPredial
    serializer_class = LocalidadeLimpezaPredialSerializer
    permission_type = 'limpeza_predial'
    permission_code = '292: Pode visualizar localidades'
    search_fields = ('id', 'id_random', 'nome', 'lat_med', 'long_med', 'unidade', 'status',)
    empresa_filter_paths = (
        'unidade__empresasecundaria__empresaprimaria__id_random',
        'unidade__empresasecundaria__id_random',
    )
    forbidden_message = "Você não tem permissão para visualizar localidades de limpeza predial."

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            unidade__empresasecundaria__status__in=['Mobilizado'],
            status__in=['Mobilizado'],
            unidade__status__in=['Mobilizado'],
        )