from rest_framework import serializers
from zeladorx.models import TypeZeladoria

class TypeZeladoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeZeladoria
        fields = ['id', 'setor', ]