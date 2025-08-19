from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from empresasecundario.api.serializers import EmpresaSecundariaSerializer
from empresasecundario.models import EmpresaSecundaria
from utils.views import (GenericDetailView, GenericUpdateView, GenericAlterStatusView,
                         GenericFilteredListView, GenericCreateView, GenericIfDeleteView,
                         GenericDeleteView)
from zeladorx.models import TypeZeladoria
from empresasecundario.utils import define_empresas
from empresaprimaria.models import EmpresaPrimaria

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateEmpresaSecundariaLimpezaPredial(request):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    setores = empresas['setores']['setores_primaria']

    foreign_key_validations = [
        {
            "coluna": "setor",
            "model": TypeZeladoria,
            "filters": {
                "id__in": setores
            },
            "error_message": "Macro serviço não habilitado para sua organização"
        },
        {
            "coluna": "empresaprimaria",
            "model": EmpresaPrimaria,
            "filters": {
                "id_random__in": empresas_primarias_ids,
                "status__in": ['Mobilizado']
            },
            "error_message": "Ecossistema fora do range"
        },
    ]

    return GenericCreateView(
        request=request,
        model_class=EmpresaSecundaria,
        serializer_class=EmpresaSecundariaSerializer,
        permission_type="especials",
        permission_to_access=['270: Pode criar novas empresas'],
        forbidden_message="Você não tem permissão para criar empresas secundarias.",
        foreign_key_validations=foreign_key_validations,
        public_endpoint=False
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def EmpresaSecundariaLimpezaPredialDetail(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']

    return GenericDetailView(
        request=request,
        model=EmpresaSecundaria,
        serializer_class=EmpresaSecundariaSerializer,
        filters={"id_random": id_random},
        permission_type="especials",
        permission_to_access=["272: Pode visualizar empresas"],
        forbidden_message="Você não tem permissão para visualizar empresas secundarias.",
        access_filters={  # valida o escopo do objeto
            "empresaprimaria__id_random__in": empresas_primarias_ids,
            "setor__setor__in": ['Limpeza predial']
        },
    )




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def EmpresaSecundariaLimpezaPredialUpdate(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']

    return GenericUpdateView(
        request=request,
        model=EmpresaSecundaria,
        serializer_class=EmpresaSecundariaSerializer,
        filters={"id_random": id_random},
        permission_type="especials",
        permission_to_access=["271: Pode editar empresas"],
        forbidden_message="Você não tem permissão para editar esta empresa.",
        not_found_message="Empresa de limpeza predial não encontrada.",
        access_filters={  # valida o escopo do objeto
            "empresaprimaria__id_random__in": empresas_primarias_ids,
            "setor__setor__in": ['Limpeza predial']
        },
        public_endpoint=False,
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def EmpresaSecundariaLimpezaPredialAlterStatus(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']

    return GenericAlterStatusView(
        request=request,
        model=EmpresaSecundaria,
        filters={'id_random': id_random},
        permission_type='especials',
        desmobilize_permission='274: Pode desmobilizar empresas',
        rehabilitate_permission='275: Pode reabilitar empresas',
        not_found_message='Empresa de limpeza predial não encontrada.',
        success_message='Status da empresa atualizado com sucesso.',
        access_filters={  # valida o escopo do objeto
            "empresaprimaria__id_random__in": empresas_primarias_ids,
            "setor__setor__in": ['Limpeza predial']
        },
        public_endpoint=False
    )



# Headers: Authorization: Token <token>
class ListEmpresaSecundariaLimpezaPredial(GenericFilteredListView):
    model_class = EmpresaSecundaria
    serializer_class = EmpresaSecundariaSerializer
    permission_type = 'especials'
    permission_code = '272: Pode visualizar empresas'
    search_fields = ('id', 'id_random', 'nome', 'setor', 'empresaprimaria', 'status')
    empresa_filter_paths = (
        'empresaprimaria__id_random',
    )
    forbidden_message = "Você não permissão para visualizar empresas de limpeza predial."

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(setor__setor__in=['Limpeza predial'])


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def IfDeleteEmpresaSecundariaLimpezaPredial(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]

    return GenericIfDeleteView(
        request,
        model=EmpresaSecundaria,
        id_random=id_random,
        permission_type='especials',
        permission_to_access=['273: Pode excluir empresas'],
        access_filters={
            "empresaprimaria__id_random__in": empresas_primarias_ids,
            "setor__setor__in": ['Limpeza predial']
        },
        forbidden_message="Você não tem permissão para excluir esta empresa."
    )



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteEmpresaSecundariaLimpezaPredial(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]

    return GenericDeleteView(
        request,
        model=EmpresaSecundaria,
        id_random=id_random,
        permission_type='especials',
        permission_to_access=['273: Pode excluir empresas'],
        access_filters={
            "empresaprimaria__id_random__in": empresas_primarias_ids,
            "setor__setor__in": ['Limpeza predial']
        },
        forbidden_message="Você não tem permissão para excluir esta empresa."
    )




class ListEmpresaSecundariaLimpezaPredialFromForms(GenericFilteredListView):
    model_class = EmpresaSecundaria
    serializer_class = EmpresaSecundariaSerializer
    permission_type = 'especials'
    permission_code = '272: Pode visualizar empresas'
    search_fields = ('id', 'id_random', 'nome', 'setor', 'empresaprimaria', 'status')
    empresa_filter_paths = (
        'empresaprimaria__id_random',
    )
    forbidden_message = "Você não permissão para visualizar empresas de limpeza predial."

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            setor__setor__in=['Limpeza predial'],
            empresaprimaria__status__in=['Mobilizado'],
            status__in=['Mobilizado']
        )
