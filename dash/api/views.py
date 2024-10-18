from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.response import Response

from dash.api.serializers import DistrictSanitaireSerializer, ServiceSanitaireSerializer, SyntheseActivitesSerializer, \
    HealthRegionSerializer
from dash.forms import ChatFilterForm, FiltredeForm
from dash.models import DistrictSanitaire, ServiceSanitaire, SyntheseActivites, HealthRegion, TypeServiceSanitaire
from django.contrib.gis.db.models.functions import AsGeoJSON

from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.response import Response


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
    queryset = SyntheseActivites.objects.select_related(
        'centre_sante__district__region__poles', 'centre_sante__type'
    ).all()
    serializer_class = SyntheseActivitesSerializer

    def get_queryset(self):
        queryset = self.queryset

        # Récupération des filtres depuis les paramètres de requête
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        pres = self.request.query_params.get('pres')
        region = self.request.query_params.get('region')
        district = self.request.query_params.get('district')
        type_service = self.request.query_params.get('type_service')

        # Application des filtres
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
        if type_service and type_service != '0':
            queryset = queryset.filter(centre_sante__type_id=type_service)  # Application du filtre par type

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Agrégation et regroupement des données
        poles = queryset.values(
            'centre_sante__district__region__poles__id',
            'centre_sante__district__region__poles__name'
        ).annotate(total_recette=Sum('total_recette'),
                   total_visite=Sum('total_visite'),
                   total_recouvrement=Sum('total_recouvrement'),
                   total_gratuite_ciblee=Sum('total_gratuite_ciblee'),
                   total_cas_sociaux=Sum('total_cas_sociaux'),
                   total_cmu=Sum('total_cmu'),
                   total_hors_cmu=Sum('total_hors_cmu'),
                   total_acte_reduit=Sum('total_acte_reduit'))

        regions = queryset.values(
            'centre_sante__district__region__poles__id',
            'centre_sante__district__region__id',
            'centre_sante__district__region__name'
        ).annotate(total_recette=Sum('total_recette'),
                   total_visite=Sum('total_visite'),
                   total_recouvrement=Sum('total_recouvrement'),
                   total_gratuite_ciblee=Sum('total_gratuite_ciblee'),
                   total_cas_sociaux=Sum('total_cas_sociaux'),
                   total_cmu=Sum('total_cmu'),
                   total_hors_cmu=Sum('total_hors_cmu'),
                   total_acte_reduit=Sum('total_acte_reduit'))

        districts = queryset.values(
            'centre_sante__district__region__id',
            'centre_sante__district__id',
            'centre_sante__district__nom'
        ).annotate(total_recette=Sum('total_recette'),
                   total_visite=Sum('total_visite'),
                   total_recouvrement=Sum('total_recouvrement'),
                   total_gratuite_ciblee=Sum('total_gratuite_ciblee'),
                   total_cas_sociaux=Sum('total_cas_sociaux'),
                   total_cmu=Sum('total_cmu'),
                   total_hors_cmu=Sum('total_hors_cmu'),
                   total_acte_reduit=Sum('total_acte_reduit'))

        centres = queryset.values(
            'centre_sante__district__id',
            'centre_sante__id',
            'centre_sante__nom',
            'centre_sante__type__id',
            'centre_sante__type__acronyme',
            # 'centre_sante__geom',
            geometry=AsGeoJSON('centre_sante__geom'),

        ).annotate(total_recette=Sum('total_recette'),
                   total_visite=Sum('total_visite'),
                   total_recouvrement=Sum('total_recouvrement'),
                   total_gratuite_ciblee=Sum('total_gratuite_ciblee'),
                   total_cas_sociaux=Sum('total_cas_sociaux'),
                   total_cmu=Sum('total_cmu'),
                   total_hors_cmu=Sum('total_hors_cmu'),
                   total_acte_reduit=Sum('total_acte_reduit'))

        # Structure hiérarchique des données
        data = {
            'poles': list(poles),
            'regions': list(regions),
            'districts': list(districts),
            'centres': list(centres),
        }
        return Response(data)


