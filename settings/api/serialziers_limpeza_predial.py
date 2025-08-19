from rest_framework import serializers
from settings.models import SettingServicosGerenteLimpezaPredial

class SettingServicosGerenteLimpezaPredialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingServicosGerenteLimpezaPredial
        fields = [
            'id', 'id_random', 'Gerente', 'NotificationsServicosAtrasados', 'NotificationsServicosProximos',
            'NotificationsServicosEmAndamento', 'NotificationsServicosCancelados', 'NotificationsServicosAgendados',
            'NotificationReportProductivity', 'NotificationReportServicosAtrasados',
            'NotificationReportServicosProximos', 'NotificationReportServicosEmAndamento',
            'NotificationReportServicosCancelados',
        ]