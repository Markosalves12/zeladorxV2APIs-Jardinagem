from rest_framework import serializers
from medidor.models import DocsFromProcess


class DocsFromProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocsFromProcess
        fields = ['id_random', 'document', ]