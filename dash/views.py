from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render

# Create your views here.

# views.py
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django_unicorn.components import UnicornView

from .forms import ExcelUploadForm, FilterForm
from .models import SyntheseActivites, ServiceSanitaire, PolesRegionaux, DistrictSanitaire
# from .forms import ExcelUploadForm
from django.utils.dateparse import parse_date
from datetime import datetime


def parse_date(date_str):
    # Try parsing the date using multiple formats
    try:
        return parse_date(date_str)
    except ValueError:
        try:
            return datetime.strptime(date_str, '%d/%m/%Y').date()
        except ValueError:
            return None  # Return None if the date cannot be parsed


def import_synthese_view(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)

        if form.is_valid():
            excel_file = request.FILES['file']

            # Read the Excel file using pandas
            try:
                df = pd.read_excel(excel_file, engine='openpyxl')

                # Iterate over the rows of the DataFrame
                for index, row in df.iterrows():
                    try:
                        centre_nom = row['CENTRES DE SANTÉ']
                        total_visite = row.get('TOTAL VISITE', 0)  # Default to 0 if missing
                        total_recette = row.get('TOTAL RECETTE', 0)
                        total_recouvrement = row.get('TOTAL RECOUVREMENT', 0)
                        total_gratuite_ciblee = row.get('TOTAL GRATUITÉ CIBLÉE', 0)
                        total_cas_sociaux = row.get('TOTAL CAS SOCIAUX', 0)
                        total_acte_reduit = row.get('TOTAL ACTE RÉDUIS', 0)
                        total_cmu = row.get('TOTAL CMU', 0)
                        total_hors_cmu = row.get('TOTAL HORS CMU', 0)
                        date_str = row['DATE']

                        # Parse date
                        date = parse_date(str(date_str))
                        if not date:
                            messages.warning(request,
                                             f"Invalid date format for {centre_nom} on row {index + 1}. Skipping.")
                            continue

                        # Determine the type of health center based on the name
                        type_mapping = {
                            'CHR': 'Centre Hospitalier Régional',
                            'CHU': 'Centre Hospitalier Universitaire',
                            'CSU': 'Centre de Santé Urbain',
                            'HG': 'Hôpital Général',
                        }

                        centre_type = None
                        for key, value in type_mapping.items():
                            if key in centre_nom:
                                centre_type = value
                                break

                        # Fetch the corresponding ServiceSanitaire object based on the name and type
                        centre_sante = ServiceSanitaire.objects.filter(nom__icontains=centre_nom,
                                                                       type=centre_type).first()

                        if not centre_sante:
                            messages.warning(request, f"No matching ServiceSanitaire found for {centre_nom}. Skipping.")
                            continue

                        # Create or update the SyntheseActivites record
                        SyntheseActivites.objects.update_or_create(
                            centre_sante=centre_sante,
                            date=date,
                            defaults={
                                'total_visite': total_visite,
                                'total_recette': total_recette,
                                'total_recouvrement': total_recouvrement,
                                'total_gratuite_ciblee': total_gratuite_ciblee,
                                'total_cas_sociaux': total_cas_sociaux,
                                'total_acte_reduit': total_acte_reduit,
                                'total_cmu': total_cmu,
                                'total_hors_cmu': total_hors_cmu,
                            }
                        )
                    except KeyError as key_error:
                        messages.warning(request, f"Missing column: {key_error}. Skipping row {index + 1}.")
                    except Exception as e:
                        messages.warning(request, f"Error processing row {index + 1}: {str(e)}")
                        continue

                messages.success(request, "SyntheseActivites data imported successfully.")
                return redirect('import_synthese')

            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('import_synthese')

    else:
        form = ExcelUploadForm()

    return render(request, 'dashboard/import_synthese.html', {'form': form})


# HEALTH_CENTER_TYPES = {
#     'CHR': 'Centre Hospitalier Régional',
#     'CHU': 'Centre Hospitalier Universitaire',
#     'CSU': 'Centre de Santé Urbain',
#     'HG': 'Hôpital Général'
# }


