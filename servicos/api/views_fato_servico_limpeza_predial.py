from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from servicos.utils_limpeza_predial import colect_dados_fato_servico_limpeza_predial
from empresasecundario.utils import define_empresas
from permissionscontrol.utils import validate_permissions
from gerente.models import Gerente
from servicos.models_limpeza_predial import FatoServicoLimpezaPredial, ServicoLimpezaPredialAgendado
from servicos.api.serializers_limpeza_predial import FatoServicoLimpezaPredialSerializer
from utils.views import (GenericCreateView, GenericDetailView, GenericUpdateView,
                         GenericIfDeleteView, GenericDeleteView)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateFatoServicoLimpezaPredial(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    foreign_key_validations = [
        {
            "coluna": "Servico",
            "model": ServicoLimpezaPredialAgendado,
            "filters": {
                "id_random": id_random
            },
            "error_message": "Os servicos servico selecionado não é gerenciado pela sua organização."
        },
        {
            "coluna": "Gerente",
            "model": Gerente,
            "filters": {
                "empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
                "empresasecundaria__id_random__in": empresas_secundarias_ids,
                "empresasecundaria__status__in": ['Mobilizado'],
                "empresasecundaria__setor__setor__in": ['Limpeza predial'],
                "status__in": ['Mobilizado']
            },
            "error_message": "O colaborador selecionada esta desmobilizada ou nao pertence a sua organização"
        },
    ]

    return GenericCreateView(
        request=request,
        model_class=FatoServicoLimpezaPredial,
        serializer_class=FatoServicoLimpezaPredialSerializer,
        permission_type="limpeza_predial",
        permission_to_access=['324: Pode acompanhar serviços agendados'],
        forbidden_message="Você não tem permissão para acompanhar serviços.",
        foreign_key_validations=foreign_key_validations,
        public_endpoint=False
    )



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def FatoServicoLimpezaPredialDetail(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericDetailView(
        request=request,
        model=FatoServicoLimpezaPredial,
            serializer_class=FatoServicoLimpezaPredialSerializer,
        filters={"id_random": id_random},
        permission_type="limpeza_predial",
        permission_to_access=['390: Pode visualizar o detalhamento de serviços'],
        forbidden_message="Você não tem permissão para visualizar acompanhamentos de limpeza predial.",
        access_filters={
            "Servico__Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Servico__Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
    )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def FatoServicoLimpezaPredialUpdate(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericUpdateView(
        request=request,
        model=FatoServicoLimpezaPredial,
        serializer_class=FatoServicoLimpezaPredialSerializer,
        filters={"id_random": id_random},
        permission_type="limpeza_predial",
        permission_to_access=['391: Pode editar o acompanhamento de servicos'],  #atualizar essa permissão
        forbidden_message="Você não tem permissão para editar acompanhamentos.",
        not_found_message="acompanhamento de limpeza predial não encontrada.",
        access_filters={
            "Servico__Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Servico__Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        public_endpoint=False,
    )


# Pega os detalhes da execucão, engajamento do time
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ListFatoServicoLimpezaPredialByservico(request, id_random):
    user_id_random = request.user.id_random

    # Permissão
    if not validate_permissions(
        request=request,
        userid=user_id_random,
        permission_type='limpeza_predial',
        permission_to_access=['390: Pode visualizar o detalhamento de serviços']
    ):
        return Response(
            {"detail": "Você não tem permissão para visualizar execução de serviços de limpeza predial"},
            status=status.HTTP_403_FORBIDDEN
        )

    # Queryset
    dados = colect_dados_fato_servico_limpeza_predial(
        request=request,
        userid=user_id_random,
        DataDeInicio=None,
        DataDeConclusao=None,
        ServicosEscalados=None,
        ColaboradoresEscalados=None,
        TipoServico=None,
        Areas=None,
        status=['Concluido', 'Agendado', 'Em andamento']
    ).filter(Servico__id_random=id_random)

    serializer = FatoServicoLimpezaPredialSerializer(dados, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ListFatoServicoLimpezaPredial(request):
    user_id_random = request.user.id_random

    # Permissão
    if not validate_permissions(
        request=request,
        userid=user_id_random,
        permission_type='limpeza_predial',
        permission_to_access=['390: Pode visualizar o detalhamento de serviços']
    ):
        return Response(
            {"detail": "Você não tem permissão para visualizar execução de serviços de limpeza predial"},
            status=status.HTTP_403_FORBIDDEN
        )

    # Queryset
    dados = colect_dados_fato_servico_limpeza_predial(
        request=request,
        userid=user_id_random,
        DataDeInicio=None,
        DataDeConclusao=None,
        ServicosEscalados=None,
        ColaboradoresEscalados=None,
        TipoServico=None,
        Areas=None,
        status=['Concluido', 'Agendado', 'Em andamento']
    )

    serializer = FatoServicoLimpezaPredialSerializer(dados, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def IfDeleteFatoServicoLimpezaPredial(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericIfDeleteView(
        request,
        model=FatoServicoLimpezaPredial,
        id_random=id_random,
        permission_type='limpeza_predial',
        permission_to_access=['323: Pode excluir serviços concluidos'],#corrigir essa permissão
        access_filters={
            "Servico__Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Servico__Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        forbidden_message="Você não tem permissão para excluir este acompanhamento."
    )




@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteFatoServicoLimpezaPredial(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericDeleteView(
        request,
        model=FatoServicoLimpezaPredial,
        id_random=id_random,
        permission_type='limpeza_predial',
        permission_to_access=['323: Pode excluir serviços concluidos'],#corrigir essa permissão
        access_filters={
            "Servico__Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Servico__Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        forbidden_message="Você não tem permissão para excluir este acompanhamento."
    )