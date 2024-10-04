from django_unicorn.components import UnicornView

from dash.forms import FilterForm
from dash.models import SyntheseActivites


class DashboardUnicornView(UnicornView):
    form_class = FilterForm
    total_visites = 0
    total_recette = 0
    total_recouvrement = 0
    total_cmu = 0

    def mount(self):
        # Load data initially
        self.load_data()

    def load_data(self):
        # For initial data loading, use SyntheseActivites model
        synthese_data = SyntheseActivites.objects.all()

        self.total_visites = sum(item.total_visite for item in synthese_data)
        self.total_recette = sum(float(item.total_recette) for item in synthese_data)
        self.total_recouvrement = sum(float(item.total_recouvrement or 0) for item in synthese_data)
        self.total_cmu = self.total_recette * 0.10  # Sample calculation for CMU

    def update(self):
        # Use form to filter data and update totals
        form = self.form_class(self.data)

        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            district_id = form.cleaned_data.get('district')
            region_id = form.cleaned_data.get('region')

            filters = {}
            if start_date:
                filters['date__gte'] = start_date
            if end_date:
                filters['date__lte'] = end_date
            if district_id:
                filters['centre_sante__district_id'] = district_id
            if region_id:
                filters['centre_sante__district__region_id'] = region_id

            synthese_data = SyntheseActivites.objects.filter(**filters)

            # Update totals based on filtered data
            self.total_visites = sum(item.total_visite for item in synthese_data)
            self.total_recette = sum(float(item.total_recette) for item in synthese_data)
            self.total_recouvrement = sum(float(item.total_recouvrement or 0) for item in synthese_data)
            self.total_cmu = self.total_recette * 0.10