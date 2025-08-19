from rest_framework import serializers
from empresaprimaria.models import EmpresaPrimaria

class EmpresaSecundariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpresaPrimaria
        fields = ['id', "id_random", "nome", "N_unidades", "status", "setor", ]