from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from semana.api.serializers import DiasDaSemanaSerializer
from semana.models import DiasDaSemana


# Response: https://gist.github.com/mitchtabian/ae03573737067c9269701ea662460205
# Headers: Authorization: Token <token>
class ListDiasDaSemana(ListAPIView):
    serializer_class = DiasDaSemanaSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('id', 'diasdasemana')

    def get_queryset(self):
        return DiasDaSemana.objects.all()