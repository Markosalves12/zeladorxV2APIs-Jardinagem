from rest_framework import serializers
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial

class CatalogodeServicoLimpezaPredialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogodeServicoLimpezaPredial
        fields = ['id', 'id_random', 'nome', 'EmpresaSecundaria', 'status']