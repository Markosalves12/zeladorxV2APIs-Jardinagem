from rest_framework import serializers
from permissionscontrol.models import PermissionsLimpezaPredial, PermissionsAccessLimpezaPredial


class PermissionsLimpezaPredialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionsLimpezaPredial
        fields = ['id', 'id_random', 'Permissions', ]


class PermissionsAccessLimpezaPredialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionsAccessLimpezaPredial
        fields = ['id', 'id_random', 'Gerente', 'Permissions', ]