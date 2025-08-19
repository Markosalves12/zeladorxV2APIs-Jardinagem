from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from permissionscontrol.utils import validate_permissions
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import PermissionDenied
from empresasecundario.utils import define_empresas
from copy import deepcopy
from django.db import router
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin.utils import NestedObjects

def GenericDetailView(
    *,
    request,
    model,
    serializer_class,
    filters: dict,
    permission_type: str,
    permission_to_access: list,
    forbidden_message: str,
    access_filters: dict = None
):
    """
    View genérica para detalhamento de objetos com validação de escopo e permissão.
    """
    user_id_random = request.user.id_random

    # Verificação de permissão
    if not validate_permissions(
        request=request,
        userid=user_id_random,
        permission_type=permission_type,
        permission_to_access=permission_to_access
    ):
        return Response({"detail": forbidden_message}, status=status.HTTP_403_FORBIDDEN)

    # Busca principal (ex: id_random)
    instance = get_object_or_404(model, **filters)

    # Validação de escopo (ex: empresas permitidas)
    if access_filters:
        scoped_qs = model.objects.filter(**filters, **access_filters)
        if not scoped_qs.exists():
            return Response({"detail": forbidden_message}, status=status.HTTP_403_FORBIDDEN)

    serializer = serializer_class(instance, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)



