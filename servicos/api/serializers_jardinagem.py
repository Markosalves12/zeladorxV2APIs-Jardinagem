from rest_framework import serializers
from servicos.models_jardinagem import ServicoJardinagemAgendado, ServicoJardinagemConfigurado, FatoServicoJardinagem

class ServicoJardinagemAgendadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicoJardinagemAgendado
        fields = ['id_random', 'Areas', 'TipoServico', 'DescricaoDoServico', 'ServicosEscalados', 'DataDeInicio',
                  'DataDeConclusao', 'ColaboradoresEscalados', 'foto_solicitacao', 'foto_entrega',]


class ServicoJardinagemConfiguradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicoJardinagemConfigurado
        fields = ['id_random', 'Areas', 'ServicosEscalados', 'tempomedioplanejado', 'diasaseremrealizado','horario_1',
                  'horario_2', 'horario_3', 'horario_4', 'horario_5',
                  'horario_6', 'horario_7', 'status']


class FatoServicoJardinagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FatoServicoJardinagem
        fields = ['id_random', 'Servico', 'data_hora_chegada_na_area', 'data_hora_retorno_area', 'Gerente']




class ServicoJardinagemAgendadoAnnotatedSerializer(serializers.Serializer):
    id_random = serializers.CharField()
    DescricaoDoServico = serializers.CharField()
    DataDeInicio = serializers.DateTimeField()
    DataDeConclusao = serializers.DateTimeField()
    TipoServico = serializers.PrimaryKeyRelatedField(read_only=True)
    Areas = serializers.PrimaryKeyRelatedField(read_only=True)
    ServicosEscalados = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    ColaboradoresEscalados = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    foto_solicitacao = serializers.ImageField(allow_null=True, required=False)
    foto_entrega = serializers.ImageField(allow_null=True, required=False)

    # Campos anotados
    dias_diferenca = serializers.IntegerField()
    novo_status = serializers.CharField()



class FatoServicoJardinagemExportSerializer(serializers.Serializer):
    id_acompanhamento = serializers.IntegerField()
    id_random_acompanhamento = serializers.CharField()

    id_agendamento = serializers.IntegerField()
    id_random_agendamento = serializers.CharField()

    colaboradores_chamados_id = serializers.IntegerField()
    colaboradores_chamados_id_random = serializers.CharField()
    colaboradores_chamados = serializers.CharField()

    data_hora_chegada = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    data_hora_retorno = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    tempo_na_area = serializers.DurationField()