from rest_framework import serializers
from localidade.models_Jardinagem import LocalidadeJardiangem


class LocalidadeJardiangemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalidadeJardiangem
        fields = ['id', 'id_random', 'nome', 'lat_med', 'long_med', 'unidade', 'status', ]