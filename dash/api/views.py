from rest_framework import viewsets

from dash.api.serializers import DistrictSanitaireSerializer, ServiceSanitaireSerializer, SyntheseActivitesSerializer
from dash.models import DistrictSanitaire, ServiceSanitaire, SyntheseActivites


class DistrictSanitaireViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DistrictSanitaire.objects.all()
    serializer_class = DistrictSanitaireSerializer


class ServiceSanitaireViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ServiceSanitaire.objects.all()
    serializer_class = ServiceSanitaireSerializer


class SyntheseActivitesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SyntheseActivites.objects.all()
    serializer_class = SyntheseActivitesSerializer
