from rest_framework import serializers

class EmailResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ConfirmarTrocaSenhaSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)