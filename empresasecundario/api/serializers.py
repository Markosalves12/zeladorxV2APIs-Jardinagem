from rest_framework import serializers
from empresasecundario.models import EmpresaSecundaria

class EmpresaSecundariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpresaSecundaria
        fields = ['id', 'id_random', 'nome', 'setor', 'empresaprimaria', 'status', ]