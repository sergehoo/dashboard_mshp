from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers

from dash.models import DistrictSanitaire, ServiceSanitaire, SyntheseActivites, HealthRegion


class HealthRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthRegion
        fields = ['id', 'name']


class DistrictSanitaireSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = DistrictSanitaire
        geo_field = 'geom'  # GeoField to be serialized as GeoJSON
        fields = ['id', 'nom', 'region', 'geojson']


class ServiceSanitaireSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ServiceSanitaire
        geo_field = 'geom'
        fields = ['id', 'nom', 'type', 'district','geom']


class SyntheseActivitesSerializer(serializers.ModelSerializer):
    centre_sante = ServiceSanitaireSerializer()

    class Meta:
        model = SyntheseActivites
        fields = ['centre_sante', 'total_visite', 'total_recette', 'total_recouvrement', 'total_cmu', 'total_acte_reduit', 'total_hors_cmu', 'total_cas_sociaux','total_gratuite_ciblee', 'date']
