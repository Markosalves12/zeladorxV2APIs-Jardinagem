from rest_framework import serializers
from permissionscontrol.models import PermissionsEspecials, PermissionsAccessEspecials

class PermissionsEspecialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionsEspecials
        fields = ['id', 'id_random', 'Permissions', ]


class PermissionsAccessEspecialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionsAccessEspecials
        fields = ['id', 'id_random', 'Gerente', 'Permissions', ]