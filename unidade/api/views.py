from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from unidade.models import Unidade
from empresasecundario.utils import define_empresas
from utils.views import (GenericDetailView, GenericUpdateView, GenericCreateView, GenericAlterStatusView,
                         GenericFilteredListView, GenericIfDeleteView, GenericDeleteView)
from empresasecundario.models import EmpresaSecundaria
from unidade.api.serializers import UnidadeSerializer
from empresaprimaria.models import EmpresaPrimaria
from rest_framework.response import Response
from rest_framework import status
from copy import deepcopy

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateUnidade(request):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']
    setores = empresas['setores']

    # Validação de limite de unidades permitidas
    try:
        empresa_associada = EmpresaPrimaria.objects.get(id_random=empresas_primarias_ids[0])
    except EmpresaPrimaria.DoesNotExist:
        return Response(
            {"detail": "Empresa primária não encontrada."},
            status=status.HTTP_400_BAD_REQUEST
        )

    n_unidades_criadas = Unidade.objects.filter(
        empresasecundaria__empresaprimaria=empresa_associada
    ).count()

    if n_unidades_criadas > empresa_associada.N_unidades:
        return Response(
            {
                "detail": f"A empresa '{empresa_associada.nome}' já atingiu o limite de unidades contratadas ({empresa_associada.N_unidades})."
            },
            status=status.HTTP_403_FORBIDDEN
        )

        # Cópia mutável dos dados recebidos
    data = deepcopy(request.data)

    # Regras de remoção de campos proibidos
    if not (setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']):
        data.pop("linkmapajardinagem", None)

    if not (setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']):
        data.pop("linkmapalimpezapredial", None)


    foreign_key_validations = [
        {
            "coluna": "empresasecundaria",
            "model": EmpresaSecundaria,
            "filters": {
                "empresaprimaria__id_random__in": empresas_primarias_ids,
                "id_random__in": empresas_secundarias_ids,
                "status__in": ['Mobilizado'],
            },
            "error_message": "Empresa secundaria desmobilizada ou não pertence a sua organização."
        },
    ]



    return GenericCreateView(
        request=request,
        model_class=Unidade,
        serializer_class=UnidadeSerializer,
        permission_type="especials",
        permission_to_access=['340: Pode criar novas unidades'],
        forbidden_message="Você não tem permissão para criar novas unidades.",
        foreign_key_validations=foreign_key_validations,
        public_endpoint=False
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UnidadeDetail(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']
    unidades_secundarias_ids = empresas['unidades_secundarias_ids']
    setores = empresas['setores']


    # Serializador dinâmico para esconder campos
    class UnidadeDynamicSerializer(UnidadeSerializer):
        class Meta(UnidadeSerializer.Meta):
            fields = list(UnidadeSerializer.Meta.fields)  # copia os campos originais

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # regra jardinagem
            if not (setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']):
                self.fields.pop("linkmapajardinagem", None)

            # regra limpeza
            if not (setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']):
                self.fields.pop("linkmapalimpezapredial", None)


    return GenericDetailView(
        request=request,
        model=Unidade,
        serializer_class=UnidadeDynamicSerializer,
        filters={"id_random": id_random},
        permission_type="especials",
        permission_to_access=["342: Pode visualizar unidades"],
        forbidden_message="Você não tem permissão para visualizar esta unidade.",
        access_filters={
            "empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "empresasecundaria__id_random__in": empresas_secundarias_ids,
            "id_random__in": unidades_secundarias_ids
        }
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def UnidadeUpdate(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']
    unidades_secundarias_ids = empresas['unidades_secundarias_ids']
    setores = empresas['setores']

    # Cópia dos dados recebidos para aplicar as regras
    data = deepcopy(request.data)

    # Regras de exclusão de campos conforme permissões
    if not (setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']):
        data.pop("linkmapajardinagem", None)

    if not (setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']):
        data.pop("linkmapalimpezapredial", None)

    return GenericUpdateView(
        request=request,
        model=Unidade,
        serializer_class=UnidadeSerializer,
        filters={"id_random": id_random},
        permission_type="especials",
        permission_to_access=["341: Pode editar unidades"],
        forbidden_message="Você não tem permissão para editar esta unidade.",
        not_found_message="Unidade não encontrada.",
        access_filters={
            "empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "empresasecundaria__id_random__in": empresas_secundarias_ids,
            "id_random__in": unidades_secundarias_ids
        },
        public_endpoint=False
    )



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def UnidadeAlterStatus(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']
    unidades_secundarias_ids = empresas['unidades_secundarias_ids']

    return GenericAlterStatusView(
        request=request,
        model=Unidade,
        filters={"id_random": id_random},
        permission_type="especials",
        desmobilize_permission='344: Pode desmobilizar unidades',
        rehabilitate_permission='345: Pode reabilitar unidades',
        not_found_message="Unidade não encontrada.",
        success_message="Status da unidade atualizado com sucesso.",
        access_filters={
            "empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "empresasecundaria__id_random__in": empresas_secundarias_ids,
            "id_random__in": unidades_secundarias_ids
        },
        public_endpoint=False
    )



# Headers: Authorization: Token <token>
class ListUnidade(GenericFilteredListView):
    model_class = Unidade
    serializer_class = UnidadeSerializer
    permission_type = 'especials'
    permission_code = '342: Pode visualizar unidades'
    search_fields = (
        'id', 'id_random', 'nome',
        'linkmapajardinagem', 'linkmapalimpezapredial',
        'empresasecundaria', 'status'
    )
    empresa_filter_paths = (
        "empresasecundaria__empresaprimaria__id_random",
        "empresasecundaria__id_random",
    )
    forbidden_message = "Você não pode visualizar unidades"

    def get_queryset(self):
        queryset = super().get_queryset()

        empresas = define_empresas(
            request=self.request,
            userid=self.request.user.id_random
        )
        unidades_secundarias_ids = empresas['unidades_secundarias_ids']

        return queryset.filter(id_random__in=unidades_secundarias_ids)

    def get_serializer_class(self):
        empresas = define_empresas(
            request=self.request,
            userid=self.request.user.id_random
        )
        setores = empresas['setores']

        class UnidadeDynamicSerializer(UnidadeSerializer):
            class Meta(UnidadeSerializer.Meta):
                fields = list(UnidadeSerializer.Meta.fields)

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                if not (setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']):
                    self.fields.pop("linkmapajardinagem", None)

                if not (setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']):
                    self.fields.pop("linkmapalimpezapredial", None)

        return UnidadeDynamicSerializer




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def IfDeleteUnidade(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']
    unidades_secundarias_ids = empresas['unidades_secundarias_ids']

    return GenericIfDeleteView(
        request,
        model=Unidade,
        id_random=id_random,
        permission_type='especials',
        permission_to_access=['343: Pode excluir unidades'],
        access_filters={
            "empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "empresasecundaria__id_random__in": empresas_secundarias_ids,
            "id_random__in": unidades_secundarias_ids
        },
        forbidden_message="Você não tem permissão para excluir esta unidade."
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteUnidade(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']
    unidades_secundarias_ids = empresas['unidades_secundarias_ids']

    return GenericDeleteView(
        request,
        model=Unidade,
        id_random=id_random,
        permission_type='especials',
        permission_to_access=['343: Pode excluir unidades'],
        access_filters={
            "empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "empresasecundaria__id_random__in": empresas_secundarias_ids,
            "id_random__in": unidades_secundarias_ids
        },
        forbidden_message="Você não tem permissão para excluir esta unidade."
    )


class ListUnidadeFromForms(GenericFilteredListView):
    model_class = Unidade
    serializer_class = UnidadeSerializer
    permission_type = 'especials'
    permission_code = '342: Pode visualizar unidades'
    search_fields = ('id', 'id_random', 'nome', 'linkmapajardinagem', 'linkmapalimnpezapredial',
                     'empresasecundaria', 'status')
    empresa_filter_paths = (
        "empresasecundaria__empresaprimaria__id_random",
        "empresasecundaria__id_random",
    )
    forbidden_message="Você não pode visualizar unidades"


    def get_queryset(self):
        queryset = super().get_queryset()

        # Agora sim: self.request está disponível
        empresas = define_empresas(
            request=self.request,
            userid=self.request.user.id_random
        )
        unidades_secundarias_ids = empresas['unidades_secundarias_ids']

        # Aplica o filtro
        return queryset.filter(
            id_random__in=unidades_secundarias_ids,
            empresasecundaria__status__in=['Mobilizado'],
            status__in=['Mobilizado']
        )