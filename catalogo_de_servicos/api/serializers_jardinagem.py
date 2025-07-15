from rest_framework import serializers
from catalogo_de_servicos.models_jardinagem import CatalogodeServicoJardinagem

class CatalogodeServicoJardinagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogodeServicoJardinagem
        fields = ['id_random', 'nome', 'EmpresaSecundaria', 'status']