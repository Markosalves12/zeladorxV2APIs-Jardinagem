from rest_framework import serializers
from checklists.models import CheckListJardinagem

class CheckListJardinagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckListJardinagem
        fields = ['id', 'id_random', 'servico_agendado', 'descricao', 'foto_comprovacao', 'status',]