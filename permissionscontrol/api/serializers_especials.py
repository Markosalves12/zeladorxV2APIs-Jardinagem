from rest_framework import serializers
from permissionscontrol.models import PermissionsEspecials, PermissionsAccessEspecials

class PermissionsEspecialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionsEspecials
        fields = ['id_random', 'Permissions', ]


class PermissionsAccessEspecialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionsAccessEspecials
        fields = ['id_random', 'Gerente', 'Permissions', ]