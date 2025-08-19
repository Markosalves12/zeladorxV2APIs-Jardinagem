from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from empresaprimaria.models import EmpresaPrimaria
from empresaprimaria.api.serializer import EmpresaSecundariaSerializer
from empresasecundario.utils import define_empresas


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def empresaprimaria(request):
    # Recupera os setores habilitados para o usuário
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']

    # Filtra os tipos de zeladoria com base nos setores habilitados
    queryset = EmpresaPrimaria.objects.filter(id_random__in=empresas_primarias_ids)

    # Serializa os dados
    serializer = EmpresaSecundariaSerializer(queryset, many=True)

    return Response({
        "empresa_primaria": serializer.data
    })
