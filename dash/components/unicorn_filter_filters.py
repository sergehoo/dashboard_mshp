from django_unicorn.components import UnicornView

from dash.forms import FilterForm
from dash.models import SyntheseActivites, DistrictSanitaire, HealthRegion, PolesRegionaux


# class UnicornFilterFiltersView(UnicornView):
#     form_class = FilterForm
#
#     # Define component variables
#     start_date = None
#     end_date = None
#     district_id = None
#     region_id = None
#     pres_id = None
#
#     def load_data(self):
#         # For initial data loading, use SyntheseActivites model
#         synthese_data = SyntheseActivites.objects.all()
#
#         self.total_visites = sum(item.total_visite for item in synthese_data)
#         self.total_recette = sum(float(item.total_recette) for item in synthese_data)
#         self.total_recouvrement = sum(float(item.total_recouvrement or 0) for item in synthese_data)
#         self.total_cmu = self.total_recette * 0.10  # Sample calculation for CMU
#
#     districts = DistrictSanitaire.objects.all()
#     regions = HealthRegion.objects.all()
#     pres = PolesRegionaux.objects.all()
#
#     def update_filters(self):
#         # Update the filters based on form inputs
#         form = self.form_class({
#             'start_date': self.start_date,
#             'end_date': self.end_date,
#             'district': self.district_id,
#             'region': self.region_id,
#             'pres': self.pres_id,
#         })
#
#         if form.is_valid():
#             # Here you can apply the filters to the data
#             filtered_data = SyntheseActivites.objects.all()
#
#             if form.cleaned_data.get('start_date'):
#                 filtered_data = filtered_data.filter(date__gte=form.cleaned_data.get('start_date'))
#
#             if form.cleaned_data.get('end_date'):
#                 filtered_data = filtered_data.filter(date__lte=form.cleaned_data.get('end_date'))
#
#             if form.cleaned_data.get('district'):
#                 filtered_data = filtered_data.filter(centre_sante__district_id=form.cleaned_data.get('district'))
#
#             if form.cleaned_data.get('region'):
#                 filtered_data = filtered_data.filter(centre_sante__district__region_id=form.cleaned_data.get('region'))
#
#             if form.cleaned_data.get('pres'):
#                 filtered_data = filtered_data.filter(centre_sante__district__region__pres_id=form.cleaned_data.get('pres'))
#
#
#             # You can then use the filtered data in your component or send it back to the main dashboard
#             self.data = filtered_data
#
#     self.total_visites = sum(item.total_visite for item in synthese_data)
#     self.total_recette = sum(float(item.total_recette) for item in synthese_data)
#     self.total_recouvrement = sum(float(item.total_recouvrement or 0) for item in synthese_data)
#     self.total_cmu = self.total_recette * 0.10

class UnicornFilterFiltersView(UnicornView):
    form_class = FilterForm

    # Define component variables
    start_date = None
    end_date = None
    district_id = None
    region_id = None
    pres_id = None

    total_visites = 0
    total_recette = 0
    total_recouvrement = 0
    total_cmu = 0
    total_gratuite_ciblee = 0
    total_cas_sociaux = 0
    total_acte_reduit = 0
    total_hors_cmu = 0

    districts = DistrictSanitaire.objects.all()
    regions = HealthRegion.objects.all()
    pres = PolesRegionaux.objects.all()

    def mount(self):
        """ Called when the component is first loaded. """
        self.load_data()

    def load_data(self):
        """ Load initial data when the component is mounted. """
        synthese_data = SyntheseActivites.objects.all()

        self.total_visites = sum(item.total_visite for item in synthese_data)
        self.total_recette = sum(float(item.total_recette or 0) for item in synthese_data)
        self.total_recouvrement = sum(float(item.total_recouvrement or 0) for item in synthese_data)
        self.total_cmu = self.total_recette * 0.10  # Example calculation for CMU

        # self.total_recette = sum(float(item.total_recette or 0) for item in synthese_data)
        self.total_gratuite_ciblee = sum(float(item.total_gratuite_ciblee or 0) for item in synthese_data)
        self.total_cas_sociaux = sum(float(item.total_cas_sociaux or 0) for item in synthese_data)
        self.total_acte_reduit = sum(float(item.total_acte_reduit or 0) for item in synthese_data)
        self.total_hors_cmu = sum(float(item.total_hors_cmu or 0) for item in synthese_data)

    def update_filters(self):
        """ Update the filters based on the form inputs. """
        form = self.form_class({
            'start_date': self.start_date,
            'end_date': self.end_date,
            'district': self.district_id,
            'region': self.region_id,
            'pres': self.pres_id,
        })

        if form.is_valid():
            filtered_data = SyntheseActivites.objects.all()

            if form.cleaned_data.get('start_date'):
                filtered_data = filtered_data.filter(date__gte=form.cleaned_data.get('start_date'))

            if form.cleaned_data.get('end_date'):
                filtered_data = filtered_data.filter(date__lte=form.cleaned_data.get('end_date'))

            if form.cleaned_data.get('district'):
                filtered_data = filtered_data.filter(centre_sante__district_id=form.cleaned_data.get('district'))

            if form.cleaned_data.get('region'):
                filtered_data = filtered_data.filter(centre_sante__district__region_id=form.cleaned_data.get('region'))

            if form.cleaned_data.get('pres'):
                filtered_data = filtered_data.filter(
                    centre_sante__district__region__poles_id=form.cleaned_data.get('pres'))

            # Calculate the totals for filtered data
            self.total_visites = sum(item.total_visite for item in filtered_data)
            self.total_recette = sum(float(item.total_recette or 0) for item in filtered_data)
            self.total_recouvrement = sum(float(item.total_recouvrement or 0) for item in filtered_data)
            self.total_cmu = self.total_recette * 0.10

            self.total_gratuite_ciblee = sum(float(item.total_gratuite_ciblee or 0) for item in filtered_data)
            self.total_cas_sociaux = sum(float(item.total_cas_sociaux or 0) for item in filtered_data)
            self.total_acte_reduit = sum(float(item.total_acte_reduit or 0) for item in filtered_data)
            self.total_hors_cmu = sum(float(item.total_hors_cmu or 0) for item in filtered_data)