def GenericUpdateView(
    *,
    request,
    model,
    serializer_class,
    filters: dict,
    permission_type: str,
    permission_to_access: list,
    forbidden_message: str,
    not_found_message: str,
    access_filters: dict = None,
    public_endpoint: bool = False
):
    user_id_random = request.user.id_random

    # Validação de permissão (se não for endpoint público)
    if not public_endpoint:
        has_permission = validate_permissions(
            request=request,
            userid=user_id_random,
            permission_type=permission_type,
            permission_to_access=permission_to_access
        )

        if not has_permission:
            return Response({"detail": forbidden_message}, status=status.HTTP_403_FORBIDDEN)

    # Busca do objeto
    try:
        instance = model.objects.get(**filters)
    except model.DoesNotExist:
        return Response({"detail": not_found_message}, status=status.HTTP_404_NOT_FOUND)

    # Verifica escopo do objeto (se não for endpoint público)
    if not public_endpoint and access_filters:
        scoped_qs = model.objects.filter(**filters, **access_filters)
        if not scoped_qs.exists():
            return Response({"detail": forbidden_message}, status=status.HTTP_403_FORBIDDEN)

    # Impede alteração do campo 'status'
    if 'status' in request.data:
        return Response(
            {"detail": "O campo 'status' não pode ser alterado por esta rota."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Atualização parcial do objeto
    serializer = serializer_class(instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "success": True,
                "message": f"{model.__name__} atualizado com sucesso.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    return Response(
        {
            "success": False,
            "message": "Erro de validação.",
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )



def GenericAlterStatusView(
    *,
    request,
    model,
    filters: dict,
    permission_type: str,
    desmobilize_permission: str,
    rehabilitate_permission: str,
    not_found_message: str = "Objeto não encontrado.",
    success_message: str = "Status atualizado com sucesso.",
    access_filters: dict = None,
    public_endpoint: bool = False,
):
    user_id = request.user.id_random

    try:
        instance = model.objects.get(**filters)
    except model.DoesNotExist:
        return Response(
            {"detail": not_found_message},
            status=status.HTTP_404_NOT_FOUND
        )

    # 🔒 Verificação de escopo (se o endpoint não for público)
    if access_filters and not public_endpoint:
        scoped_qs = model.objects.filter(**filters, **access_filters)
        if not scoped_qs.exists():
            return Response(
                {"detail": "Você não tem permissão para alterar este item."},
                status=status.HTTP_403_FORBIDDEN
            )

    allowed_fields = {"status"}
    received_fields = set(request.data.keys())

    if not received_fields:
        return Response(
            {"detail": "O campo 'status' é obrigatório."},
            status=status.HTTP_400_BAD_REQUEST
        )

    extra_fields = received_fields - allowed_fields
    if extra_fields:
        return Response(
            {
                "detail": "Apenas o campo 'status' pode ser alterado nesta rota.",
                "campos_recebidos": list(received_fields)
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    new_status = request.data.get("status")
    if new_status not in ["Mobilizado", "Desmobilizado"]:
        return Response(
            {"detail": "Valor de status inválido. Use 'Mobilizado' ou 'Desmobilizado'."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 🔐 Validação de permissão (se o endpoint não for público)
    if not public_endpoint:
        permission_map = {
            "Desmobilizado": desmobilize_permission,
            "Mobilizado": rehabilitate_permission,
        }
        required_permission = permission_map.get(new_status)

        has_permission = validate_permissions(
            request=request,
            userid=user_id,
            permission_type=permission_type,
            permission_to_access=[required_permission]
        )

        if not has_permission:
            return Response(
                {"detail": f"Você não tem permissão para alterar para o status '{new_status}'."},
                status=status.HTTP_403_FORBIDDEN
            )

    # ✅ Atualização
    instance.status = new_status
    instance.save()

    return Response(
        {
            "success": True,
            "message": f"{success_message} Novo status: '{new_status}'.",
            "data": {
                "id_random": instance.id_random,
                "status": instance.status
            }
        },
        status=status.HTTP_200_OK
    )




class GenericFilteredListView(ListAPIView):
    model_class = None
    serializer_class = None
    permission_type = None
    permission_code = None
    search_fields = ()
    empresa_filter_paths = ()
    extra_filters = {}
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    forbidden_message = "Você não tem permissão para visualizar"

    def get_queryset(self):
        user_id_random = self.request.user.id_random

        # Validação da permissão
        if not validate_permissions(
            request=self.request,
            userid=user_id_random,
            permission_type=self.permission_type,
            permission_to_access=[self.permission_code]
        ):
            raise PermissionDenied(self.forbidden_message)

        empresas = define_empresas(request=self.request, userid=user_id_random)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        empresas_secundarias_ids = empresas.get('empresas_secundarias_ids', [])

        filter_kwargs = {}

        # Aplica o filtro obrigatório da empresa primária
        if len(self.empresa_filter_paths) >= 1:
            filter_kwargs[self.empresa_filter_paths[0] + '__in'] = empresas_primarias_ids

        # Aplica o filtro opcional da empresa secundária
        if len(self.empresa_filter_paths) >= 2 and empresas_secundarias_ids:
            filter_kwargs[self.empresa_filter_paths[1] + '__in'] = empresas_secundarias_ids

        # Adiciona filtros extras fixos
        if self.extra_filters:
            filter_kwargs.update(self.extra_filters)

        return self.model_class.objects.filter(**filter_kwargs).distinct()

    def get_serializer_class(self):
        return self.serializer_class




def GenericCreateView(
    request,
    model_class,
    serializer_class,
    permission_type: str,
    permission_to_access: list[str],
    forbidden_message: str = "Você não tem permissão para criar este objeto.",
    foreign_key_validations: list[dict] = None,
    public_endpoint: bool = False,
    post_create_hook: callable = None  # 👈 NOVO PARÂMETRO
):
    user_id_random = request.user.id_random

    # 🔓 Se for um endpoint público, ignora validações e apenas cria
    if public_endpoint:
        data = deepcopy(request.data)
        data.pop("id_random", None)
        serializer = serializer_class(data=data)

        if serializer.is_valid():
            obj = serializer.save()

            # ⚙️ Hook de pós-criação (opcional)
            if post_create_hook:
                post_create_hook(request=request, model_class=model_class, obj=obj, data=data)

            return Response(
                {
                    "success": True,
                    "message": f"{model_class.__name__} criado com sucesso (público).",
                    "data": serializer_class(obj).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 🔒 Validação de macro serviço
    empresas = define_empresas(request=request, userid=user_id_random)
    setores = empresas.get("setores", {})

    macro_servico_map = {
        "jardinagem": ("habilitar_jardinagem", "habilitar_jardinagem_secundaria"),
        "limpeza": ("habilitar_limpeza", "habilitar_limpeza_secundaria"),
    }

    if permission_type in macro_servico_map:
        primary_flag, secondary_flag = macro_servico_map[permission_type]
        if not (setores.get(primary_flag) and setores.get(secondary_flag)):
            return Response(
                {"detail": f"Macro serviço '{permission_type}' não está habilitado para seu perfil."},
                status=status.HTTP_403_FORBIDDEN
            )

    # 🔐 Permissões
    if not validate_permissions(
        request=request,
        userid=user_id_random,
        permission_type=permission_type,
        permission_to_access=permission_to_access
    ):
        return Response({"detail": forbidden_message}, status=status.HTTP_403_FORBIDDEN)

    # 🚫 Impede definição manual de ID
    if "id_random" in request.data:
        return Response(
            {"detail": "O campo 'id_random' não pode ser definido manualmente."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 🔗 Valida chaves estrangeiras
    if foreign_key_validations:
        for rule in foreign_key_validations:
            fk_field = rule["coluna"]
            fk_model = rule["model"]
            fk_filters = rule["filters"]
            error_message = rule.get("error_message", f"{fk_field} inválido ou fora do escopo permitido.")

            fk_id = request.data.get(fk_field)
            if not fk_id:
                return Response(
                    {"detail": f"O campo '{fk_field}' é obrigatório."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not fk_model.objects.filter(id=fk_id, **fk_filters).exists():
                return Response(
                    {"detail": error_message},
                    status=status.HTTP_400_BAD_REQUEST
                )

    # 📦 Criação
    data = deepcopy(request.data)
    data.pop("id_random", None)
    serializer = serializer_class(data=data)

    if serializer.is_valid():
        obj = serializer.save()

        # ⚙️ Executa configuração pós-criação
        if post_create_hook:
            post_create_hook(request=request, model_class=model_class, obj=obj, data=data)

        return Response(
            {
                "success": True,
                "message": f"{model_class.__name__} criado com sucesso.",
                "data": serializer_class(obj).data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def GenericListByParentIdRandom(
    request,
    parent_model,
    child_model,
    serializer_class,
    parent_lookup_field: str,
    id_random: str,
    permission_type: str,
    permission_to_access: list[str],
    not_found_message: str = "Objeto pai não encontrado.",
    forbidden_message: str = "Você não tem permissão para acessar esse recurso.",
    access_filters: dict = None
):
    user_id_random = request.user.id_random

    # 🔐 Verificação de permissão
    has_permission = validate_permissions(
        request=request,
        userid=user_id_random,
        permission_type=permission_type,
        permission_to_access=permission_to_access
    )
    if not has_permission:
        return Response({"detail": forbidden_message}, status=status.HTTP_403_FORBIDDEN)

    # Verifica existência do objeto pai
    try:
        parent_model.objects.get(id_random=id_random)
    except parent_model.DoesNotExist:
        return Response({"detail": not_found_message}, status=status.HTTP_404_NOT_FOUND)

    # 🔎 Busca objetos filhos relacionados + escopo permitido
    filters = {parent_lookup_field: id_random}
    if access_filters:
        filters.update(access_filters)

    objects = child_model.objects.filter(**filters)

    serializer = serializer_class(objects, many=True, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)


def flatten_nested(obj_list, depth=0):
    """
    Converte estrutura aninhada do Django Admin (nested()) em lista formatada.
    """
    flat = []
    for item in obj_list:
        if isinstance(item, list):
            flat.extend(flatten_nested(item, depth + 1))
        else:
            flat.append(f"{'  ' * depth}- {str(item)}")
    return flat


def GenericIfDeleteView(
    request,
    *,
    model,
    id_random: str,
    permission_type: str,
    permission_to_access: list,
    access_filters: dict,
    not_found_message: str = "Objeto não encontrado.",
    forbidden_message: str = "Você não tem permissão para visualizar este recurso."
):
    user_id_random = request.user.id_random

    # Validação de permissão
    has_permission = validate_permissions(
        request=request,
        userid=user_id_random,
        permission_type=permission_type,
        permission_to_access=permission_to_access
    )

    if not has_permission:
        return Response(
            {"detail": forbidden_message},
            status=status.HTTP_403_FORBIDDEN
        )

    # Busca com filtros de acesso (ex: organização, empresa)
    try:
        instance = model.objects.get(id_random=id_random, **access_filters)
    except model.DoesNotExist:
        return Response(
            {"detail": not_found_message},
            status=status.HTTP_404_NOT_FOUND
        )

    # Coleta de objetos relacionados que seriam deletados
    collector = NestedObjects(using=router.db_for_write(model))
    collector.collect([instance])
    nested_tree = collector.nested()
    deletions_list = flatten_nested(nested_tree)

    return Response({
        "objeto_principal": str(instance),
        "resumo": {
            model.__name__: len(objs)
            for model, objs in collector.model_objs.items()
        },
        "objetos_em_cascata": deletions_list
    }, status=status.HTTP_200_OK)



def GenericListChecklistByServico(
    *,
    request,
    servico_model,
    related_model,
    serializer_class,
    permission_type: str,
    permission_to_access: list,
    forbidden_message: str,
    not_found_message: str,
    filters_related_model: dict,
    servico_id_random: str
):
    user_id_random = request.user.id_random

    # Validação de permissão
    has_permission = validate_permissions(
        request=request,
        userid=user_id_random,
        permission_type=permission_type,
        permission_to_access=permission_to_access
    )

    if not has_permission:
        return Response({"detail": forbidden_message}, status=status.HTTP_403_FORBIDDEN)

    # Verifica se o serviço existe
    try:
        servico_instance = servico_model.objects.get(id_random=servico_id_random)
    except ObjectDoesNotExist:
        return Response({"detail": not_found_message}, status=status.HTTP_404_NOT_FOUND)

    # Define empresas com base no usuário
    empresas = define_empresas(request=request, userid=user_id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    # Aplica os filtros recebidos + escopo
    queryset = related_model.objects.filter(
        **filters_related_model,
    ).distinct()

    # Serialização dos dados
    serializer = serializer_class(queryset, many=True)
    return Response(
        {
            "success": True,
            "message": f"{related_model.__name__} listado com sucesso.",
            "data": serializer.data
        },
        status=status.HTTP_200_OK
    )



# Mapeamento de permissões por status
STATUS_PERMISSION_MAP = {
    'Agendado': ['320: Pode agendar novos serviços'],
    'Em andamento': [
        '361: Pode acompanhar serviços agendados para si próprio',
        '324: Pode acompanhar serviços agendados'
    ],
    'Concluido': ['326: Pode concluir serviços em andamento'],
    'Cancelado': ['328: Pode cancelar serviços agendados']
}



def alterar_status_servico_agendado(request, id_random, model, permission_type):
    # Obtém o novo status do corpo da requisição
    novo_status = request.data.get("status", "").capitalize()

    if novo_status not in STATUS_PERMISSION_MAP:
        return Response(
            {"detail": f"Status '{novo_status}' não é permitido."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Recupera empresas relacionadas ao usuário
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    # Verifica permissões com base no status solicitado
    try:
        validate_permissions(
            request=request,
            userid=request.user.id_random,
            permission_type=permission_type,
            permission_to_access=STATUS_PERMISSION_MAP[novo_status]
        )
    except Exception as e:
        return Response(
            {"detail": str(e)},
            status=status.HTTP_403_FORBIDDEN
        )

    # Filtra os serviços e pega o primeiro
    servico = model.objects.filter(
        Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
        Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
        id_random=id_random
    ).first()

    if not servico:
        return Response(
            {"detail": "Serviço não encontrado ou acesso negado."},
            status=status.HTTP_404_NOT_FOUND
        )

    # Altera o status e salva
    servico.status = novo_status
    servico.save()

    return Response(
        {"detail": f"Status alterado com sucesso para '{novo_status}'."},
        status=status.HTTP_200_OK
    )




def GenericCreateCheckListView(
    request,
    model_class,
    serializer_class,
    permission_type: str,
    permission_to_access: list[str],
    forbidden_message: str = "Você não tem permissão para criar este objeto.",
    foreign_key_validations: list[dict] = None,
    public_endpoint: bool = False
):
    user_id_random = request.user.id_random

    # 🔓 Se for um endpoint público, ignora validações e apenas cria
    if public_endpoint:
        data = deepcopy(request.data)
        data.pop("id_random", None)
        serializer = serializer_class(data=data)

        if serializer.is_valid():
            obj = serializer.save()
            return Response(
                {
                    "success": True,
                    "message": f"{model_class.__name__} criado com sucesso (público).",
                    "data": serializer_class(obj).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 🔒 Validação de habilitação de macro serviço
    empresas = define_empresas(request=request, userid=user_id_random)
    setores = empresas.get("setores", {})

    macro_servico_map = {
        "jardinagem": ("habilitar_jardinagem", "habilitar_jardinagem_secundaria"),
        "limpeza": ("habilitar_limpeza", "habilitar_limpeza_secundaria"),
    }

    if permission_type in macro_servico_map:
        primary_flag, secondary_flag = macro_servico_map[permission_type]
        if not (setores.get(primary_flag) and setores.get(secondary_flag)):
            return Response(
                {"detail": f"Macro serviço '{permission_type}' não está habilitado para seu perfil."},
                status=status.HTTP_403_FORBIDDEN
            )

    # 🔐 Validação de permissão
    if not validate_permissions(
        request=request,
        userid=user_id_random,
        permission_type=permission_type,
        permission_to_access=permission_to_access
    ):
        return Response({"detail": forbidden_message}, status=status.HTTP_403_FORBIDDEN)

    # 🚫 Proíbe definição manual de id_random (exceto para checklists, status é permitido)
    data = deepcopy(request.data)
    data.pop("id_random", None)

    # 🚫 Proíbe campo 'status' em qualquer criação que não seja checklist
    is_checklist = permission_type == "checklist" or model_class.__name__.lower().startswith("checklist")
    if not is_checklist:
        data.pop("status", None)

    # ✅ Validação de chaves estrangeiras
    if foreign_key_validations:
        for rule in foreign_key_validations:
            fk_field = rule["coluna"]
            fk_model = rule["model"]
            fk_filters = rule["filters"]
            error_message = rule.get("error_message", f"{fk_field} inválido ou fora do escopo permitido.")

            fk_id = request.data.get(fk_field)
            if not fk_id:
                return Response(
                    {"detail": f"O campo '{fk_field}' é obrigatório."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not fk_model.objects.filter(id=fk_id, **fk_filters).exists():
                return Response(
                    {"detail": error_message},
                    status=status.HTTP_400_BAD_REQUEST
                )

    # 📦 Serialização e criação
    serializer = serializer_class(data=data)
    if serializer.is_valid():
        obj = serializer.save()
        return Response(
            {
                "success": True,
                "message": f"{model_class.__name__} criado com sucesso.",
                "data": serializer_class(obj).data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




def GenericUpdateChecklistView(
    *,
    request,
    model,
    serializer_class,
    filters: dict,
    permission_type: str,
    permission_to_access: list,
    forbidden_message: str,
    not_found_message: str,
    access_filters: dict = None,
    public_endpoint: bool = False
):
    user_id_random = request.user.id_random

    # Validação de permissão (se não for endpoint público)
    if not public_endpoint:
        has_permission = validate_permissions(
            request=request,
            userid=user_id_random,
            permission_type=permission_type,
            permission_to_access=permission_to_access
        )
        if not has_permission:
            return Response({"detail": forbidden_message}, status=status.HTTP_403_FORBIDDEN)

    # Busca do objeto
    try:
        instance = model.objects.get(**filters)
    except model.DoesNotExist:
        return Response({"detail": not_found_message}, status=status.HTTP_404_NOT_FOUND)

    # Verifica escopo do objeto (se não for endpoint público)
    if not public_endpoint and access_filters:
        scoped_qs = model.objects.filter(**filters, **access_filters)
        if not scoped_qs.exists():
            return Response({"detail": forbidden_message}, status=status.HTTP_403_FORBIDDEN)

    # Atualização parcial do objeto (agora permitindo o campo 'status')
    serializer = serializer_class(instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "success": True,
                "message": f"{model.__name__} atualizado com sucesso.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    return Response(
        {
            "success": False,
            "message": "Erro de validação.",
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )




class GenericFilteredListViewFromForms(ListAPIView):
    """
    View genérica para listagem filtrada de dados vindos de formulários,
    sem exigir validação de permissões de acesso.
    """
    model_class = None
    serializer_class = None
    search_fields = ()
    empresa_filter_paths = ()
    extra_filters = {}
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)

    def get_queryset(self):
        user_id_random = self.request.user.id_random

        empresas = define_empresas(request=self.request, userid=user_id_random)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        empresas_secundarias_ids = empresas.get('empresas_secundarias_ids', [])

        filter_kwargs = {}

        # Filtro obrigatório: empresa primária
        if len(self.empresa_filter_paths) >= 1:
            filter_kwargs[self.empresa_filter_paths[0] + '__in'] = empresas_primarias_ids

        # Filtro opcional: empresa secundária
        if len(self.empresa_filter_paths) >= 2 and empresas_secundarias_ids:
            filter_kwargs[self.empresa_filter_paths[1] + '__in'] = empresas_secundarias_ids

        # Filtros adicionais fixos
        if self.extra_filters:
            filter_kwargs.update(self.extra_filters)

        return self.model_class.objects.filter(**filter_kwargs).distinct()

    def get_serializer_class(self):
        return self.serializer_class


def GenericDeleteView(
    request,
    *,
    model,
    id_random: str,
    permission_type: str,
    permission_to_access: list,
    access_filters: dict,
    not_found_message: str = "Objeto não encontrado.",
    forbidden_message: str = "Você não tem permissão para excluir este recurso."
):
    user_id_random = request.user.id_random

    # 1. Validação de permissão
    has_permission = validate_permissions(
        request=request,
        userid=user_id_random,
        permission_type=permission_type,
        permission_to_access=permission_to_access
    )

    if not has_permission:
        return Response(
            {"detail": forbidden_message},
            status=status.HTTP_403_FORBIDDEN
        )

    # 2. Busca com filtros de acesso (escopo de empresas, etc.)
    try:
        instance = model.objects.get(id_random=id_random, **access_filters)
    except model.DoesNotExist:
        return Response(
            {"detail": not_found_message},
            status=status.HTTP_404_NOT_FOUND
        )

    # 3. Deletar objeto (em cascata, conforme relações)
    instance_repr = str(instance)
    instance.delete()

    return Response(
        {
            "detail": f"{model.__name__} '{instance_repr}' foi deletado com sucesso."
        },
        status=status.HTTP_200_OK
    )