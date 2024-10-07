from django.db.models import Sum
from slick_reporting.views import SlickReportView

from dash.models import SyntheseActivites


class SyntheseActivitesReport(SlickReportView):
    report_model = SyntheseActivites
    group_by = 'date'
    columns = ['centre_sante__nom', 'total_visite', 'total_recette', 'total_recouvrement', 'total_cmu']

    chart_settings = [
        {
            'type': 'line',
            'data_source': ['total_visite'],
            'title': 'Visites Over Time',
            'display': 'date',
        },
        {
            'type': 'bar',
            'data_source': ['total_recette'],
            'title': 'Total Recette',
            'display': 'centre_sante__nom',
        },
        {
            'type': 'pie',
            'data_source': ['total_cmu'],
            'title': 'CMU Breakdown',
            'display': 'centre_sante__nom',
        }
    ]


class PoleRegionauxReport(SlickReportView):
    report_model = SyntheseActivites
    group_by = 'centre_sante__district__region__poles__name'  # Grouper par Pôles Régionaux
    columns = ['centre_sante__nom', 'total_visite', 'total_recette', 'total_cmu']

    chart_settings = [
        {
            'type': 'bar',
            'data_source': ['total_visite'],
            'title': 'Total Visites par Pôle Régional',
            'display': 'centre_sante__district__region__poles__name',
        },
        {
            'type': 'pie',
            'data_source': ['total_recette'],
            'title': 'Répartition des Recettes par Pôle Régional',
            'display': 'centre_sante__district__region__poles__name',
        }
    ]

    def get_data(self):
        return SyntheseActivites.objects.values(
            'centre_sante__district__region__poles__name'
        ).annotate(
            total_visite=Sum('total_visite'),
            total_recette=Sum('total_recette'),
            total_cmu=Sum('total_cmu'),
        )


class HealthRegionReport(SlickReportView):
    report_model = SyntheseActivites
    group_by = 'centre_sante__district__region__name'  # Grouper par Régions de Santé
    columns = ['centre_sante__nom', 'total_visite', 'total_recette', 'total_cmu']

    chart_settings = [
        {
            'type': 'line',
            'data_source': ['total_visite'],
            'title': 'Visites par Région de Santé',
            'display': 'centre_sante__district__region__name',
        },
        {
            'type': 'bar',
            'data_source': ['total_cmu'],
            'title': 'Total CMU par Région de Santé',
            'display': 'centre_sante__district__region__name',
        }
    ]

    def get_data(self):
        return SyntheseActivites.objects.values(
            'centre_sante__district__region__name'
        ).annotate(
            total_visite=Sum('total_visite'),
            total_recette=Sum('total_recette'),
            total_cmu=Sum('total_cmu'),
        )


class DistrictSanitaireReport(SlickReportView):
    report_model = SyntheseActivites
    group_by = 'centre_sante__district__nom'  # Grouper par Districts
    columns = ['centre_sante__nom', 'total_visite', 'total_recette', 'total_cmu']

    chart_settings = [
        {
            'type': 'bar',
            'data_source': ['total_recette'],
            'title': 'Recettes par District',
            'display': 'centre_sante__district__nom',
        },
        {
            'type': 'pie',
            'data_source': ['total_visite'],
            'title': 'Visites par District',
            'display': 'centre_sante__district__nom',
        }
    ]

    def get_data(self):
        return SyntheseActivites.objects.values(
            'centre_sante__district__nom'
        ).annotate(
            total_visite=Sum('total_visite'),
            total_recette=Sum('total_recette'),
            total_cmu=Sum('total_cmu'),
        )


