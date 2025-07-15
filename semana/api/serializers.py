from rest_framework import serializers
from semana.models import DiasDaSemana


class DiasDaSemanaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiasDaSemana
        fields = ['id', 'diasdasemana', ]