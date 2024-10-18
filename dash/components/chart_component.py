from django_unicorn.components import UnicornView

from dash.models import TypeServiceSanitaire, SyntheseActivites


class ChartComponent(UnicornView):
    type_service = None
    chart_data = {
        "labels": [],
        "total_visite": [],
        "total_recette": [],
        "total_cmu": []
    }
    type_services = []

    def mount(self):
        self.type_services = TypeServiceSanitaire.objects.all()

    def load_chart_data(self):
        # Fetch the data for the chart based on the selected type_service
        query = SyntheseActivites.objects.all()
        if self.type_service:
            query = query.filter(centre_sante__type=self.type_service)

        self.chart_data['labels'] = [item.centre_sante.nom for item in query]
        self.chart_data['total_visite'] = [item.total_visite for item in query]
        self.chart_data['total_recette'] = [float(item.total_recette) for item in query]
        self.chart_data['total_cmu'] = [float(item.total_cmu) for item in query]