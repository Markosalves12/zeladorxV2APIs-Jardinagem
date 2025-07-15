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


# Pega os detalhes da execucão, engajamento do time
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ListDetailFatoServicoJardinagem(request, id_random):
    user_id_random = request.user.id_random

    # Permissão
    if not validate_permissions(
        request=request,
        userid=user_id_random,
        permission_type='jardinagem',
        permission_to_access=['390: Pode visualizar o detalhamento de serviços']
    ):
        return Response(
            {"detail": "Você não tem permissão para visualizar execução de serviços de jardinagem"},
            status=status.HTTP_403_FORBIDDEN
        )

    # Queryset
    dados = colect_dados_fato_servico_jardinagem(
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

    serializer = FatoServicoJardinagemExportSerializer(dados, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)



class ListServicoJardinagemAgendadoAnotados(ListAPIView):
    serializer_class = ServicoJardinagemAgendadoAnnotatedSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = (
        'Areas__nome',
        'TipoServico__nome',
        'DescricaoDoServico',
        'ServicosEscalados__nome',
        'ColaboradoresEscalados__nome',
        'status',
        'dias_diferenca',
        'novo_status',
    )

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