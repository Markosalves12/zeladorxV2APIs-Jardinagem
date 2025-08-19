from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from servicos.api.serializers_jardinagem import (ServicoJardinagemAgendadoSerializer,
                                                 ServicoJardinagemAgendadoAnnotatedSerializer)
from servicos.models_jardinagem import ServicoJardinagemAgendado
from servicos.utils_jardinagem import query_servicos_jardinagem_agendados_anotados
from empresasecundario.utils import define_empresas
from permissionscontrol.utils import validate_permissions
from rest_framework.exceptions import PermissionDenied
from utils.views import (GenericCreateView, GenericDetailView, GenericUpdateView, GenericIfDeleteView,
                         alterar_status_servico_agendado, GenericFilteredListView, GenericDeleteView)
from catalogo_de_servicos.models_jardinagem import CatalogodeServicoJardinagem
from gerente.models import Gerente
from areas.models_jardinagem import AreasJardins


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateServicosJardinagem(request):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    foreign_key_validations = [
        {
            "coluna": "ServicosEscalados",
            "model": CatalogodeServicoJardinagem,
            "filters": {
                "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
                "EmpresaSecundaria__id_random__in": empresas_secundarias_ids,
                "EmpresaSecundaria__status__in": ['Mobilizado'],
                "status__in": ['Mobilizado']
            },
            "error_message": "Servicos selecionados não estão mobilizadas ou não pertence às empresas que você gerencia."
        },
        {
            "coluna": "ColaboradoresEscalados",
            "model": Gerente,
            "filters": {
                "empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
                "empresasecundaria__id_random__in": empresas_secundarias_ids,
                "empresasecundaria__status__in": ['Mobilizado'],
                "empresasecundaria__setor__setor__in": ['Jardinagem'],
                "status__in": ['Mobilizado']
            },
            "error_message": "Gerentes selecionados não estão mobilizados ou não pertencem às empresas que você gerencia."
        },
        {
            "coluna": "Areas",
            "model": AreasJardins,
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
        model_class=ServicoJardinagemAgendado,
        serializer_class=ServicoJardinagemAgendadoSerializer,
        permission_type="jardinagem",
        permission_to_access=['320: Pode agendar novos serviços'],
        forbidden_message="Você não tem permissão para agendar novos serviços de jardinagem.",
        foreign_key_validations=foreign_key_validations,
        public_endpoint=False
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ServicosJardinagemDetail(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericDetailView(
        request=request,
        model=ServicoJardinagemAgendado,
        serializer_class=ServicoJardinagemAgendadoSerializer,
        filters={"id_random": id_random},
        permission_type="jardinagem",
        permission_to_access=['322: Pode visualizar serviços agendados'],
        forbidden_message="Você não tem permissão para visualizar serviços de jardinagem agendados.",
        access_filters={
            "Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        }
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def ServicosJardinagemUpdate(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericUpdateView(
        request=request,
        model=ServicoJardinagemAgendado,
        serializer_class=ServicoJardinagemAgendadoSerializer,
        filters={"id_random": id_random},
        permission_type="jardinagem",
        permission_to_access=['321: Pode editar serviços agendados'],
        forbidden_message="Você não tem permissão para editar serviços de jardinagem agendados.",
        not_found_message="Serviço de jardinagem não encontrada.",
        access_filters={
            "Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        public_endpoint=False,
    )


class ListServicoJardinagemAgendadoAnotados(ListAPIView):
    serializer_class = ServicoJardinagemAgendadoAnnotatedSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)

    def get_queryset(self):
        user_id_random = self.request.user.id_random

        if not validate_permissions(
            request=self.request,
            userid=user_id_random,
            permission_type='jardinagem',
            permission_to_access=['322: Pode visualizar serviços agendados']
        ):
            raise PermissionDenied("Você não tem permissão para visualizar serviços de jardinagem agendados.")

        auto_acompleshed = validate_permissions(
            request=self.request,
            userid=user_id_random,
            permission_type='jardinagem',
            permission_to_access=['361: Pode acompanhar serviços agendados para si próprio']
        )

        agendado = query_servicos_jardinagem_agendados_anotados(
            self.request,
            user_id_random,
            status_list=['Agendado', 'Em andamento']
        )

        gerente = Gerente.objects.get(id_random=user_id_random)
        if auto_acompleshed and not gerente.is_superuser:
            agendado = agendado.filter(ColaboradoresEscalados__id_random__in=[user_id_random, 'MuUe1D3pvT3v'])

        return agendado



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def IfDeleteServicoAgendadoJardinagem(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericIfDeleteView(
        request,
        model=ServicoJardinagemAgendado,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['323: Pode excluir serviços agendados'],
        access_filters={
            "Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        forbidden_message="Você não tem permissão para excluir este serviço agendado."
    )



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteServicoAgendadoJardinagem(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericDeleteView(
        request,
        model=ServicoJardinagemAgendado,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['323: Pode excluir serviços agendados'],
        access_filters={
            "Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        forbidden_message="Você não tem permissão para excluir este serviço agendado."
    )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def alterar_status_servico_jardinagem(request, id_random):
    return alterar_status_servico_agendado(
        request=request,
        id_random=id_random,
        model=ServicoJardinagemAgendado,
        permission_type="jardinagem"
    )