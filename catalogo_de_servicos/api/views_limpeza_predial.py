from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from catalogo_de_servicos.api.serializers_limpeza_predial import CatalogodeServicoLimpezaPredialSerializer
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial
from utils.views import (GenericDetailView, GenericUpdateView, GenericAlterStatusView, GenericFilteredListView,
                         GenericCreateView, GenericIfDeleteView, GenericDeleteView)
from empresasecundario.utils import define_empresas
from empresasecundario.models import EmpresaSecundaria


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateCatalogoServicosLimpezaPredial(request):
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
                "setor__setor__in": ['Limpeza predial'],
                "status__in": ['Mobilizado']
            },
            "error_message": "A empresa secundaria selecionada está desmobilizado ou fora do seu escopo de empresas."
        },
    ]

    return GenericCreateView(
        request=request,
        model_class=CatalogodeServicoLimpezaPredial,
        serializer_class=CatalogodeServicoLimpezaPredialSerializer,
        permission_type="limpeza_predial",
        permission_to_access=['260: Pode criar novos serviços ao catálogo'],
        forbidden_message="Você não tem permissão para criar servicos de limpeza predial.",
        foreign_key_validations=foreign_key_validations,
        public_endpoint=False
    )



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CatalogoServicosLimpezaPredialDetail(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericDetailView(
        request=request,
        model=CatalogodeServicoLimpezaPredial,
        serializer_class=CatalogodeServicoLimpezaPredialSerializer,
        filters={"id_random": id_random},
        permission_type="limpeza_predial",
        permission_to_access=["262: Pode visualizar serviços do catálogo"],
        forbidden_message="Você não tem permissão para visualizar este serviço de limpeza predial.",
        access_filters={  # valida o escopo do objeto
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids
        },
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def CatalogoServicosLimpezaPredialUpdate(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericUpdateView(
        request=request,
        model=CatalogodeServicoLimpezaPredial,
        serializer_class=CatalogodeServicoLimpezaPredialSerializer,
        filters={"id_random": id_random},
        permission_type="limpeza_predial",
        permission_to_access=["261: Pode editar serviços do catálogo"],
        forbidden_message="Você não tem permissão para editar este serviço do catálogo.",
        not_found_message="Serviço de limpeza predial não encontrado.",
        access_filters={  # valida o escopo do objeto
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids
        },
        public_endpoint=False
    )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def CatalogoServicosLimpezaPredialAlterStatus(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericAlterStatusView(
        request=request,
        model=CatalogodeServicoLimpezaPredial,
        filters={'id_random': id_random},
        permission_type='limpeza_predial',
        desmobilize_permission='264: Pode desmobilizar serviços do catálogo',
        rehabilitate_permission='265: Pode reabilitar serviços do catálogo',
        not_found_message='Serviço de limpeza predial não encontrado.',
        success_message='Status do serviço de limpeza predial atualizado com sucesso.',
        access_filters={  # valida o escopo do objeto
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids
        },
        public_endpoint=False
    )



# Headers: Authorization: Token <token>
class ListCatalogodeServicoLimpezaPredial(GenericFilteredListView):
    model_class = CatalogodeServicoLimpezaPredial
    serializer_class = CatalogodeServicoLimpezaPredialSerializer
    permission_type = 'limpeza_predial'
    permission_code = '262: Pode visualizar serviços do catálogo'
    search_fields = ('id', 'id_random', 'nome', 'EmpresaSecundaria', 'status')
    empresa_filter_paths = (
        "EmpresaSecundaria__empresaprimaria__id_random",
        "EmpresaSecundaria__id_random"
    )
    forbidden_messag="Você não tem permissão para visualizar catalogo de serviço de limpeza predial.",


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def IfDeleteServicoCatalogoLimpezaPredial(request, id_random):

    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericIfDeleteView(
        request,
        model=CatalogodeServicoLimpezaPredial,
        id_random=id_random,
        permission_type='limpeza_predial',
        permission_to_access=['263: Pode excluir serviços do catálogo'],
        access_filters={
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids
        }
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteServicoCatalogoLimpezaPredial(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericDeleteView(
        request,
        model=CatalogodeServicoLimpezaPredial,
        id_random=id_random,
        permission_type='limpeza_predial',
        permission_to_access=['263: Pode excluir serviços do catálogo'],
        access_filters={
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids
        }
    )



class ListCatalogodeServicoLimpezaPredialFromForms(GenericFilteredListView):
    model_class = CatalogodeServicoLimpezaPredial
    serializer_class = CatalogodeServicoLimpezaPredialSerializer
    permission_type = 'limpeza_predial'
    permission_code = '262: Pode visualizar serviços do catálogo'
    search_fields = ('id', 'id_random', 'nome', 'EmpresaSecundaria', 'status')
    empresa_filter_paths = (
        "EmpresaSecundaria__empresaprimaria__id_random",
        "EmpresaSecundaria__id_random"
    )
    forbidden_messag="Você não tem permissão para visualizar catalogo de serviço de limpeza predial."

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            EmpresaSecundaria__status__in=['Mobilizado'],
            status__in=['Mobilizado']
        )