# class SyntheseActivitesViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = SyntheseActivites.objects.all()
#     serializer_class = SyntheseActivitesSerializer
#
#     def get_queryset(self):
#         queryset = SyntheseActivites.objects.all()
#
#         # Obtenez les paramètres de la requête pour les filtres
#         start_date = self.request.query_params.get('start_date', None)
#         end_date = self.request.query_params.get('end_date', None)
#         pres = self.request.query_params.get('pres', None)
#         region = self.request.query_params.get('region', None)
#         district = self.request.query_params.get('district', None)
#
#         # Appliquer les filtres par date
#         if start_date:
#             queryset = queryset.filter(date__gte=start_date)
#         if end_date:
#             queryset = queryset.filter(date__lte=end_date)
#
#         # Filtrer par district, région et pôle
#         if district and district != '0':
#             queryset = queryset.filter(centre_sante__district_id=district)
#         if region and region != '0':
#             queryset = queryset.filter(centre_sante__district__region_id=region)
#         if pres and pres != '0':
#             queryset = queryset.filter(centre_sante__district__region__poles__id=pres)
#
#         return queryset
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#
#         # Agréger les données par niveau hiérarchique
#         poles = queryset.values('centre_sante__district__region__poles__id',
#                                 'centre_sante__district__region__poles__name').annotate(
#             total_recette=Sum('total_recette'))
#
#         regions = queryset.values('centre_sante__district__region__poles__id', 'centre_sante__district__region__id',
#                                   'centre_sante__district__region__name').annotate(
#             total_recette=Sum('total_recette'))
#
#         districts = queryset.values('centre_sante__district__region__id', 'centre_sante__district__id',
#                                     'centre_sante__district__nom').annotate(
#             total_recette=Sum('total_recette'))
#
#         centres = queryset.values('centre_sante__district__id', 'centre_sante__id', 'centre_sante__nom').annotate(
#             total_recette=Sum('total_recette'))
#
#         # Organiser les données sous forme de hiérarchie
#         data = {
#             'poles': list(poles),
#             'regions': list(regions),
#             'districts': list(districts),
#             'centres': list(centres),
#         }
#         return Response(data)

# class SyntheseActivitesViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = SyntheseActivites.objects.all()
#     serializer_class = SyntheseActivitesSerializer
#
#     def get_queryset(self):
#         queryset = SyntheseActivites.objects.all()
#
#         # Obtenez les paramètres de la requête pour les filtres
#         start_date = self.request.query_params.get('start_date', None)
#         end_date = self.request.query_params.get('end_date', None)
#         pres = self.request.query_params.get('pres', None)
#         region = self.request.query_params.get('region', None)
#         district = self.request.query_params.get('district', None)
#
#         print(start_date, end_date, region, district)
#
#         # Appliquer les filtres
#         if start_date:
#             queryset = queryset.filter(date__gte=start_date)
#         if end_date:
#             queryset = queryset.filter(date__lte=end_date)
#
#         if district and district != '0':
#             queryset = queryset.filter(centre_sante__district_id=district)
#         if region and region != '0':
#             queryset = queryset.filter(centre_sante__district__region_id=region)
#         if pres and pres != '0':
#             queryset = queryset.filter(centre_sante__district__region__poles__id=pres)
#
#         return queryset

class TypeServiceViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        type_services = TypeServiceSanitaire.objects.values_list('acronyme', flat=True)
        return Response({'type_services': list(type_services)})


class ChartDataViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet en lecture seule qui retourne les données du graphique.
    """
    queryset = SyntheseActivites.objects.all()

    def list(self, request, *args, **kwargs):
        # Appliquer les filtres depuis le formulaire
        chat_filter_form = ChatFilterForm(request.GET or None)
        synthese_data = self.queryset  # Utilisation du queryset par défaut

        if chat_filter_form.is_valid():
            type_service = chat_filter_form.cleaned_data.get('type_service')
            if type_service:
                synthese_data = synthese_data.filter(centre_sante__type_id=type_service.id)

        # Préparer les données à retourner
        labels = [item.centre_sante.nom for item in synthese_data if item.centre_sante]
        total_visite = [item.total_visite for item in synthese_data]
        total_recette = [float(item.total_recette or 0) for item in synthese_data]
        total_cmu = [float(item.total_cmu or 0) for item in synthese_data]

        # Charger tous les types de services disponibles
        type_services = TypeServiceSanitaire.objects.values_list('acronyme', flat=True)

        # Retourner les données au format JSON
        data = {
            'labels': labels,
            'total_visite': total_visite,
            'total_recette': total_recette,
            'total_cmu': total_cmu,
            'type_services': list(type_services),
        }
        return Response(data)
