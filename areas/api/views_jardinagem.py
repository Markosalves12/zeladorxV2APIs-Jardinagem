from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from areas.api.serializers_jardinagem import AreasJardinsSerializer
from areas.models_jardinagem import AreasJardins
from localidade.models_Jardinagem import LocalidadeJardiangem
from utils.views import (GenericDetailView, GenericUpdateView, GenericAlterStatusView, GenericFilteredListView,
                         GenericCreateView, GenericListByParentIdRandom)
from catalogo_de_servicos.models_jardinagem import CatalogodeServicoJardinagem
from vegetacao.models import CatalogoVegetacao
from terrenos.models import Terreno
from empresasecundario.utils import define_empresas


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateAreaJardins(request):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    foreign_key_validations = [
        {
            "coluna": "localidade",
            "model": LocalidadeJardiangem,
            "filters": {
                "unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
                "unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
                "unidade__empresasecundaria__status__in": ["Mobilizado",],
                "status__in": ['Mobilizado'],
                "unidade__status__in": ["Mobilizado",],
            },
            "error_message": "A localidade selecionada não está mobilizada ou não pertence às empresas que você gerencia."
        },
        {
            "coluna": "servico",
            "model": CatalogodeServicoJardinagem,
            "filters": {
                "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
                "EmpresaSecundaria__id_random__in": empresas_secundarias_ids,
                "EmpresaSecundaria__status__in": ["Mobilizado",],
                "status__in": ["Mobilizado", ],
            },
            "error_message": "O serviço selecionado está desmobilizado ou fora do seu escopo de empresas."
        },
        {
            "coluna": "vegetacao",
            "model": CatalogoVegetacao,
            "filters": {
                "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
                "EmpresaSecundaria__id_random__in": empresas_secundarias_ids,
                "EmpresaSecundaria__status__in": ['Mobilizado'],
                "status__in": ['Mobilizado'],
            },
            "error_message": "A vegetação selecionada não está disponível ou não é permitida neste contexto."
        },
        {
            "coluna": "Terreno",
            "model": Terreno,
            "filters": {
                "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
                "EmpresaSecundaria__id_random__in": empresas_secundarias_ids,
                "EmpresaSecundaria__status__in": ['Mobilizado'],
                "status__in": ['Mobilizado'],
            },
            "error_message": "O terreno selecionado está fora do seu escopo ou desmobilizado."
        }
    ]

    return GenericCreateView(
        request=request,
        model_class=AreasJardins,
        serializer_class=AreasJardinsSerializer,
        permission_type="jardinagem",
        permission_to_access=['250: Pode criar novas áreas de jardinagem'],
        forbidden_message="Você não tem permissão para criar áreas de jardinagem.",
        foreign_key_validations=foreign_key_validations
    )




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def AreasJardinsDetail(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericDetailView(
        request=request,
        model=AreasJardins,
        serializer_class=AreasJardinsSerializer,
        filters={"id_random": id_random},  # busca o objeto
        access_filters={  # valida o escopo do objeto
            "localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        permission_type="jardinagem",
        permission_to_access=["252: Pode visualizar áreas de jardinagem"],
        forbidden_message="Você não tem permissão para visualizar esta área de jardinagem."
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def AreasJardinsUpdate(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericUpdateView(
        request=request,
        model=AreasJardins,
        serializer_class=AreasJardinsSerializer,
        filters={"id_random": id_random},
        permission_type="jardinagem",
        permission_to_access=["251: Pode editar áreas de jardinagem"],
        forbidden_message="Você não tem permissão para editar esta área de jardinagem.",
        not_found_message="Área de jardinagem não encontrada.",
        access_filters={  # valida o escopo do objeto
            "localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
    )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def AreasJardinsAlterStatus(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericAlterStatusView(
        request=request,
        model=AreasJardins,
        filters={"id_random": id_random},
        permission_type="jardinagem",
        desmobilize_permission="254: Pode desmobilizar áreas de jardinagem",
        rehabilitate_permission="255: Pode reabilitar áreas de jardinagem",
        not_found_message="Área de jardinagem não encontrada.",
        success_message="Status da área de jardinagem atualizado com sucesso.",
        access_filters={
            "localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
    )


# Response: https://gist.github.com/mitchtabian/ae03573737067c9269701ea662460205
# Headers: Authorization: Token <token>
class ListAreasJardins(GenericFilteredListView):
    model_class = AreasJardins
    serializer_class = AreasJardinsSerializer
    permission_type = 'jardinagem'
    permission_code = '252: Pode visualizar áreas de jardinagem'
    search_fields = ('id_random', 'nome', 'dimensao', 'Terreno', 'vegetacao', 'servico', 'localidade', 'periodicidade', 'status')
    empresa_filter_paths = (
        "localidade__unidade__empresasecundaria__empresaprimaria__id_random",
        "localidade__unidade__empresasecundaria__id_random"
    )



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def AreasAssociadasLocalidadeJardins(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]


    return GenericListByParentIdRandom(
        request=request,
        parent_model=LocalidadeJardiangem,
        child_model=AreasJardins,
        serializer_class=AreasJardinsSerializer,
        parent_lookup_field='localidade__id_random',
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['252: Pode visualizar áreas de jardinagem'],
        not_found_message='Localidade de jardinagem não encontrada.',
        forbidden_message='Você não tem permissão para visualizar esta área de jardinagem.',
        access_filters={
            "localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
    )