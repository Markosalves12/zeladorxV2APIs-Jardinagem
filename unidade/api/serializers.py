from rest_framework import serializers
from unidade.models import Unidade

class UnidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidade
        fields = ['id_random', 'nome', 'linkmapajardinagem', 'linkmapalimnpezapredial', 'empresasecundaria', 'status']