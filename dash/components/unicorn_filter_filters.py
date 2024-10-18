from django_unicorn.components import UnicornView

from dash.forms import FilterForm, FiltredeForm
from dash.models import SyntheseActivites, DistrictSanitaire, HealthRegion, PolesRegionaux, TypeServiceSanitaire


# class UnicornFilterFiltersView(UnicornView):
#     form_class = FiltredeForm
#
#     # Define component variables
#     start_date = None
#     end_date = None
#     district_id = None
#     region_id = None
#     pres_id = None
#
#     total_visites = 0
#     total_recette = 0
#     total_recouvrement = 0
#     total_cmu = 0
#     total_gratuite_ciblee = 0
#     total_cas_sociaux = 0
#     total_acte_reduit = 0
#     total_hors_cmu = 0
#
#     districts = DistrictSanitaire.objects.all()
#     regions = HealthRegion.objects.all()
#     pres = PolesRegionaux.objects.all()
#
#     def mount(self):
#         # self.start_date = self.start_date or ''
#         # self.end_date = self.end_date or ''
#         # self.pres_id = self.pres_id or ''
#         # self.region_id = self.region_id or ''
#         # self.district_id = self.district_id or ''
#         self.load_data()
#
#     def load_data(self):
#         print("zone du load")
#         """ Load initial data when the component is mounted. """
#         synthese_data = SyntheseActivites.objects.all()
#
#         self.total_visites = sum(item.total_visite for item in synthese_data)
#         self.total_recette = sum(float(item.total_recette or 0) for item in synthese_data)
#         self.total_recouvrement = sum(float(item.total_recouvrement or 0) for item in synthese_data)
#         self.total_cmu = self.total_recette * 0.10  # Example calculation for CMU
#
#         # self.total_recette = sum(float(item.total_recette or 0) for item in synthese_data)
#         self.total_gratuite_ciblee = sum(float(item.total_gratuite_ciblee or 0) for item in synthese_data)
#         self.total_cas_sociaux = sum(float(item.total_cas_sociaux or 0) for item in synthese_data)
#         self.total_acte_reduit = sum(float(item.total_acte_reduit or 0) for item in synthese_data)
#         self.total_hors_cmu = sum(float(item.total_hors_cmu or 0) for item in synthese_data)
#
#     def update_filters(self):
#
#         """ Update the filters based on the form inputs. """
#         print("Update filters method triggered!")
#         form = self.form_class({
#             'start_date': self.start_date,
#             'end_date': self.end_date,
#             'district': self.district_id,
#             'region': self.region_id,
#             'pres': self.pres_id,
#         })
#
#         print(f"uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu Start Date: {self.start_date}, End Date: {self.end_date}")
#
#         if form.is_valid():
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
#                 filtered_data = filtered_data.filter(
#                     centre_sante__district__region__poles_id=form.cleaned_data.get('pres'))
#
#             # Calculate the totals for filtered data
#             self.total_visites = sum(item.total_visite for item in filtered_data)
#             self.total_recette = sum(float(item.total_recette or 0) for item in filtered_data)
#             self.total_recouvrement = sum(float(item.total_recouvrement or 0) for item in filtered_data)
#             self.total_cmu = self.total_recette * 0.10
#
#             self.total_gratuite_ciblee = sum(float(item.total_gratuite_ciblee or 0) for item in filtered_data)
#             self.total_cas_sociaux = sum(float(item.total_cas_sociaux or 0) for item in filtered_data)
#             self.total_acte_reduit = sum(float(item.total_acte_reduit or 0) for item in filtered_data)
#             self.total_hors_cmu = sum(float(item.total_hors_cmu or 0) for item in filtered_data)

