from rest_framework import serializers
from settings.models import SettingServicosGerenteJardinagem

class SettingServicosGerenteJardinagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingServicosGerenteJardinagem
        fields = [
            'id', 'id_random', 'Gerente', 'NotificationsServicosAtrasados', 'NotificationsServicosProximos',
            'NotificationsServicosEmAndamento', 'NotificationsServicosCancelados',
            'NotificationsServicosAgendados', 'NotificationReportProductivity',
            'NotificationReportServicosAtrasados', 'NotificationReportServicosProximos',
            'NotificationReportServicosEmAndamento','NotificationReportServicosCancelados',
        ]