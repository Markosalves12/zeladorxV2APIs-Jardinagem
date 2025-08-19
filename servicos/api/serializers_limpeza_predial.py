from rest_framework import serializers
from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado, ServicoLimpezaPredialConfigurado, FatoServicoLimpezaPredial

class ServicoLimpezaPredialAgendadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicoLimpezaPredialAgendado
        fields = ['id', 'id_random', 'Areas', 'TipoServico', 'DescricaoDoServico', 'ServicosEscalados', 'DataDeInicio',
                  'DataDeConclusao', ]


class ServicoLimpezaPredialConfiguradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicoLimpezaPredialConfigurado
        fields = ['id', 'id_random', 'Areas', 'ServicosEscalados', 'tempomedioplanejado', 'diasaseremrealizado', 'horario_1',
                  'horario_2', 'horario_3', 'horario_4', 'horario_5',
                  'horario_6', 'horario_7', 'status']


class FatoServicoLimpezaPredialSerializer(serializers.ModelSerializer):
    class Meta:
        model = FatoServicoLimpezaPredial
        fields = ['id', 'id_random', 'Servico', 'data_hora_chegada_na_area', 'data_hora_retorno_area', 'Gerente', 'foto_entrega']



class ServicoLimpezaPredialAgendadoAnnotatedSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    id_random = serializers.CharField()
    DescricaoDoServico = serializers.CharField()
    DataDeInicio = serializers.DateTimeField()
    DataDeConclusao = serializers.DateTimeField()
    TipoServico = serializers.PrimaryKeyRelatedField(read_only=True)
    Areas = serializers.PrimaryKeyRelatedField(read_only=True)
    ServicosEscalados = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # Campos anotados
    dias_diferenca = serializers.IntegerField()
    novo_status = serializers.CharField()