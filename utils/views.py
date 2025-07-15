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
    access_filters: dict = None
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

    # Busca do objeto
    try:
        instance = model.objects.get(**filters)
    except model.DoesNotExist:
        return Response({"detail": not_found_message}, status=status.HTTP_404_NOT_FOUND)

    # Verifica escopo do objeto (limite de acesso)
    if access_filters:
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
    access_filters: dict = None
):
    user_id = request.user.id_random

    # Busca o objeto
    try:
        instance = model.objects.get(**filters)
    except model.DoesNotExist:
        return Response(
            {"detail": not_found_message},
            status=status.HTTP_404_NOT_FOUND
        )

    # 🔒 Verificação de escopo (acesso)
    if access_filters:
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

    # 🔐 Validação de permissão por ação
    if new_status == "Desmobilizado":
        has_permission = validate_permissions(
            request=request,
            userid=user_id,
            permission_type=permission_type,
            permission_to_access=[desmobilize_permission]
        )
        if not has_permission:
            return Response(
                {"detail": "Você não tem permissão para desmobilizar este item."},
                status=status.HTTP_403_FORBIDDEN
            )

    elif new_status == "Mobilizado":
        has_permission = validate_permissions(
            request=request,
            userid=user_id,
            permission_type=permission_type,
            permission_to_access=[rehabilitate_permission]
        )
        if not has_permission:
            return Response(
                {"detail": "Você não tem permissão para reabilitar este item."},
                status=status.HTTP_403_FORBIDDEN
            )

    # 🟢 Atualiza status
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

    def get_queryset(self):
        user_id_random = self.request.user.id_random

        # Validação da permissão
        if not validate_permissions(
            request=self.request,
            userid=user_id_random,
            permission_type=self.permission_type,
            permission_to_access=[self.permission_code]
        ):
            raise PermissionDenied(f"Você não tem permissão para visualizar {self.permission_type}.")

        empresas = define_empresas(request=self.request, userid=user_id_random)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        empresas_secundarias_ids = empresas['empresas_secundarias_ids']

        filter_kwargs = {}
        # Monta filtros para os relacionamentos com empresas primárias e secundárias
        if self.empresa_filter_paths:
            filter_kwargs[self.empresa_filter_paths[0] + '__in'] = empresas_primarias_ids
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
    foreign_key_validations: list[dict] = None
):
    user_id_random = request.user.id_random

    # Validação de permissão
    if not validate_permissions(
        request=request,
        userid=user_id_random,
        permission_type=permission_type,
        permission_to_access=permission_to_access
    ):
        return Response({"detail": forbidden_message}, status=status.HTTP_403_FORBIDDEN)

    # Proíbe definição manual de id_random
    if "id_random" in request.data:
        return Response(
            {"detail": "O campo 'id_random' não pode ser definido manualmente."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Validação de chaves estrangeiras
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

    # Serialização e criação
    data = deepcopy(request.data)
    data.pop("id_random", None)
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