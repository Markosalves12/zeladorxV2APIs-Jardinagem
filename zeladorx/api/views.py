from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from zeladorx.models import TypeZeladoria
from zeladorx.api.serializers import TypeZeladoriaSerializer
from empresasecundario.utils import define_empresas


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def MyMacroServices(request):
    # Recupera os setores habilitados para o usuário
    empresas = define_empresas(request=request, userid=request.user.id_random)
    setores = empresas.get('setores', {})

    # Lista de setores habilitados
    tipos_habilitados = []

    if setores.get('habilitar_jardinagem') or setores.get('habilitar_jardinagem_secundaria'):
        tipos_habilitados.append("Jardinagem")

    if setores.get('habilitar_limpeza') or setores.get('habilitar_limpeza_secundaria'):
        tipos_habilitados.append("Limpeza predial")

    # Filtra os tipos de zeladoria com base nos setores habilitados
    queryset = TypeZeladoria.objects.filter(setor__in=tipos_habilitados)

    # Serializa os dados
    serializer = TypeZeladoriaSerializer(queryset, many=True)

    return Response({
        "macro_servicos_habilitados": serializer.data
    })
