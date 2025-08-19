from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from settings.api.serialziers_limpeza_predial import SettingServicosGerenteLimpezaPredialSerializer
from settings.models import SettingServicosGerenteLimpezaPredial
from utils.views import GenericDetailView, GenericUpdateView, GenericFilteredListView
from empresasecundario.utils import define_empresas

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def SettingServicosGerenteLimpezaPredialDetail(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericDetailView(
        request=request,
        model=SettingServicosGerenteLimpezaPredial,
        serializer_class=SettingServicosGerenteLimpezaPredialSerializer,
        filters={"id_random": id_random},
        permission_type="limpeza_predial",
        permission_to_access=["410: Pode editar o recebimento de notificações gerais"],
        forbidden_message="Você não tem permissão para visualizar configuracoes de limpeza predial.",
        access_filters={
            "Gerente__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Gerente__empresasecundaria__id_random__in": empresas_secundarias_ids,
        }
    )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def SettingServicosGerenteLimpezaPredialUpdate(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    # Pega configuração original
    configuracao = SettingServicosGerenteLimpezaPredial.objects.get(id_random=id_random)
    gerente_id = configuracao.Gerente.id  # preserva o gerente original

    # Copia os dados e força o campo Gerente a permanecer igual
    data = request.data.copy()
    data['Gerente'] = gerente_id  # impede alteração

    return GenericUpdateView(
        request=request,
        model=SettingServicosGerenteLimpezaPredial,
        serializer_class=SettingServicosGerenteLimpezaPredialSerializer,
        filters={"id_random": id_random},
        permission_type="limpeza_predial",
        permission_to_access=["410: Pode editar o recebimento de notificações gerais"],
        forbidden_message="Você não tem permissão para editar localidades de jardinagem.",
        not_found_message="Localidade de jardinagem não encontrada.",
        access_filters={
            "Gerente__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Gerente__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        public_endpoint=False,
    )



class ListSettingServicosGerenteLimpezaPredial(GenericFilteredListView):
    model_class = SettingServicosGerenteLimpezaPredial
    serializer_class = SettingServicosGerenteLimpezaPredialSerializer
    permission_type = 'limpeza_predial'
    permission_code = '410: Pode editar o recebimento de notificações gerais'
    search_fields = ('id', 'id_random', 'Gerente', 'NotificationsServicosAtrasados', 'NotificationsServicosProximos',
            'NotificationsServicosEmAndamento', 'NotificationsServicosCancelados',
            'NotificationsServicosAgendados', 'NotificationReportProductivity',
            'NotificationReportServicosAtrasados', 'NotificationReportServicosProximos',
            'NotificationReportServicosEmAndamento','NotificationReportServicosCancelados',)
    empresa_filter_paths = (
        'Gerente__empresasecundaria__empresaprimaria__id_random',
        'Gerente__empresasecundaria__id_random',
    )
    extra_filters = {
        'Gerente__empresasecundaria__setor__setor__in': ['Jardinagem'],
        'Gerente__status': 'Mobilizado',
    }
    forbidden_message="Você não tem permissão para visualziar permissões de usuários"