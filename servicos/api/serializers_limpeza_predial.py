from rest_framework import serializers
from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado, ServicoLimpezaPredialConfigurado, FatoServicoLimpezaPredial

class ServicoLimpezaPredialAgendadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicoLimpezaPredialAgendado
        fields = ['id_random', 'Areas', 'TipoServico', 'DescricaoDoServico', 'ServicosEscalados', 'DataDeInicio',
                  'DataDeConclusao', ]


class ServicoLimpezaPredialConfiguradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicoLimpezaPredialConfigurado
        fields = ['id_random', 'Areas', 'ServicosEscalados', 'tempomedioplanejado', 'diasaseremrealizado', 'horario_1',
                  'horario_2', 'horario_3', 'horario_4', 'horario_5',
                  'horario_6', 'horario_7', 'status']


class FatoServicoLimpezaPredialSerializer(serializers.ModelSerializer):
    class Meta:
        model = FatoServicoLimpezaPredial
        fields = ['id_random', 'Servico', 'data_hora_chegada_na_area', 'data_hora_retorno_area', 'Gerente', 'foto_entrega']