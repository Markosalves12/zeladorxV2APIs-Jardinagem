from rest_framework import serializers
from areas.models_jardinagem import AreasJardins

class AreasJardinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreasJardins
        fields = ['id_random', 'nome', 'dimensao', 'Terreno', 'vegetacao', 'servico', 'localidade', 'foto',
                  'periodicidade', 'status', ]
