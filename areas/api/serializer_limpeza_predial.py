from rest_framework import serializers
from areas.models_limpeza_predial import AreaLimpezaPredial

class AreaLimpezaPredialSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaLimpezaPredial
        fields = ['id_random', 'nome', 'dimensao',  'servico', 'localidade', 'foto', 'status', ]