from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from empresasecundario.api.serializers import EmpresaSecundariaSerializer
from empresasecundario.models import EmpresaSecundaria
from utils.views import GenericDetailView, GenericUpdateView, GenericAlterStatusView, GenericFilteredListView

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def EmpresaSecundariaLimpezaPredialDetail(request, id_random):
    return GenericDetailView(
        request=request,
        model=EmpresaSecundaria,
        serializer_class=EmpresaSecundariaSerializer,
        filters={"id_random": id_random},
        permission_type="especials",
        permission_to_access=["272: Pode visualizar empresas"],
        forbidden_message="Você não tem permissão para visualizar empresas secundarias."
    )




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def EmpresaSecundariaLimpezaPredialUpdate(request, id_random):
    return GenericUpdateView(
        request=request,
        model=EmpresaSecundaria,
        serializer_class=EmpresaSecundariaSerializer,
        filters={"id_random": id_random},
        permission_type="especials",
        permission_to_access=["271: Pode editar empresas"],
        forbidden_message="Você não tem permissão para editar esta empresa.",
        not_found_message="Empresa de limpeza predial não encontrada."
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def EmpresaSecundariaLimpezaPredialAlterStatus(request, id_random):
    return GenericAlterStatusView(
        request=request,
        model=EmpresaSecundaria,
        filters={'id_random': id_random},
        permission_type='especials',
        desmobilize_permission='274: Pode desmobilizar empresas',
        rehabilitate_permission='275: Pode reabilitar empresas',
        not_found_message='Empresa de limpeza predial não encontrada.',
        success_message='Status da empresa atualizado com sucesso.'
    )




# Response: https://gist.github.com/mitchtabian/ae03573737067c9269701ea662460205
# Url: https://<your-domain>/api/blog/list
# Headers: Authorization: Token <token>
class ListEmpresaSecundariaLimpezaPredial(GenericFilteredListView):
    model_class = EmpresaSecundaria
    serializer_class = EmpresaSecundariaSerializer
    permission_type = 'especials'
    permission_code = '272: Pode visualizar empresas'
    search_fields = ('id_random', 'nome', 'setor', 'empresaprimaria', 'status')
    empresa_filter_paths = (
        'empresaprimaria__id_random',
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(setor__setor__in=['Limpeza predial'])
