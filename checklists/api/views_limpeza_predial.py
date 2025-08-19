from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from checklists.api.serializers_limpeza_predial import CheckListLimpezaPredialSerializer
from checklists.models import CheckListLimpezaPredial
from empresasecundario.utils import define_empresas
from utils.views import (GenericFilteredListView, GenericCreateView, GenericUpdateView, GenericDetailView,
                         GenericUpdateChecklistView, GenericDeleteView,
                         GenericIfDeleteView, GenericListChecklistByServico)
from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateCheckListLimpezaPredial(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    foreign_key_validations = [
        {
            "coluna": "servico_agendado",
            "model": ServicoLimpezaPredialAgendado,
            "filters": {
                "Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
                "Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
                "status__in": ['Agendado', 'Em andamento'],
                "id_random": id_random
            },
            "error_message": "O serviço agendado não pertence às empresas que você gerencia."
        },
    ]

    return GenericCreateView(
        request=request,
        model_class=CheckListLimpezaPredial,
        serializer_class=CheckListLimpezaPredialSerializer,
        permission_type="limpeza_predial",
        permission_to_access=['400: Pode criar novos checklists'],
        forbidden_message="Você não tem permissão para criar checklists de limpeza predial.",
        foreign_key_validations=foreign_key_validations,
        public_endpoint=False
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def CheckListLimpezaPredialUpdate(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericUpdateChecklistView(
        request=request,
        model=CheckListLimpezaPredial,
        serializer_class=CheckListLimpezaPredialSerializer,
        filters={"id_random": id_random},
        permission_type="jardinagem",
        permission_to_access=["401: Pode editar checklists"],
        forbidden_message="Você não tem permissão para editar este checklist de jardinagem.",
        not_found_message="Checklist nao encontrado.",
        access_filters={  # valida o escopo do objeto
            "servico_agendado__Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "servico_agendado__Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
            "servico_agendado__status__in": ['Agendado', 'Em andamento'],
        },
        public_endpoint=False,
    )




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CheckListLimpezaPredialDetails(request, id_random):
    user_id_random = request.user.id_random

    empresas = define_empresas(request=request, userid=user_id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericDetailView(
        request=request,
        model=CheckListLimpezaPredial,
        serializer_class=CheckListLimpezaPredialSerializer,
        filters={"id_random": id_random},  # busca o objeto
        access_filters={  # valida o escopo do objeto
            "servico_agendado__Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "servico_agendado__Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        permission_type='limpeza_predial',
        permission_to_access=['402: Pode visualizar checklists'],
        forbidden_message="Você não tem permissão para visualizar este checklist de limpeza predial."
    )



# Headers: Authorization: Token <token>
class ListCheckListLimpezaPredial(GenericFilteredListView):
    model_class = CheckListLimpezaPredial
    serializer_class = CheckListLimpezaPredialSerializer
    permission_type = 'limpeza_predial'
    permission_code = '402: Pode visualizar checklists'
    search_fields = ('id', 'id_random', 'servico_agendado', 'descricao', 'foto_comprovacao', 'status')
    empresa_filter_paths = (
        "servico_agendado__Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random",
        "servico_agendado__Areas__localidade__unidade__empresasecundaria__id_random"
    )
    forbidden_message="Você não tem permissão para visualizar este checklist de limpeza predial."



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def IfDeleteCheckListLimpezaPredail(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericIfDeleteView(
        request,
        model=CheckListLimpezaPredial,
        id_random=id_random,
        permission_type='limpeza_predial',
        permission_to_access=['403: Pode excluir checklists'],
        access_filters={
            "servico_agendado__Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "servico_agendado__Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        forbidden_message="Você não tem permissão para excluir este checklist."
    )



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteCheckListLimpezaPredail(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericDeleteView(
        request,
        model=CheckListLimpezaPredial,
        id_random=id_random,
        permission_type='limpeza_predial',
        permission_to_access=['403: Pode excluir checklists'],
        access_filters={
            "servico_agendado__Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "servico_agendado__Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        forbidden_message="Você não tem permissão para excluir este checklist."
    )



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ListCheckListLimpezaPredialByServico(request, id_random):
    # verifica se o serviço existe
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']


    return GenericListChecklistByServico(
        request=request,
        servico_model=ServicoLimpezaPredialAgendado,
        related_model=CheckListLimpezaPredial,
        serializer_class=CheckListLimpezaPredialSerializer,
        permission_type='limpeza_predial',
        permission_to_access=['402: Pode visualizar checklists'],
        forbidden_message="Você não tem permissão para visualizar este conteúdo.",
        not_found_message="Serviço de jardinagem não encontrado.",
        filters_related_model={
            "servico_agendado__Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "servico_agendado__Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
            "servico_agendado__id_random": id_random
        },  # se quiser filtrar algo a mais, adicione aqui
        servico_id_random=id_random
    )