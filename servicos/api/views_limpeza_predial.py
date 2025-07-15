# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from servicos.api.serializers_limpeza_predial import (ServicoLimpezaPredialAgendadoSerializer,
                                                 ServicoLimpezaPredialConfiguradoSerializer, FatoServicoLimpezaPredialSerializer)
from servicos.models_limpeza_predial import (ServicoLimpezaPredialConfigurado, ServicoLimpezaPredialAgendado,
                                             FatoServicoLimpezaPredial)



# Response: https://gist.github.com/mitchtabian/ae03573737067c9269701ea662460205
# Url: https://<your-domain>/api/blog/list
# Headers: Authorization: Token <token>
class ListServicoLimpezaPredialAgendado(ListAPIView):
    queryset = ServicoLimpezaPredialAgendado.objects.all()
    serializer_class = ServicoLimpezaPredialAgendadoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('Areas', 'TipoServico', 'DescricaoDoServico', 'ServicosEscalados', 'DataDeInicio',
                  'DataDeConclusao', 'ColaboradoresEscalados', 'foto_solicitacao', 'foto_entrega', 'status')



class ListServicoLimpezaPredialConfigurado(ListAPIView):
    queryset = ServicoLimpezaPredialConfigurado.objects.all()
    serializer_class = ServicoLimpezaPredialConfiguradoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('Areas', 'ServicosEscalados', 'tempomedioplanejado', 'diasaseremrealizado', 'horario_1',
                  'horario_2', 'horario_3', 'horario_4', 'horario_5',
                  'horario_6', 'horario_7' 'status')



class ListFatoLimpezaPredial(ListAPIView):
    queryset = FatoServicoLimpezaPredial.objects.all()
    serializer_class = FatoServicoLimpezaPredialSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('Servico', 'data_hora_chegada_na_area', 'data_hora_retorno_area', 'Gerente', 'foto_entrega', )