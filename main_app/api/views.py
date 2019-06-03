from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from ..models import Sites, Devices

from .serializers import SitesSerializer, DevicesSerializer

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


#Devices views

class DevicesListCreateAPIView(ListCreateAPIView):

    queryset = Devices.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = DevicesSerializer
    lookup_field = "uuid" # Dont use the model id or pk for API


class DevicesRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    queryset = Devices.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = DevicesSerializer
    lookup_field = 'uuid' # Dont use the model id or pk for API
