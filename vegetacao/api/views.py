from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from vegetacao.api.serializers import CatalogoVegetacaoSerializer
from vegetacao.models import CatalogoVegetacao
from empresasecundario.utils import define_empresas
from empresasecundario.models import EmpresaSecundaria
from utils.views import (GenericCreateView, GenericDetailView, GenericUpdateView, GenericAlterStatusView,
                         GenericFilteredListView, GenericIfDeleteView, GenericDeleteView)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateVegetacao(request):
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
            "error_message": "Empresa secundaria desmobilizada ou não pertence a sua organização"
        },
    ]

    return GenericCreateView(
        request=request,
        model_class=CatalogoVegetacao,
        serializer_class=CatalogoVegetacaoSerializer,
        permission_type="jardinagem",
        permission_to_access=['350: Pode criar novas vegetações'],
        forbidden_message="Você não tem permissão para criar vegetações.",
        foreign_key_validations=foreign_key_validations,
        public_endpoint=False
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def VegetacaoDetail(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericDetailView(
        request=request,
        model=CatalogoVegetacao,
        serializer_class=CatalogoVegetacaoSerializer,
        filters={"id_random": id_random},
        permission_type="jardinagem",
        permission_to_access=['352: Pode visualizar vegetações'],
        forbidden_message="Você não tem permissão para visualizar vegetações.",
        access_filters={
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids,
        }
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def VegetacaoUpdate(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericUpdateView(
        request=request,
        model=CatalogoVegetacao,
        serializer_class=CatalogoVegetacaoSerializer,
        filters={"id_random": id_random},
        permission_type="jardinagem",
        permission_to_access=['351: Pode editar vegetações'],
        forbidden_message="Você não tem permissão para editar vegetações.",
        not_found_message="Vegetação não encontrada.",
        access_filters={
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids,
        },
        public_endpoint=False,
    )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def VegetacaoAlterStatus(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericAlterStatusView(
        request=request,
        model=CatalogoVegetacao,
        filters={"id_random": id_random},
        permission_type="jardinagem",
        desmobilize_permission='354: Pode desmobilizar vegetações',
        rehabilitate_permission='355: Pode reabilitar vegetações',
        not_found_message="Vegetação não encontrada.",
        success_message="Status da vegetação atualizado com sucesso.",
        access_filters={
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids,
        },
        public_endpoint=False
    )



# Response: https://gist.github.com/mitchtabian/ae03573737067c9269701ea662460205
# Headers: Authorization: Token <token>
class ListCatalogoVegetacao(GenericFilteredListView):
    model_class = CatalogoVegetacao
    serializer_class = CatalogoVegetacaoSerializer
    permission_type = 'jardinagem'
    permission_code = '352: Pode visualizar vegetações'
    search_fields = ('id', 'id_random', 'nome', 'EmpresaSecundaria', 'status')
    empresa_filter_paths = (
        "EmpresaSecundaria__empresaprimaria__id_random",
        "EmpresaSecundaria__id_random",
    )
    forbidden_message = "Você não tem permissão para visualizar vegetações."



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def IfDeleteCatalogoVegetacao(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericIfDeleteView(
        request,
        model=CatalogoVegetacao,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['353: Pode excluir vegetações'],
        access_filters={
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids
        },
        forbidden_message="Você não tem permissão para excluir esta vegetacao."
    )



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteCatalogoVegetacao(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericDeleteView(
        request,
        model=CatalogoVegetacao,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['353: Pode excluir vegetações'],
        access_filters={
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids
        },
        forbidden_message="Você não tem permissão para excluir esta vegetacao."
    )




class ListCatalogoVegetacaoFromForms(GenericFilteredListView):
    model_class = CatalogoVegetacao
    serializer_class = CatalogoVegetacaoSerializer
    permission_type = 'jardinagem'
    permission_code = '352: Pode visualizar vegetações'
    search_fields = ('id', 'id_random', 'nome', 'EmpresaSecundaria', 'status')
    empresa_filter_paths = (
        "EmpresaSecundaria__empresaprimaria__id_random",
        "EmpresaSecundaria__id_random",
    )
    forbidden_message = "Você não tem permissão para visualizar vegetações."


    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            EmpresaSecundaria__status__in=['Mobilizado'],
            status__in=['Mobilizado']
        )