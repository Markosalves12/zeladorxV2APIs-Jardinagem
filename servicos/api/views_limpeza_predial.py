from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from servicos.api.serializers_limpeza_predial import ServicoLimpezaPredialAgendadoSerializer, ServicoLimpezaPredialAgendadoAnnotatedSerializer
from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado
from empresasecundario.utils import define_empresas
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial
from areas.models_limpeza_predial import AreaLimpezaPredial
from utils.views import (GenericCreateView, GenericDetailView, GenericUpdateView, GenericIfDeleteView,
                         alterar_status_servico_agendado, GenericDeleteView)
from permissionscontrol.utils import validate_permissions
from rest_framework.exceptions import PermissionDenied
from servicos.utils_limpeza_predial import query_servicos_limpeza_predial_agendados_anotados

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateServicosLimpezaPredial(request):
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
            "error_message": "Servicos selecionados não estão mobilizadas ou não pertence às empresas que você gerencia."
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
            "error_message": "A área selecionada não está mobilizada ou não pertence às empresas que você gerencia."
        },
    ]

    return GenericCreateView(
        request=request,
        model_class=ServicoLimpezaPredialAgendado,
        serializer_class=ServicoLimpezaPredialAgendadoSerializer,
        permission_type="limpeza_predial",
        permission_to_access=['320: Pode agendar novos serviços'],
        forbidden_message="Você não tem permissão para agendar novos serviços de limpeza predial.",
        foreign_key_validations=foreign_key_validations,
        public_endpoint=False
    )



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ServicosLimpezaPredialDetail(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericDetailView(
        request=request,
        model=ServicoLimpezaPredialAgendado,
        serializer_class=ServicoLimpezaPredialAgendadoSerializer,
        filters={"id_random": id_random},
        permission_type="limpeza_predial",
        permission_to_access=['322: Pode visualizar serviços agendados'],
        forbidden_message="Você não tem permissão para visualizar serviços de limpeza predial agendados.",
        access_filters={
            "Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        }
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def ServicosLimpezaPredailUpdate(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericUpdateView(
        request=request,
        model=ServicoLimpezaPredialAgendado,
        serializer_class=ServicoLimpezaPredialAgendadoSerializer,
        filters={"id_random": id_random},
        permission_type="limpeza_predial",
        permission_to_access=['321: Pode editar serviços agendados'],
        forbidden_message="Você não tem permissão para editar serviços de limpeza predial agendados.",
        not_found_message="Serviço de limpeza predial não encontrada.",
        access_filters={
            "Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        public_endpoint=False,
    )


class ListServicoLimpezaPredialAgendadoAnotados(ListAPIView):
    serializer_class = ServicoLimpezaPredialAgendadoAnnotatedSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)

    def get_queryset(self):
        user_id_random = self.request.user.id_random

        if not validate_permissions(
            request=self.request,
            userid=user_id_random,
            permission_type='limpeza_predial',
            permission_to_access=['322: Pode visualizar serviços agendados']
        ):
            raise PermissionDenied("Você não tem permissão para visualizar serviços de limpeza predial agendados.")

        agendado = query_servicos_limpeza_predial_agendados_anotados(
            self.request,
            user_id_random,
            status_list=['Agendado', 'Em andamento']
        )

        return agendado


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def IfDeleteServicoAgendadoLimpezaPredial(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericIfDeleteView(
        request,
        model=ServicoLimpezaPredialAgendado,
        id_random=id_random,
        permission_type='limpeza_predial',
        permission_to_access=['323: Pode excluir serviços agendados'],
        access_filters={
            "Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        forbidden_message="Você não tem permissão para excluir esta área de jardinagem.",
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteServicoAgendadoLimpezaPredial(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericDeleteView(
        request,
        model=ServicoLimpezaPredialAgendado,
        id_random=id_random,
        permission_type='limpeza_predial',
        permission_to_access=['323: Pode excluir serviços agendados'],
        access_filters={
            "Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        forbidden_message="Você não tem permissão para excluir esta área de jardinagem.",
    )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def alterar_status_servico_limpeza_predial(request, id_random):
    return alterar_status_servico_agendado(
        request=request,
        model=ServicoLimpezaPredialAgendado,
        permission_type="limpeza_predial",
        id_random=id_random,
    )