# def import_synthese_view(request):
#     if request.method == 'POST':
#         # Get the uploaded file from the request
#         excel_file = request.FILES['excel_file']
#
#         # Read the Excel file
#         try:
#             df = pd.read_excel(excel_file, engine='openpyxl')
#
#             # Iterate through the DataFrame and save data
#             for index, row in df.iterrows():
#                 # Mapping health center type to the full name
#                 health_center_type = row['Type']
#                 full_health_center_type = HEALTH_CENTER_TYPES.get(health_center_type, health_center_type)
#
#                 # Get or create the ServiceSanitaire object
#                 service_sanitaire, created = ServiceSanitaire.objects.get_or_create(
#                     nom=row['Nom du Service'],
#                     defaults={
#                         'type': full_health_center_type,
#                         'district': DistrictSanitaire.objects.filter(nom=row['District']).first(),
#                         # Add other fields if necessary
#                     }
#                 )
#
#                 # Create SyntheseActivites entry
#                 SyntheseActivites.objects.create(
#                     centre_sante=service_sanitaire,
#                     total_visite=row['Total Visites'],
#                     total_recette=row['Total Recettes'],
#                     total_recouvrement=row['Total Recouvrement'],
#                     total_gratuite_ciblee=row['Total Gratuité Ciblée'],
#                     total_cas_sociaux=row['Total Cas Sociaux'],
#                     total_acte_reduit=row['Total Acte Réduit'],
#                     total_cmu=row['Total CMU'],
#                     total_hors_cmu=row['Total Hors CMU'],
#                     date=row['Date']
#                 )
#
#             return redirect('success_url')  # Redirect to a success page after import
#
#         except Exception as e:
#             return render(request, 'dashboard/import_synthese.html', {'error': str(e)})


# class DashboardUnicornView(UnicornView):
#     form_class = FilterForm
#     data = []
#
#     def update(self):
#         # Filter data based on form input
#         form = self.form_class(self.data)
#
#         if form.is_valid():
#             start_date = form.cleaned_data.get('start_date')
#             end_date = form.cleaned_data.get('end_date')
#             district_id = form.cleaned_data.get('district')
#             region_id = form.cleaned_data.get('region')
#
#             filters = {}
#             if start_date:
#                 filters['date__gte'] = start_date
#             if end_date:
#                 filters['date__lte'] = end_date
#             if district_id:
#                 filters['centre_sante__district=district_id'] = district_id
#             if region_id:
#                 filters['centre_sante__district__region_id'] = region_id
#
#             self.data = SyntheseActivites.objects.filter(**filters)
# def preview_import_view(request):
#     if request.method == 'POST':
#         form = ExcelUploadForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             excel_file = request.FILES['file']
#
#             try:
#                 # Read the Excel file using pandas
#                 df = pd.read_excel(excel_file, engine='openpyxl')
#
#                 # Extract data for previsualization (up to a certain number of rows for performance)
#                 preview_data = df.head(10)  # Only show the first 10 rows for preview
#
#                 # Store the DataFrame in session (to access after confirmation)
#                 request.session['preview_data'] = df.to_dict('records')  # Convert to a list of dictionaries
#
#                 return render(request, 'dashboard/import_preview.html', {
#                     'form': form,
#                     'preview_data': preview_data.to_html(index=False),  # Convert to HTML for rendering in template
#                 })
#
#             except Exception as e:
#                 messages.error(request, f"An error occurred while reading the Excel file: {str(e)}")
#                 return redirect('preview_import')
#
#     else:
#         form = ExcelUploadForm()
#
#     return render(request, 'dashboard/import_synthese.html', {'form': form})

def preview_import_view(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)

        if form.is_valid():
            excel_file = request.FILES['file']

            try:
                # Read the Excel file using pandas
                df = pd.read_excel(excel_file, engine='openpyxl')

                # Convert dates to string format (if applicable)
                for col in df.columns:
                    if pd.api.types.is_datetime64_any_dtype(df[col]):
                        df[col] = df[col].dt.strftime('%Y-%m-%d')  # Convert to string format

                # Extract data for previsualization (up to a certain number of rows for performance)
                preview_data = df.head(10)  # Only show the first 10 rows for preview

                # Store the DataFrame in session (to access after confirmation)
                request.session['preview_data'] = df.to_dict('records')  # Convert to a list of dictionaries

                return render(request, 'dashboard/import_preview.html', {
                    'form': form,
                    'preview_data': preview_data.to_html(index=False),  # Convert to HTML for rendering in template
                })

            except Exception as e:
                messages.error(request, f"An error occurred while reading the Excel file: {str(e)}")
                return redirect('import_synthese')

    else:
        form = ExcelUploadForm()

    return render(request, 'dashboard/import_form.html', {'form': form})
