from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from gerente.api.serializers import GerenteSerializer
from gerente.models import Gerente
from utils.views import (GenericDetailView, GenericAlterStatusView,
                         GenericFilteredListView, GenericIfDeleteView,
                         GenericUpdateView, GenericCreateView, GenericDeleteView)
from empresasecundario.utils import define_empresas
from empresasecundario.models import EmpresaSecundaria

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateGerenteLimpezaPredial(request):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']

    foreign_key_validations = [
        {
            "coluna": "empresasecundaria",
            "model": EmpresaSecundaria,
            "filters": {
                "empresaprimaria__id_random__in": empresas_primarias_ids,
                "setor__setor": 'Limpeza predial',
                "status__in": ['Mobilizado']
            },
            "error_message": "A empresa secundaria selecionada está desmobilizado ou fora do seu escopo de empresas."
        },
    ]

    return GenericCreateView(
        request=request,
        model_class=Gerente,
        serializer_class=GerenteSerializer,
        permission_type="limpeza_predial",
        permission_to_access=['280: Pode criar novos colaboradores'],
        forbidden_message="Você não tem permissão para criar novos colaboradores.",
        foreign_key_validations=foreign_key_validations,
        public_endpoint=False
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GerenteLimpezaPredialDetail(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericDetailView(
        request=request,
        model=Gerente,
        serializer_class=GerenteSerializer,
        filters={"id_random": id_random},
        permission_type="limpeza_predial",
        permission_to_access=["282: Pode visualizar colaboradores"],
        forbidden_message="Você não tem permissão para visualizar colaboradores de limpeza predial.",
        access_filters={
            "empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "empresasecundaria__id_random__in": empresas_secundarias_ids,
            "empresasecundaria__setor__setor": 'Limpeza predial'
        }
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def GerenteLimpezaPredialUpdate(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericUpdateView(
        request=request,
        model=Gerente,
        serializer_class=GerenteSerializer,
        filters={"id_random": id_random},
        permission_type="jardinagem",
        permission_to_access=["281: Pode editar colaboradores"],
        forbidden_message="Você não tem permissão para editar colaboradores de jardinagem.",
        not_found_message="Colaborador de jardinagem não encontrado.",
        access_filters={
            "empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "empresasecundaria__id_random__in": empresas_secundarias_ids,
            "empresasecundaria__setor__setor": 'Limpeza predial'
        },
        public_endpoint=False,
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def GerenteLimpezaPredialAlterStatus(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericAlterStatusView(
        request=request,
        model=Gerente,
        filters={'id_random': id_random},
        permission_type='limpeza_predial',
        desmobilize_permission='284: Pode desmobilizar colaboradores',
        rehabilitate_permission='285: Pode reabilitar colaboradores',
        not_found_message='Colaborador de limpeza predial não encontrado.',
        success_message='Status do colaborador atualizado com sucesso.',
        access_filters={
            "empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "empresasecundaria__id_random__in": empresas_secundarias_ids,
            "empresasecundaria__setor__setor": 'Limpeza predial'
        },
        public_endpoint=False
    )


# Headers: Authorization: Token <token>
class ListGerenteLimpezaPredial(GenericFilteredListView):
    model_class = Gerente
    serializer_class = GerenteSerializer
    permission_type = 'limpeza_predial'
    permission_code = '282: Pode visualizar colaboradores'
    search_fields = ('id', 'username', 'email', 'empresasecundaria', 'is_superuser', 'status')
    empresa_filter_paths = (
        'empresasecundaria__empresaprimaria__id_random',
        'empresasecundaria__id_random',
    )
    forbidden_message = "Você não tem permissão para visualizar colaboradores de limpeza predial."

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(empresasecundaria__setor__setor='Limpeza predial')



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def IfDeleteGerenteLimpezaPredial(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericIfDeleteView(
        request,
        model=Gerente,
        id_random=id_random,
        permission_type='limpeza_predial',
        permission_to_access=['283: Pode excluir colaboradores'],
        access_filters={
            "empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "empresasecundaria__id_random__in": empresas_secundarias_ids,
            "empresasecundaria__setor__setor": 'Limpeza predial'
        }
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteGerenteLimpezaPredial(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericDeleteView(
        request,
        model=Gerente,
        id_random=id_random,
        permission_type='limpeza_predial',
        permission_to_access=['283: Pode excluir colaboradores'],
        access_filters={
            "empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "empresasecundaria__id_random__in": empresas_secundarias_ids,
            "empresasecundaria__setor__setor": 'Limpeza predial'
        }
    )


class ListGerenteLimpezaPredialFromForms(GenericFilteredListView):
    model_class = Gerente
    serializer_class = GerenteSerializer
    permission_type = 'limpeza_predial'
    permission_code = '282: Pode visualizar colaboradores'
    search_fields = ('id', 'username', 'email', 'empresasecundaria', 'is_superuser', 'status')
    empresa_filter_paths = (
        'empresasecundaria__empresaprimaria__id_random',
        'empresasecundaria__id_random',
    )
    forbidden_message = "Você não tem permissão para visualizar colaboradores de limpeza predial."

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            empresasecundaria__status__in=['Mobilizado'],
            empresasecundaria__setor__setor__in=['Limpeza predial'],
            status__in=['Mobilizado']
        )