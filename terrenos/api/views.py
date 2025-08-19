from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from terrenos.api.serializers import TerrenoSerializer
from terrenos.models import Terreno
from utils.views import (GenericDetailView, GenericUpdateView, GenericFilteredListView, GenericCreateView,
                         GenericAlterStatusView, GenericIfDeleteView, GenericDeleteView)
from empresasecundario.utils import define_empresas
from empresasecundario.models import EmpresaSecundaria


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateTerreno(request):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    foreign_key_validations = [
        {
            "coluna": "EmpresaSecundaria",
            "model": EmpresaSecundaria,
            "filters": {
                "empresaprimaria__id_random__in": empresas_primarias_ids,
                "id_random__in": empresas_secundarias_ids,
                "empresaprimaria__status__in": ['Mobilizado'],
                "status__in": ['Mobilizado'],
                "setor__setor__in": ["Jardinagem"]
            },
            "error_message": "Empresa secundaria esta desmobilizada ou não pertence a sua organização."
        },
    ]

    return GenericCreateView(
        request=request,
        model_class=Terreno,
        serializer_class=TerrenoSerializer,
        permission_type="jardinagem",
        permission_to_access=['330: Pode criar novos terrenos'],
        forbidden_message="Você não tem permissão para criar terrenos.",
        foreign_key_validations=foreign_key_validations,
        public_endpoint=False
    )



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def TerrenoDetail(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericDetailView(
        request=request,
        model=Terreno,
        serializer_class=TerrenoSerializer,
        filters={"id_random": id_random},
        permission_type="jardinagem",
        permission_to_access=['332: Pode visualizar terrenos'],
        forbidden_message="Você não tem permissão para visualizar terrenos.",
        access_filters={
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids
        }
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def TerrenoUpdate(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericUpdateView(
        request=request,
        model=Terreno,
        serializer_class=TerrenoSerializer,
        filters={"id_random": id_random},
        permission_type="jardinagem",
        permission_to_access=['331: Pode editar terrenos'],
        forbidden_message="Você não tem permissão para editar terrenos.",
        not_found_message="Localidade de jardinagem não encontrada.",
        access_filters={
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids
        },
        public_endpoint=False,
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def TerrenoAlterStatus(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericAlterStatusView(
        request=request,
        model=Terreno,
        filters={"id_random": id_random},
        permission_type="jardinagem",
        desmobilize_permission='334: Pode desmobilizar terrenos',
        rehabilitate_permission='335: Pode reabilitar terrenos',
        not_found_message="Terreno não encontrada.",
        success_message="Status do terreno atualizado com sucesso.",
        access_filters={
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids
        },
        public_endpoint=False
    )


class ListTerrenos(GenericFilteredListView):
    model_class = Terreno
    serializer_class = TerrenoSerializer
    permission_type = 'jardinagem'
    permission_code = '332: Pode visualizar terrenos'
    search_fields = ('id', 'id_random', 'nome', 'EmpresaSecundaria', 'status', )
    empresa_filter_paths = (
        "EmpresaSecundaria__empresaprimaria__id_random",
        "EmpresaSecundaria__id_random"
    )
    forbidden_message="Você não pode visualizar terrenos"




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def IfDeleteTerreno(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericIfDeleteView(
        request,
        model=Terreno,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['333: Pode excluir terrenos'],
        access_filters={
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids
        },
        forbidden_message="Você não tem permissão para excluir esse terreno."
    )



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteTerreno(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericDeleteView(
        request,
        model=Terreno,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['333: Pode excluir terrenos'],
        access_filters={
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids
        },
        forbidden_message="Você não tem permissão para excluir esse terreno."
    )



class ListTerrenosFromForms(GenericFilteredListView):
    model_class = Terreno
    serializer_class = TerrenoSerializer
    permission_type = 'jardinagem'
    permission_code = '332: Pode visualizar terrenos'
    search_fields = ('id', 'id_random', 'nome', 'EmpresaSecundaria', 'status', )
    empresa_filter_paths = (
        "EmpresaSecundaria__empresaprimaria__id_random",
        "EmpresaSecundaria__id_random"
    )
    forbidden_message="Você não pode visualizar terrenos"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            EmpresaSecundaria__status__in=['Mobilizado'],
            status__in=['Mobilizado']
        )
