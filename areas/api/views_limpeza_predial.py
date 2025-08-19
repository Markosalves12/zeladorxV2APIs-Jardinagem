from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from areas.api.serializer_limpeza_predial import AreaLimpezaPredialSerializer
from areas.models_limpeza_predial import AreaLimpezaPredial
from localidade.models_limpeza_predial import LocalidadeLimpezaPredial
from utils.views import (GenericDetailView, GenericUpdateView, GenericAlterStatusView, GenericFilteredListView,
                         GenericCreateView, GenericListByParentIdRandom, GenericIfDeleteView, GenericDeleteView)
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial
from empresasecundario.utils import define_empresas
from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado
from django.db.models import F, ExpressionWrapper, DurationField, CharField
from retornos.utils import formatar_tempo_desde
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status

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
        public_endpoint=False
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
        public_endpoint=False
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
        public_endpoint=False
    )



class ListAreasLimpezaPredial(GenericFilteredListView):
    model_class = AreaLimpezaPredial
    serializer_class = AreaLimpezaPredialSerializer
    permission_type = 'limpeza_predial'
    permission_code = '252: Pode visualizar áreas de limpeza predial'
    search_fields = ('id', 'id_random', 'nome', 'dimensao', 'servico', 'localidade', 'status')
    forbidden_message = "Você não tem permissão para visualizar áreas de limpeza predial."
    empresa_filter_paths = (
        "localidade__unidade__empresasecundaria__empresaprimaria__id_random",
        "localidade__unidade__empresasecundaria__id_random"
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
        forbidden_message="Você não tem permissão para visualizar áreas de limpeza predial.",
        access_filters={
            "localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def IfDeleteAreasLimpezaPredial(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericIfDeleteView(
        request,
        model=AreaLimpezaPredial,
        id_random=id_random,
        permission_type='limpeza_predial',
        permission_to_access=['253: Pode excluir áreas de limpeza predial'],
        access_filters={
            "localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        forbidden_message="Você não tem permissão para excluir esta área de limpeza predial."
    )



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteAreasLimpezaPredial(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericDeleteView(
        request,
        model=AreaLimpezaPredial,
        id_random=id_random,
        permission_type='limpeza_predial',
        permission_to_access=['253: Pode excluir áreas de limpeza predial'],
        access_filters={
            "localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        forbidden_message="Você não tem permissão para excluir esta área de limpeza predial."
    )


class ListAreasLimpezaPredialFromForms(GenericFilteredListView):
    model_class = AreaLimpezaPredial
    serializer_class = AreaLimpezaPredialSerializer
    permission_type = 'limpeza_predial'
    permission_code = '252: Pode visualizar áreas de limpeza predial'
    search_fields = ('id', 'id_random', 'nome', 'dimensao', 'servico', 'localidade', 'status')
    forbidden_message = "Você não tem permissão para visualizar áreas de limpeza predial."
    empresa_filter_paths = (
        "localidade__unidade__empresasecundaria__empresaprimaria__id_random",
        "localidade__unidade__empresasecundaria__id_random"
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            localidade__unidade__empresasecundaria__status__in=['Mobilizado'],
            status__in=['Mobilizado'],
            localidade__status__in=['Mobilizado'],
            localidade__unidade__status__in=['Mobilizado']
        )



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def TempoDesdeUltimoAtendimentoLimpezaPredial(request):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    setores = empresas['setores']


    if not (setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']):
        return Response(
            {"detail": "Limpeza predial não habilitada para esse usuário."},
            status=status.HTTP_403_FORBIDDEN
        )

    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']


    # Dias desde o atendimento até agora
    dados = ServicoLimpezaPredialAgendado.objects.filter(
        Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
        Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
        Areas__status='Mobilizado',
        status='Concluido'
    ).distinct('Areas__id_random').order_by('Areas__id_random', '-DataDeConclusao').annotate(
        dias_diferenca=ExpressionWrapper(
            timezone.now() - F('DataDeConclusao'),
            output_field=DurationField()
        )
    )

    resultado = []
    for obj in dados:
        tempo_desde = formatar_tempo_desde(obj.dias_diferenca)

        resultado.append({
            "id": obj.id,
            "Areas": str(obj.Areas),
            "DataDeInicio": obj.DataDeInicio,
            "DataDeConclusao": obj.DataDeConclusao,
            "ServicosEscalados": [str(s) for s in obj.ServicosEscalados.all()],
            "TipoServico": obj.TipoServico,
            "DescricaoDoServico": obj.DescricaoDoServico,
            "tempo_desde_ultimo_atendimento": tempo_desde,
        })

    return Response(resultado, status=status.HTTP_200_OK)