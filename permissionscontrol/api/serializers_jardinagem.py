from rest_framework import serializers
from permissionscontrol.models import PermissionsJardinagem, PermissionsAccessJardinagem

class PermissionsJardinagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionsJardinagem
        fields = ['id', 'id_random', 'Permissions', ]


class PermissionsAccessJardinagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionsAccessJardinagem
        fields = ['id', 'id_random', 'Gerente', 'Permissions', ]