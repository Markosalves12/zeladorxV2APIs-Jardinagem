from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from catalogo_de_servicos.api.serializers_jardinagem import CatalogodeServicoJardinagemSerializer
from catalogo_de_servicos.models_jardinagem import CatalogodeServicoJardinagem
from utils.views import (GenericDetailView, GenericUpdateView, GenericAlterStatusView, GenericFilteredListView,
                         GenericCreateView, GenericIfDeleteView, GenericFilteredListViewFromForms, GenericDeleteView)
from empresasecundario.utils import define_empresas
from empresasecundario.models import EmpresaSecundaria


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateCatalogoServicosJardinagem(request):
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
                "setor__setor__in": ['Jardinagem'],
                "status__in": ['Mobilizado']
            },
            "error_message": "A empresa secundaria selecionada está desmobilizado ou fora do seu escopo de empresas."
        },
    ]

    return GenericCreateView(
        request=request,
        model_class=CatalogodeServicoJardinagem,
        serializer_class=CatalogodeServicoJardinagemSerializer,
        permission_type="jardinagem",
        permission_to_access=['260: Pode criar novos serviços ao catálogo'],
        forbidden_message="Você não tem permissão para criar servicos de jardinagem.",
        foreign_key_validations=foreign_key_validations,
        public_endpoint=False
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CatalogoServicosJardinagemDetail(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericDetailView(
        request=request,
        model=CatalogodeServicoJardinagem,
        serializer_class=CatalogodeServicoJardinagemSerializer,
        filters={"id_random": id_random},
        permission_type="jardinagem",
        permission_to_access=["262: Pode visualizar serviços do catálogo"],
        forbidden_message="Você não tem permissão para visualizar este serviço do catálogo.",
        access_filters={  # valida o escopo do objeto
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids
        },
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def CatalogoServicosJardinagemUpdate(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericUpdateView(
        request=request,
        model=CatalogodeServicoJardinagem,
        serializer_class=CatalogodeServicoJardinagemSerializer,
        filters={"id_random": id_random},
        permission_type="jardinagem",
        permission_to_access=["261: Pode editar serviços do catálogo"],
        forbidden_message="Você não tem permissão para editar este serviço do catálogo.",
        not_found_message="Serviço de jardinagem não encontrado.",
        access_filters={  # valida o escopo do objeto
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids
        },
        public_endpoint=False
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def CatalogoServicosJardinagemAlterStatus(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericAlterStatusView(
        request=request,
        model=CatalogodeServicoJardinagem,
        filters={'id_random': id_random},
        permission_type='jardinagem',
        desmobilize_permission='264: Pode desmobilizar serviços do catálogo',
        rehabilitate_permission='265: Pode reabilitar serviços do catálogo',
        not_found_message='Serviço de jardinagem não encontrado.',
        success_message='Status do serviço de jardinagem atualizado com sucesso.',
        access_filters={  # valida o escopo do objeto
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids
        },
        public_endpoint=False
    )



# Headers: Authorization: Token <token>
class ListCatalogodeServicoJardinagem(GenericFilteredListView):
    model_class = CatalogodeServicoJardinagem
    serializer_class = CatalogodeServicoJardinagemSerializer
    permission_type = 'jardinagem'
    permission_code = '262: Pode visualizar serviços do catálogo'
    search_fields = ('id', 'id_random', 'nome', 'EmpresaSecundaria', 'status', )
    empresa_filter_paths = (
        "EmpresaSecundaria__empresaprimaria__id_random",
        "EmpresaSecundaria__id_random"
    )
    forbidden_message="Você não tem permissão para visualizar catalogo de serviço de jardinagem."


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def IfDeleteServicoCatalogoJardinagem(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericIfDeleteView(
        request,
        model=CatalogodeServicoJardinagem,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['263: Pode excluir serviços do catálogo'],
        access_filters={
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids
        },
        forbidden_message="Você não tem permissão para excluir este serviço do catálogo."
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteServicoCatalogoJardinagem(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericDeleteView(
        request,
        model=CatalogodeServicoJardinagem,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['263: Pode excluir serviços do catálogo'],
        access_filters={
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids
        },
        forbidden_message="Você não tem permissão para excluir este serviço do catálogo."
    )

class ListCatalogodeServicoJardinagemFromForms(GenericFilteredListViewFromForms):
    model_class = CatalogodeServicoJardinagem
    serializer_class = CatalogodeServicoJardinagemSerializer
    search_fields = ('id', 'id_random', 'nome', 'EmpresaSecundaria', 'status')
    empresa_filter_paths = (
        "EmpresaSecundaria__empresaprimaria__id_random",
        "EmpresaSecundaria__id_random",
    )
    forbidden_message="Você não tem permissão para visualizar catalogo de serviço de jardinagem."

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            EmpresaSecundaria__status__in=['Mobilizado'],
            status__in=['Mobilizado']
        )