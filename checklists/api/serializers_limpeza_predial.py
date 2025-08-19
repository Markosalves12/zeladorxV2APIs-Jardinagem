from rest_framework import serializers
from checklists.models import CheckListLimpezaPredial

class CheckListLimpezaPredialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckListLimpezaPredial
        fields = ['id', 'id_random', 'servico_agendado', 'descricao', 'foto_comprovacao', 'status',]