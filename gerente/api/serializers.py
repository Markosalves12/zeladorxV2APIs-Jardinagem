from rest_framework import serializers
from gerente.models import Gerente



class GerenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gerente
        fields = ['id', 'id_random', 'username', 'email', 'empresasecundaria', 'is_superuser', 'status']