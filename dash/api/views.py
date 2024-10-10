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

    def get_queryset(self):
        queryset = SyntheseActivites.objects.all()

        # Obtenez les paramètres de la requête pour les filtres
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        pres = self.request.query_params.get('pres', None)
        region = self.request.query_params.get('region', None)
        district = self.request.query_params.get('district', None)

        print(start_date, end_date, region, district)

        # Appliquer les filtres
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        if district and district != '0':
            queryset = queryset.filter(centre_sante__district_id=district)
        if region and region != '0':
            queryset = queryset.filter(centre_sante__district__region_id=region)
        if pres and pres != '0':
            queryset = queryset.filter(centre_sante__district__region__poles__id=pres)

        return queryset
