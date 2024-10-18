from django_unicorn.components import UnicornView

from dash.models import TypeServiceSanitaire, SyntheseActivites


class ChartsView(UnicornView):
    selected_type = None
    types_service_sanitaire = []
    data = {}

    def mount(self):
        # Load all types on component mount
        self.types_service_sanitaire = TypeServiceSanitaire.objects.all()

    def get_filtered_data(self):
        queryset = SyntheseActivites.objects.all()

        # Filter by type of ServiceSanitaire if selected
        if self.selected_type:
            queryset = queryset.filter(centre_sante__type__id=self.selected_type)

        # Aggregate data for chart rendering
        self.data = {
            'total_recette': list(queryset.values_list('total_recette', flat=True)),
            'total_visite': list(queryset.values_list('total_visite', flat=True)),
            'total_cmu': list(queryset.values_list('total_cmu', flat=True)),
            'labels': list(queryset.values_list('date', flat=True))
        }

    def updated(self, name, value):
        # Fetch updated data when filters change
        self.get_filtered_data()