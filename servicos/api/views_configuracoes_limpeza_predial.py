from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from servicos.api.serializers_limpeza_predial import ServicoLimpezaPredialConfiguradoSerializer
from servicos.models_limpeza_predial import ServicoLimpezaPredialConfigurado
from empresasecundario.utils import define_empresas
from utils.views import (GenericDetailView, GenericUpdateView, GenericAlterStatusView, GenericFilteredListView,
                         GenericCreateView, GenericIfDeleteView, GenericDeleteView)
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial
from areas.models_limpeza_predial import AreaLimpezaPredial


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateServicosConfiguradosLimpezaPredial(request):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    foreign_key_validations = [
        {
            "coluna": "ServicosEscalados",
            "model": CatalogodeServicoLimpezaPredial,
            "filters": {
                "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
                "EmpresaSecundaria__id_random__in": empresas_secundarias_ids,
                "EmpresaSecundaria__status__in": ['Mobilizado'],
                "status__in": ['Mobilizado']
            },
            "error_message": "Os servicos escalados estão desmobilizados ou nao pertencem a sua organização."
        },
        {
            "coluna": "Areas",
            "model": AreaLimpezaPredial,
            "filters": {
                "localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
                "localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
                "localidade__unidade__empresasecundaria__status__in": ['Mobilizado'],
                "status__in": ['Mobilizado'],
                "localidade__status__in": ['Mobilizado'],
                "localidade__unidade__status__in": ['Mobilizado']
            },
            "error_message": "A área selecionada esta desmobilizada ou nao pertence a sua organização"
        },
    ]

    return GenericCreateView(
        request=request,
        model_class=ServicoLimpezaPredialConfigurado,
        serializer_class=ServicoLimpezaPredialConfiguradoSerializer,
        permission_type="limpeza_predial",
        permission_to_access=['370: Pode configurar novos serviços'],
        forbidden_message="Você não tem permissão para criar servicos de limpeza predial configurados.",
        foreign_key_validations=foreign_key_validations,
        public_endpoint=False
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ServicosConfiguradosLimpezaPredialDetail(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericDetailView(
        request=request,
        model=ServicoLimpezaPredialConfigurado,
        serializer_class=ServicoLimpezaPredialConfiguradoSerializer,
        filters={"id_random": id_random},
        permission_type="limpeza_predial",
        permission_to_access=["372: Pode visualizar serviços configurados"],
        forbidden_message="Você não tem permissão para visualizar serviços de jardinagem configurados.",
        access_filters={
            "Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        }
    )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def ServicosConfiguradosLimpezaPredialUpdate(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericUpdateView(
        request=request,
        model=ServicoLimpezaPredialConfigurado,
        serializer_class=ServicoLimpezaPredialConfiguradoSerializer,
        filters={"id_random": id_random},
        permission_type="limpeza_predial",
        permission_to_access=['371: Pode editar serviços configurados'],
        forbidden_message="Você não tem permissão para editar serviços configurados de limpeza predial.",
        not_found_message="Permissão de jardinagem não encontrada.",
        access_filters={
            "Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        public_endpoint=False,
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def ServicosConfiguradosLimpezaPredialAlterStatus(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]


    return GenericAlterStatusView(
        request=request,
        model=ServicoLimpezaPredialConfigurado,
        filters={"id_random": id_random},
        permission_type="limpeza_predial",
        desmobilize_permission='374: Pode desmobilizar serviços configurados',
        rehabilitate_permission='375: Pode reabilitar serviços configurados',
        not_found_message="Área de jardinagem não encontrada.",
        success_message="Status da área de jardinagem atualizado com sucesso.",
        access_filters={
            "Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
    )


class ListServicoLimpezaPredialConfigurado(GenericFilteredListView):
    model_class = ServicoLimpezaPredialConfigurado
    serializer_class = ServicoLimpezaPredialConfiguradoSerializer
    permission_type = 'limpeza_predial'
    permission_code = "372: Pode visualizar serviços configurados"
    search_fields = ('id', 'id_random', 'Areas', 'ServicosEscalados', 'tempomedioplanejado', 'diasaseremrealizado',
                     'horario_1', 'horario_2', 'horario_3', 'horario_4', 'horario_5', 'horario_6',
                     'horario_7' 'status', )
    empresa_filter_paths = (
        "Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random",
        "Areas__localidade__unidade__empresasecundaria__id_random"
    )
    forbidden_message = "Você não pode visualizar serviços de limpeza predial configurados"



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def IfDeleteServicoLimpezaPredialConfigurado(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericIfDeleteView(
        request,
        model=ServicoLimpezaPredialConfigurado,
        id_random=id_random,
        permission_type='limpeza_predial',
        permission_to_access=['373: Pode excluir serviços configurados'],
        access_filters={
            "Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        forbidden_message="Você não tem permissão para excluir serviços configurados."
    )




@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteServicoLimpezaPredialConfigurado(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericDeleteView(
        request,
        model=ServicoLimpezaPredialConfigurado,
        id_random=id_random,
        permission_type='limpeza_predial',
        permission_to_access=['373: Pode excluir serviços configurados'],
        access_filters={
            "Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        forbidden_message="Você não tem permissão para excluir serviços configurados."
    )