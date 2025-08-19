from rest_framework import serializers
from vegetacao.models import CatalogoVegetacao

class CatalogoVegetacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoVegetacao
        fields = ['id', 'id_random', 'nome', 'EmpresaSecundaria', 'status']