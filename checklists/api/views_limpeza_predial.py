from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from checklists.api.serializers_limpeza_predial import CheckListLimpezaPredialSerializer
from checklists.models import CheckListLimpezaPredial
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas


from utils.views import GenericFilteredListView

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ListCheckListDetailsLimpezaPredial(request, id_random):
    user_id_random = request.user.id_random

    # Permissão
    if not validate_permissions(
        request=request,
        userid=user_id_random,
        permission_type='limpeza_predial',
        permission_to_access=['402: Pode visualizar checklists']
    ):
        return Response(
            {"detail": "Você não tem permissão para visualizar checklists de serviços de limpeza predial"},
            status=status.HTTP_403_FORBIDDEN
        )

    empresas = define_empresas(request=request, userid=user_id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    # Queryset
    checklists = CheckListLimpezaPredial.objects.filter(
        servico_agendado__Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
        servico_agendado__Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
        servico_agendado__id_random=id_random
    ).distinct()

    serializer = CheckListLimpezaPredialSerializer(checklists, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)




# Response: https://gist.github.com/mitchtabian/ae03573737067c9269701ea662460205
# Url: https://<your-domain>/api/blog/list
# Headers: Authorization: Token <token>
class ListCheckListLimpezaPredial(GenericFilteredListView):
    model_class = CheckListLimpezaPredial
    serializer_class = CheckListLimpezaPredialSerializer
    permission_type = 'limpeza_predial'
    permission_code = '402: Pode visualizar checklists'
    search_fields = ('id_random', 'servico_agendado', 'descricao', 'foto_comprovacao', 'status')
    empresa_filter_paths = (
        "servico_agendado__Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random",
        "servico_agendado__Areas__localidade__unidade__empresasecundaria__id_random"
    )
