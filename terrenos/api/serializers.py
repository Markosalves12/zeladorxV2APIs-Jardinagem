from rest_framework import serializers
from terrenos.models import Terreno

class TerrenoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terreno
        fields = ['id', 'id_random', 'nome', 'EmpresaSecundaria', 'status', ]