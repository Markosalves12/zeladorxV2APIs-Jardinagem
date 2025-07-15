from rest_framework import serializers
from localidade.models_limpeza_predial import LocalidadeLimpezaPredial


class LocalidadeLimpezaPredialSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalidadeLimpezaPredial
        fields = ['id_random', 'nome', 'lat_med', 'long_med', 'unidade', 'status', ]