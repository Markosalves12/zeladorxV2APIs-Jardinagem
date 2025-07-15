from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from areas.api.serializer_limpeza_predial import AreaLimpezaPredialSerializer
from areas.models_limpeza_predial import AreaLimpezaPredial
from localidade.models_limpeza_predial import LocalidadeLimpezaPredial
from utils.views import (GenericDetailView, GenericUpdateView, GenericAlterStatusView, GenericFilteredListView,
                         GenericCreateView, GenericListByParentIdRandom)
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial
from empresasecundario.utils import define_empresas

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateAreaLimpezaPredial(request):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    foreign_key_validations = [
        {
            "coluna": "localidade",
            "model": LocalidadeLimpezaPredial,
            "filters": {
                "unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
                "unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
                "unidade__empresasecundaria__status__in": ['Mobilizado'],
                "status__in": ['Mobilizado'],
                "unidade__status__in": ['Mobilizado'],
            },
            "error_message": "A localidade selecionada não está mobilizada ou não pertence às empresas que você gerencia."
        },
        {
            "coluna": "servico",
            "model": CatalogodeServicoLimpezaPredial,
            "filters": {
                "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
                "EmpresaSecundaria__id_random__in": empresas_secundarias_ids,
                "EmpresaSecundaria__status__in": ["Mobilizado",],
                "status__in": ["Mobilizado", ],
            },
            "error_message": "O serviço selecionado está desmobilizado ou fora do seu escopo de empresas."
        },
    ]

    return GenericCreateView(
        request=request,
        model_class=AreaLimpezaPredial,
        serializer_class=AreaLimpezaPredialSerializer,
        permission_type="limpeza_predial",
        permission_to_access=['250: Pode criar novas áreas de limpeza predial'],
        forbidden_message="Você não tem permissão para criar áreas de limpeza predial.",
        foreign_key_validations=foreign_key_validations,
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def AreasLimpezaPredialDetail(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericDetailView(
        request=request,
        model=AreaLimpezaPredial,
        serializer_class=AreaLimpezaPredialSerializer,
        filters={"id_random": id_random},
        permission_type="limpeza_predial",
        access_filters={  # valida o escopo do objeto
            "localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        permission_to_access=['252: Pode visualizar áreas de limpeza predial'],
        forbidden_message='Você não tem permissão para visualizar esta área de limpeza predial.'
    )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def AreasLimpezaPredialUpdate(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericUpdateView(
        request=request,
        model=AreaLimpezaPredial,
        serializer_class=AreaLimpezaPredialSerializer,
        filters={"id_random": id_random},
        permission_type="limpeza_predial",
        permission_to_access=["251: Pode editar áreas de limpeza predial"],
        forbidden_message="Você não tem permissão para editar esta área de limpeza predial.",
        not_found_message="Área de limpeza predial não encontrada.",
        access_filters={  # valida o escopo do objeto
            "localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
    )




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def AreaLimpezaPredialAlterStatus(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericAlterStatusView(
        request=request,
        model=AreaLimpezaPredial,
        filters={'id_random': id_random},
        permission_type='limpeza_predial',
        desmobilize_permission='254: Pode desmobilizar áreas de limpeza predial',
        rehabilitate_permission='255: Pode reabilitar áreas de limpeza predial',
        not_found_message='Área de limpeza predial não encontrada.',
        success_message='Status da área de limpeza predial atualizado com sucesso.',
        access_filters={
            "localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
    )



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def AreasAssociadasLocalidadeLimpezaPredial(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericListByParentIdRandom(
        request=request,
        parent_model=LocalidadeLimpezaPredial,
        child_model=AreaLimpezaPredial,
        serializer_class=AreaLimpezaPredialSerializer,
        parent_lookup_field='localidade__id_random',
        id_random=id_random,
        permission_type='limpeza_predial',
        permission_to_access=['252: Pode visualizar áreas de limpeza predial'],
        not_found_message='Localidade de limpeza predial não encontrada.',
        forbidden_message='Você não tem permissão para visualizar esta área de limpeza predial.',
        access_filters={
            "localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
    )



class ListAreasLimpezaPredial(GenericFilteredListView):
    model_class = AreaLimpezaPredial
    serializer_class = AreaLimpezaPredialSerializer
    permission_type = 'limpeza_predial'
    permission_code = '252: Pode visualizar áreas de limpeza predial'
    search_fields = ('id_random', 'nome', 'dimensao', 'servico', 'localidade', 'status')
    empresa_filter_paths = (
        "localidade__unidade__empresasecundaria__empresaprimaria__id_random",
        "localidade__unidade__empresasecundaria__id_random"
    )