class UnicornFilterFiltersView(UnicornView):
    form_class = FiltredeForm

    # Define component variables
    start_date = None
    end_date = None
    district_id = None
    region_id = None
    pres_id = None
    type_service_id = None

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
    type_service = TypeServiceSanitaire.objects.all()

    def mount(self):
        # Initialize filters with default values if not provided
        self.start_date = self.start_date or None
        self.end_date = self.end_date or None
        self.district_id = self.district_id or None
        self.region_id = self.region_id or None
        self.pres_id = self.pres_id or None
        self.type_service_id = self.type_service_id or None

        # Load initial data
        self.load_data()

        # Initialiser la liste des types de service
        self.type_service = TypeServiceSanitaire.objects.all()

    def load_data(self):
        """ Load initial data when the component is mounted. """
        print("Chargement des données initiales")
        synthese_data = SyntheseActivites.objects.all()

        # Calculate totals for the initial unfiltered data
        self.total_visites = sum(item.total_visite for item in synthese_data)
        self.total_recette = sum(float(item.total_recette or 0) for item in synthese_data)
        self.total_recouvrement = sum(float(item.total_recouvrement or 0) for item in synthese_data)
        self.total_cmu = self.total_recette * 0.10  # Example calculation for CMU
        self.total_gratuite_ciblee = sum(float(item.total_gratuite_ciblee or 0) for item in synthese_data)
        self.total_cas_sociaux = sum(float(item.total_cas_sociaux or 0) for item in synthese_data)
        self.total_acte_reduit = sum(float(item.total_acte_reduit or 0) for item in synthese_data)
        self.total_hors_cmu = sum(float(item.total_hors_cmu or 0) for item in synthese_data)

    def update_filters(self):
        """ Update the filters based on the form inputs. """
        print("Mise à jour des filtres !")

        # Initialize the form with current filters
        form = self.form_class({
            'start_date': self.start_date,
            'end_date': self.end_date,
            'district': self.district_id,
            'region': self.region_id,
            'pres': self.pres_id,
            'type_service': self.type_service_id,  # Ajoutez ici le type de service
        })

        # Ensure form is valid before filtering data
        if form.is_valid():
            filtered_data = SyntheseActivites.objects.all()

            # Apply date filters if provided
            if form.cleaned_data.get('start_date'):
                filtered_data = filtered_data.filter(date__gte=form.cleaned_data.get('start_date'))

            if form.cleaned_data.get('end_date'):
                filtered_data = filtered_data.filter(date__lte=form.cleaned_data.get('end_date'))

            # Apply district, region, and pres (pole régional) filters
            if form.cleaned_data.get('district'):
                filtered_data = filtered_data.filter(centre_sante__district_id=form.cleaned_data.get('district'))

            if form.cleaned_data.get('region'):
                filtered_data = filtered_data.filter(centre_sante__district__region_id=form.cleaned_data.get('region'))

            if form.cleaned_data.get('pres'):
                filtered_data = filtered_data.filter(
                    centre_sante__district__region__poles_id=form.cleaned_data.get('pres'))

            if form.cleaned_data.get('type_service'):
                filtered_data = filtered_data.filter(
                    centre_sante__type_id=form.cleaned_data.get('type_service'))  # Filtre par type

            # Recalculate the totals for the filtered data
            self.total_visites = sum(item.total_visite for item in filtered_data)
            self.total_recette = sum(float(item.total_recette or 0) for item in filtered_data)
            self.total_recouvrement = sum(float(item.total_recouvrement or 0) for item in filtered_data)
            self.total_cmu = self.total_recette * 0.10  # Example calculation for CMU
            self.total_gratuite_ciblee = sum(float(item.total_gratuite_ciblee or 0) for item in filtered_data)
            self.total_cas_sociaux = sum(float(item.total_cas_sociaux or 0) for item in filtered_data)
            self.total_acte_reduit = sum(float(item.total_acte_reduit or 0) for item in filtered_data)
            self.total_hors_cmu = sum(float(item.total_hors_cmu or 0) for item in filtered_data)

        # Handle case where form is not valid
        else:
            print(f"Formulaire invalide avec des erreurs : {form.errors}")

    def reset_filters(self):
        """ Reset filters to default values and reload data. """
        self.start_date = None
        self.end_date = None
        self.district_id = None
        self.region_id = None
        self.pres_id = None
        self.type_service_id = None

        # Reload data with no filters
        self.load_data()
