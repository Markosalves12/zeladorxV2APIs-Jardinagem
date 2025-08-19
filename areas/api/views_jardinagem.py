from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from areas.api.serializers_jardinagem import AreasJardinsSerializer
from areas.models_jardinagem import AreasJardins
from localidade.models_Jardinagem import LocalidadeJardiangem
from utils.views import (GenericDetailView, GenericUpdateView, GenericAlterStatusView, GenericFilteredListView,
                         GenericCreateView, GenericListByParentIdRandom, GenericIfDeleteView,
                         GenericFilteredListViewFromForms, GenericDeleteView)


from catalogo_de_servicos.models_jardinagem import CatalogodeServicoJardinagem
from vegetacao.models import CatalogoVegetacao
from terrenos.models import Terreno
from empresasecundario.utils import define_empresas
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import F, ExpressionWrapper, DurationField, CharField
from retornos.utils import formatar_tempo_desde, calcular_data_retorno_formatada
from servicos.models_jardinagem import ServicoJardinagemAgendado

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateAreaJardinagem(request):
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
            "error_message": "A vegetação selecionada está desmobilizada ou fora do seu escopo de empresas."
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
            "error_message": "O terreno selecionado está desmobilizado ou fora do seu escopo de empresas."
        }
    ]

    return GenericCreateView(
        request=request,
        model_class=AreasJardins,
        serializer_class=AreasJardinsSerializer,
        permission_type="jardinagem",
        permission_to_access=['250: Pode criar novas áreas de jardinagem'],
        forbidden_message="Você não tem permissão para criar áreas de jardinagem.",
        foreign_key_validations=foreign_key_validations,
        public_endpoint=False
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def AreasJardinagemDetail(request, id_random):
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
def AreasJardinagemUpdate(request, id_random):
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
        public_endpoint=False
    )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def AreasJardinagemAlterStatus(request, id_random):
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
        public_endpoint=False
    )



# Headers: Authorization: Token <token>
class ListAreasJardinagem(GenericFilteredListView):
    model_class = AreasJardins
    serializer_class = AreasJardinsSerializer
    permission_type = 'jardinagem'
    permission_code = '252: Pode visualizar áreas de jardinagem'
    search_fields = ('id', 'id_random', 'nome', 'dimensao', 'Terreno', 'vegetacao', 'servico', 'localidade', 'periodicidade', 'status')
    forbidden_message = "Você não tem permissão para visualizar áreas de jardinagem."
    empresa_filter_paths = (
        "localidade__unidade__empresasecundaria__empresaprimaria__id_random",
        "localidade__unidade__empresasecundaria__id_random"
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def AreasAssociadasLocalidadeJardinagem(request, id_random):
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
        forbidden_message="Você não tem permissão para visualizar áreas de jardinagem.",
        access_filters={
            "localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def IfDeleteAreasJardinagem(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericIfDeleteView(
        request,
        model=AreasJardins,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['253: Pode excluir áreas de jardinagem'],
        access_filters={
            "localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        forbidden_message="Você não tem permissão para excluir esta área de jardinagem."
    )


class ListAreasJardinagemFromFoms(GenericFilteredListViewFromForms):
    model_class = AreasJardins
    serializer_class = AreasJardinsSerializer
    search_fields = (
        'id', 'id_random', 'nome', 'dimensao', 'Terreno', 'vegetacao',
        'servico', 'localidade', 'periodicidade', 'status'
    )
    forbidden_message = "Você não tem permissão para visualizar áreas de jardinagem."
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
def TempoDesdeUltimoAtendimentoJardinagem(request):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    setores = empresas['setores']

    if not (setores['habilitar_jardinagem'] and setores['habilitar_jardinagem_secundaria']):
        return Response(
            {"detail": "Jardinagem não habilitada para esse usuário."},
            status=status.HTTP_403_FORBIDDEN
        )

    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    dados = ServicoJardinagemAgendado.objects.filter(
        Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
        Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
        Areas__status='Mobilizado',
        status='Concluido'
    ).distinct('Areas__id_random').order_by('Areas__id_random', '-DataDeConclusao').annotate(
        dias_diferenca=ExpressionWrapper(
            timezone.now() - F('DataDeConclusao'),
            output_field=DurationField()
        ),
        Periodicidade=F('Areas__periodicidade')
    )

    resultado = []
    for obj in dados:
        tempo_desde = formatar_tempo_desde(obj.dias_diferenca)
        data_retorno, dias_restantes = calcular_data_retorno_formatada(
            obj.DataDeConclusao.date(),
            obj.Periodicidade
        )

        resultado.append({
            "id": obj.id,
            "Areas": str(obj.Areas),
            "Periodicidade": obj.Periodicidade,
            "DataDeInicio": obj.DataDeInicio,
            "DataDeConclusao": obj.DataDeConclusao,
            "ServicosEscalados": [str(s) for s in obj.ServicosEscalados.all()],
            "ColaboradoresEscalados": [str(c) for c in obj.ColaboradoresEscalados.all()],
            "TipoServico": obj.TipoServico,
            "DescricaoDoServico": obj.DescricaoDoServico,
            "tempo_desde_ultimo_atendimento": tempo_desde,
            "data_retorno_formatada": data_retorno,
            "dias_restantes": dias_restantes
        })

    return Response(resultado, status=status.HTTP_200_OK)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteAreasJardinagem(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericDeleteView(
        request,
        model=AreasJardins,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['253: Pode excluir áreas de jardinagem'],
        access_filters={
            "localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        forbidden_message="Você não tem permissão para excluir esta área de jardinagem."
    )