def confirm_import_view(request):
    # Check if there is preview data in the session
    if 'preview_data' not in request.session:
        messages.error(request, "No preview data found. Please upload the file again.")
        return redirect('preview_import')

    if request.method == 'POST':
        preview_data = request.session.get('preview_data')

        try:
            for row in preview_data:
                # Extract data from the session-stored preview
                centre_nom = row['CENTRES DE SANTÉ']
                total_visite = row.get('TOTAL VISITE', 0)
                total_recette = row.get('TOTAL RECETTE', 0)
                total_recouvrement = row.get('TOTAL RECOUVREMENT', 0)
                total_gratuite_ciblee = row.get('TOTAL GRATUITÉ CIBLÉE', 0)
                total_cas_sociaux = row.get('TOTAL CAS SOCIAUX', 0)
                total_acte_reduit = row.get('TOTAL ACTE RÉDUIS', 0)
                total_cmu = row.get('TOTAL CMU', 0)
                total_hors_cmu = row.get('TOTAL HORS CMU', 0)
                date_str = row['DATE']

                # Parse date
                date = parse_date(str(date_str))

                # Determine the type of health center based on the name
                type_mapping = {
                    'CHR': 'Centre Hospitalier Régional',
                    'CHU': 'Centre Hospitalier Universitaire',
                    'CSU': 'Centre de Santé Urbain',
                    'HG': 'Hôpital Général',
                }

                centre_type = None
                for key, value in type_mapping.items():
                    if key in centre_nom:
                        centre_type = value
                        break

                # Fetch the corresponding ServiceSanitaire object based on the name and type
                centre_sante = ServiceSanitaire.objects.filter(nom__icontains=centre_nom, type=centre_type).first()

                if not centre_sante:
                    messages.warning(request, f"No matching ServiceSanitaire found for {centre_nom}. Skipping.")
                    continue

                # Create or update the SyntheseActivites record
                SyntheseActivites.objects.update_or_create(
                    centre_sante=centre_sante,
                    date=date,
                    defaults={
                        'total_visite': total_visite,
                        'total_recette': total_recette,
                        'total_recouvrement': total_recouvrement,
                        'total_gratuite_ciblee': total_gratuite_ciblee,
                        'total_cas_sociaux': total_cas_sociaux,
                        'total_acte_reduit': total_acte_reduit,
                        'total_cmu': total_cmu,
                        'total_hors_cmu': total_hors_cmu,
                    }
                )

            # Clear the session after import
            request.session.pop('preview_data', None)

            messages.success(request, "Data imported successfully.")
            return redirect('import_synthese')

        except Exception as e:
            messages.error(request, f"An error occurred during import: {str(e)}")
            return redirect('import_synthese')

    return render(request, 'dashboard/import_synthese.html')


def get_top_districts():
    top_districts = (
        SyntheseActivites.objects.values('centre_sante__district__nom')
        .annotate(
            total_visite=Sum('total_visite'),
            total_recette=Sum('total_recette'),
            total_recouvrement=Sum('total_recouvrement'),
            total_cmu=Sum('total_cmu'),
        )
        .order_by('-total_visite', '-total_recette', '-total_recouvrement', '-total_cmu')[:5]
    )
    return top_districts


# def get_pole_totals():
#     # Aggregate total_recette by Pole Régional
#     poles_totals = (
#         PolesRegionaux.objects.prefetch_related('healthregion_set__districtsanitaire_set__servicesanitaire_set')
#         .annotate(
#             total_recette=Sum('healthregion__districtsanitaire__servicesanitaire__syntheseactivites__total_recette'))
#     )
#     return poles_totals


def get_pole_totals_with_regions_and_districts():
    # Aggregate total_recette for poles, regions, and districts
    poles_totals = (
        PolesRegionaux.objects.prefetch_related(
            'healthregion_set__districtsanitaire_set__servicesanitaire_set__syntheseactivites_set'
        )
        .annotate(
            total_recette=Sum('healthregion__districtsanitaire__servicesanitaire__syntheseactivites__total_recette')
        )
    )

    # Annotate total_recette for each region
    for pole in poles_totals:
        for region in pole.healthregion_set.all():
            region.total_recette = (
                    SyntheseActivites.objects.filter(
                        centre_sante__district__region=region
                    ).aggregate(total_recette=Sum('total_recette'))['total_recette'] or 0
            )

            # Annotate total_recette for each district
            for district in region.districtsanitaire_set.all():
                district.total_recette = (
                        SyntheseActivites.objects.filter(
                            centre_sante__district=district
                        ).aggregate(total_recette=Sum('total_recette'))['total_recette'] or 0
                )

    return poles_totals


class DashboardView(LoginRequiredMixin,TemplateView):
    login_url = '/accounts/login/'
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = FilterForm()
        context['synthese_data'] = SyntheseActivites.objects.all()  # Default to all data
        # Fetch Pôles, Regions, Districts, and Centres de Santé
        # poles = PolesRegionaux.objects.prefetch_related(
        #     'healthregion_set__districtsanitaire_set__servicesanitaire_set'
        # )
        context['poles'] = get_pole_totals_with_regions_and_districts()

        # context['poles'] = poles
        context['top_districts'] = get_top_districts()

        return context


class SyntheseActivitesView(ListView):
    model = SyntheseActivites
    context_object_name = 'synthese_data'
    template_name = 'dashboard/syntheseview.html'
