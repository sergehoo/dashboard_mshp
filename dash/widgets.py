from django_select2.forms import ModelSelect2Widget

from dash.models import DistrictSanitaire, HealthRegion, ServiceSanitaire


class RegionSelect2Widget(ModelSelect2Widget):
    model = HealthRegion  # Spécifie le modèle pour le champ Region
    search_fields = ["nom__icontains"]  # Recherche dynamique par nom de région

    def label_from_instance(self, obj):
        return obj.nom  # Affiche uniquement le nom de la région dans le menu déroulant


class DistrictNomSelect2Widget(ModelSelect2Widget):
    model = DistrictSanitaire  # Spécifie le modèle pour le champ DistrictSanitaire
    search_fields = ["nom__icontains"]  # Recherche dynamique par nom de district

    def label_from_instance(self, obj):
        return obj.nom  # Affiche uniquement le nom du district dans le menu déroulant


class CentreSanteSelect2Widget(ModelSelect2Widget):
    model = ServiceSanitaire  # Spécifiez le modèle pour le champ centre_sante
    search_fields = ["nom__icontains"]  # Recherche dynamique par nom de centre de santé

    def label_from_instance(self, obj):
        return obj.nom  # Affiche uniquement le nom du centre de santé dans le menu déroulant
