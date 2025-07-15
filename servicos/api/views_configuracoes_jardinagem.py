from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from servicos.api.serializers_jardinagem import (ServicoJardinagemAgendadoSerializer,
                                                 ServicoJardinagemConfiguradoSerializer,
                                                 FatoServicoJardinagemSerializer, FatoServicoJardinagemExportSerializer,
                                                 ServicoJardinagemAgendadoAnnotatedSerializer)
from servicos.models_jardinagem import ServicoJardinagemConfigurado, ServicoJardinagemAgendado, FatoServicoJardinagem
from servicos.utils_jardinagem import query_servicos_jardinagem_agendados_anotados, colect_dados_fato_servico_jardinagem
from empresasecundario.utils import define_empresas
from permissionscontrol.utils import validate_permissions
from rest_framework.exceptions import PermissionDenied
from gerente.models import Gerente

from utils.views import GenericDetailView, GenericUpdateView


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ServicosConfiguradosJardinsDetail(request, id_random):
    return GenericDetailView(
        request=request,
        model=ServicoJardinagemConfigurado,
        serializer_class=ServicoJardinagemConfiguradoSerializer,
        filters={"id_random": id_random},
        permission_type="jardinagem",
        permission_to_access=["372: Pode visualizar serviços configurados"],
        forbidden_message="Você não tem permissão para visualizar serviços de jardinagem configurados."
    )



def ServicosConfiguradosJardinsUpdate(request, id_random):
    return GenericUpdateView(
        request=request,
        model=ServicoJardinagemConfigurado,
        serializer_class=ServicoJardinagemConfiguradoSerializer,
        filters={"id_random": id_random},
        permission_type="jardinagem",
        permission_to_access=['371: Pode editar serviços configurados'],
        forbidden_message="Você não tem permissão para editar serviços configurados de jardinagem.",
        not_found_message="Permissão de jardinagem não encontrada."
    )



class ListServicoJardinagemConfigurado(ListAPIView):
    serializer_class = ServicoJardinagemConfiguradoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('id_random', 'Areas', 'ServicosEscalados', 'tempomedioplanejado', 'diasaseremrealizado',
                     'horario_1', 'horario_2', 'horario_3', 'horario_4', 'horario_5', 'horario_6',
                     'horario_7' 'status')


    def get_queryset(self):
        user_id_random = self.request.user.id_random

        # Verifica permissão
        if not validate_permissions(
            request=self.request,
            userid=user_id_random,
            permission_type='jardinagem',
            permission_to_access=['372: Pode visualizar serviços configurados']
        ):
            raise PermissionDenied("Você não tem permissão para visualizar servicos de jardinagem configurados.")

        empresas = define_empresas(request=self.request, userid=user_id_random)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        empresas_secundarias_ids = empresas['empresas_secundarias_ids']

        return ServicoJardinagemConfigurado.objects.filter(
            Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
        ).distinct()

