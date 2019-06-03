from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from ..models import Sites

from .serializers import SitesSerializer

class SitesListCreateAPIView(ListCreateAPIView):

    queryset = Sites.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = SitesSerializer
    lookup_field = "uuid" # Dont use the model id or pk for API


class SitesRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    queryset = Sites.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = SitesSerializer
    lookup_field = 'uuid' # Dont use the model id or pk for API
