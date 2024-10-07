from rest_framework import viewsets

from dash.api.serializers import DistrictSanitaireSerializer, ServiceSanitaireSerializer, SyntheseActivitesSerializer, \
    HealthRegionSerializer
from dash.models import DistrictSanitaire, ServiceSanitaire, SyntheseActivites, HealthRegion


class HealthRegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HealthRegion.objects.all()
    serializer_class = HealthRegionSerializer


class DistrictSanitaireViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DistrictSanitaire.objects.all()
    serializer_class = DistrictSanitaireSerializer


class ServiceSanitaireViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ServiceSanitaire.objects.all()
    serializer_class = ServiceSanitaireSerializer


class SyntheseActivitesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SyntheseActivites.objects.all()
    serializer_class = SyntheseActivitesSerializer
