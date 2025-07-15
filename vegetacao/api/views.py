# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from vegetacao.api.serializers import CatalogoVegetacaoSerializer
from vegetacao.models import CatalogoVegetacao



# Response: https://gist.github.com/mitchtabian/ae03573737067c9269701ea662460205
# Url: https://<your-domain>/api/blog/list
# Headers: Authorization: Token <token>
class ListCatalogoVegetacao(ListAPIView):
    queryset = CatalogoVegetacao.objects.all()
    serializer_class = CatalogoVegetacaoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('nome', 'linkmapajardinagem', 'linkmapalimnpezapredial', 'empresasecundaria', 'status')