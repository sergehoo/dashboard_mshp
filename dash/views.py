from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

# views.py
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView
from django_unicorn.components import UnicornView
from slick_reporting.views import SlickReportView

from .forms import ExcelUploadForm, FilterForm, ChatFilterForm, CombinedFilterForm
from .models import SyntheseActivites, ServiceSanitaire, PolesRegionaux, DistrictSanitaire, TypeServiceSanitaire
# from .forms import ExcelUploadForm
from django.utils.dateparse import parse_date
from datetime import datetime


# def import_synthese_view(request):
#     if request.method == 'POST':
#         form = ExcelUploadForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             excel_file = request.FILES['file']
#
#             # Read the Excel file using pandas
#             try:
#                 df = pd.read_excel(excel_file, engine='openpyxl')
#
#                 # Iterate over the rows of the DataFrame
#                 for index, row in df.iterrows():
#                     try:
#                         centre_nom = row['CENTRES DE SANTÉ']
#                         total_visite = row.get('TOTAL VISITE', 0)  # Default to 0 if missing
#                         total_recette = row.get('TOTAL RECETTE', 0)
#                         total_recouvrement = row.get('TOTAL RECOUVREMENT', 0)
#                         total_gratuite_ciblee = row.get('TOTAL GRATUITÉ CIBLÉE', 0)
#                         total_cas_sociaux = row.get('TOTAL CAS SOCIAUX', 0)
#                         total_acte_reduit = row.get('TOTAL ACTE RÉDUIS', 0)
#                         total_cmu = row.get('TOTAL CMU', 0)
#                         total_hors_cmu = row.get('TOTAL HORS CMU', 0)
#                         date_str = row['DATE']
#
#                         # Parse date
#                         date = parse_date(str(date_str))
#                         if not date:
#                             messages.warning(request,
#                                              f"Invalid date format for {centre_nom} on row {index + 1}. Skipping.")
#                             continue
#
#                         # Determine the type of health center based on the name
#                         type_mapping = {
#                             'CHR': 'Centre Hospitalier Régional',
#                             'CHU': 'Centre Hospitalier Universitaire',
#                             'CSU': 'Centre de Santé Urbain',
#                             'HG': 'Hôpital Général',
#                         }
#
#                         centre_type = None
#                         for key, value in type_mapping.items():
#                             if key in centre_nom:
#                                 centre_type = value
#                                 break
#
#                         # Fetch the corresponding ServiceSanitaire object based on the name and type
#                         centre_sante = ServiceSanitaire.objects.filter(nom__icontains=centre_nom,
#                                                                        type=centre_type).first()
#
#                         if not centre_sante:
#                             messages.warning(request, f"No matching ServiceSanitaire found for {centre_nom}. Skipping.")
#                             continue
#
#                         # Create or update the SyntheseActivites record
#                         SyntheseActivites.objects.update_or_create(
#                             centre_sante=centre_sante,
#                             date=date,
#                             defaults={
#                                 'total_visite': total_visite,
#                                 'total_recette': total_recette,
#                                 'total_recouvrement': total_recouvrement,
#                                 'total_gratuite_ciblee': total_gratuite_ciblee,
#                                 'total_cas_sociaux': total_cas_sociaux,
#                                 'total_acte_reduit': total_acte_reduit,
#                                 'total_cmu': total_cmu,
#                                 'total_hors_cmu': total_hors_cmu,
#                             }
#                         )
#                     except KeyError as key_error:
#                         messages.warning(request, f"Missing column: {key_error}. Skipping row {index + 1}.")
#                     except Exception as e:
#                         messages.warning(request, f"Error processing row {index + 1}: {str(e)}")
#                         continue
#
#                 messages.success(request, "SyntheseActivites data imported successfully.")
#                 return redirect('import_synthese')
#
#             except Exception as e:
#                 messages.error(request, f"An error occurred: {str(e)}")
#                 return redirect('import_synthese')
#
#     else:
#         form = ExcelUploadForm()
#
#     return render(request, 'dashboard/import_synthese.html', {'form': form})


# def import_synthese_view(request):
#     if request.method == 'POST':
#         form = ExcelUploadForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             excel_file = request.FILES['file']
#
#             try:
#                 df = pd.read_excel(excel_file, engine='openpyxl')
#                 data = df.to_dict(orient='records')
#
#                 # Prévisualisation des données
#                 preview_data = data[:5]  # On prend les 5 premières lignes pour la prévisualisation
#
#                 # Validation et sauvegarde des données
#                 errors = []
#                 for index, record in enumerate(data):
#                     try:
#                         centre_nom = record['CENTRES DE SANTÉ']
#
#                         # Nettoyer et convertir les valeurs numériques
#                         total_visite = int(record.get('TOTAL VISITE', 0))
#                         total_recette = Decimal(str(record.get('TOTAL RECETTE', 0)).replace(' ', ''))
#                         total_recouvrement = Decimal(str(record.get('TOTAL RECOUVREMENT', 0)).replace(' ', ''))
#                         total_gratuite_ciblee = Decimal(str(record.get('TOTAL GRATUITÉ CIBLÉE', 0)).replace(' ', ''))
#                         total_cas_sociaux = int(record.get('TOTAL CAS SOCIAUX', 0))
#                         total_acte_reduit = Decimal(str(record.get('TOTAL ACTE RÉDUIS', 0)).replace(' ', ''))
#                         total_cmu = Decimal(str(record.get('TOTAL CMU', 0)).replace(' ', ''))
#                         total_hors_cmu = Decimal(str(record.get('TOTAL HORS CMU', 0)).replace(' ', ''))
#
#                         date_str = record['DATE']
#
#                         # Vérification des valeurs numériques
#                         if total_recette > Decimal('99999999999999999999.99') or total_recouvrement > Decimal(
#                                 '99999999999999999999.99'):
#                             errors.append(f"Valeur numérique trop grande pour {centre_nom} sur la ligne {index + 1}.")
#                             continue
#
#                         date = parse_date(str(date_str))
#                         if not date:
#                             errors.append(f"Format de date invalide pour {centre_nom} sur la ligne {index + 1}.")
#                             continue
#
#                         # Déterminer le type de centre de santé
#                         type_mapping = {
#                             'CHR': 'Centre Hospitalier Régional',
#                             'CHU': 'Centre Hospitalier Universitaire',
#                             'CSU': 'Centre de Santé Urbain',
#                             'HG': 'Hôpital Général',
#                         }
#
#                         centre_type = None
#                         for key, value in type_mapping.items():
#                             if key in centre_nom:
#                                 centre_type = value
#                                 break
#
#                         # Obtenir ou créer une instance de TypeServiceSanitaire
#                         type_service, created = TypeServiceSanitaire.objects.get_or_create(
#                             nom=centre_type,
#                             defaults={'acronyme': key}  # Utilisez la clé du mapping comme acronyme
#                         )
#
#                         # Recherche ou création du ServiceSanitaire
#                         centre_sante, created = ServiceSanitaire.objects.get_or_create(
#                             nom=centre_nom,
#                             defaults={'type': type_service}
#                         )
#
#                         # Création ou mise à jour de SyntheseActivites
#                         SyntheseActivites.objects.update_or_create(
#                             centre_sante=centre_sante,
#                             date=date,
#                             defaults={
#                                 'total_visite': total_visite,
#                                 'total_recette': total_recette,
#                                 'total_recouvrement': total_recouvrement,
#                                 'total_gratuite_ciblee': total_gratuite_ciblee,
#                                 'total_cas_sociaux': total_cas_sociaux,
#                                 'total_acte_reduit': total_acte_reduit,
#                                 'total_cmu': total_cmu,
#                                 'total_hors_cmu': total_hors_cmu,
#                             }
#                         )
#                     except KeyError as key_error:
#                         errors.append(f"Colonne manquante : {key_error}. Ligne {index + 1} ignorée.")
#                     except Exception as e:
#                         errors.append(f"Erreur lors du traitement de la ligne {index + 1} : {str(e)}")
#
#                 if errors:
#                     return JsonResponse({'status': 'partial_success', 'preview_data': preview_data, 'errors': errors})
#                 else:
#                     return JsonResponse({'status': 'success', 'preview_data': preview_data})
#
#             except Exception as e:
#                 return JsonResponse({'status': 'error', 'message': str(e)})
#
#     else:
#         form = ExcelUploadForm()
#
#     return render(request, 'dashboard/import_synthese.html', {'form': form})

def parse_date(date_str):
    """
    Parse date from string in multiple formats.
    """
    date_formats = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y']
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    return None


# def import_synthese_view(request):
#     if request.method == 'POST':
#         form = ExcelUploadForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             excel_file = request.FILES['file']
#
#             try:
#                 df = pd.read_excel(excel_file, engine='openpyxl')
#                 data = df.to_dict(orient='records')
#
#                 # Afficher le contenu de la ligne 25
#                 row_25 = data[24]  # L'indexation commence à 0, donc la ligne 25 est l'index 24
#                 print("Contenu de la ligne 25 :", row_25)
#
#                 # Prévisualisation des données
#                 preview_data = data[:5]  # On prend les 5 premières lignes pour la prévisualisation
#
#                 # Validation et sauvegarde des données
#                 errors = []
#                 for index, record in enumerate(data):
#                     try:
#                         centre_nom = record['CENTRES DE SANTÉ']
#
#                         # Nettoyer et convertir les valeurs numériques
#                         total_visite = int(record.get('TOTAL VISITE', 0))
#                         total_recette = Decimal(str(record.get('TOTAL RECETTE', 0)).replace(' ', ''))
#                         total_recouvrement = Decimal(str(record.get('TOTAL RECOUVREMENT', 0)).replace(' ', ''))
#                         total_gratuite_ciblee = Decimal(str(record.get('TOTAL GRATUITÉ CIBLÉE', 0)).replace(' ', ''))
#                         total_cas_sociaux = int(record.get('TOTAL CAS SOCIAUX', 0))
#                         total_acte_reduit = Decimal(str(record.get('TOTAL ACTE RÉDUIS', 0)).replace(' ', ''))
#                         total_cmu = Decimal(str(record.get('TOTAL CMU', 0)).replace(' ', ''))
#                         total_hors_cmu = Decimal(str(record.get('TOTAL HORS CMU', 0)).replace(' ', ''))
#
#                         date_str = record['DATE']
#
#                         # Vérification des valeurs numériques
#                         if total_recette > Decimal('99999999999999999999.99') or total_recouvrement > Decimal(
#                                 '99999999999999999999.99'):
#                             errors.append(f"Valeur numérique trop grande pour {centre_nom} sur la ligne {index + 1}.")
#                             continue
#
#                         date = parse_date(str(date_str))
#                         if not date:
#                             errors.append(f"Format de date invalide pour {centre_nom} sur la ligne {index + 1}.")
#                             continue
#
#                         # Déterminer le type de centre de santé
#                         type_mapping = {
#                             'CHR': 'Centre Hospitalier Régional',
#                             'CHU': 'Centre Hospitalier Universitaire',
#                             'CSU': 'Centre de Santé Urbain',
#                             'HG': 'Hôpital Général',
#                         }
#
#                         centre_type = None
#                         for key, value in type_mapping.items():
#                             if key in centre_nom:
#                                 centre_type = value
#                                 break
#
#                         # Obtenir ou créer une instance de TypeServiceSanitaire
#                         type_service, created = TypeServiceSanitaire.objects.get_or_create(
#                             nom=centre_type,
#                             defaults={'acronyme': key}  # Utilisez la clé du mapping comme acronyme
#                         )
#
#                         # Recherche ou création du ServiceSanitaire
#                         centre_sante, created = ServiceSanitaire.objects.get_or_create(
#                             nom=centre_nom,
#                             defaults={'type': type_service}
#                         )
#
#                         # Création ou mise à jour de SyntheseActivites
#                         SyntheseActivites.objects.update_or_create(
#                             centre_sante=centre_sante,
#                             date=date,
#                             defaults={
#                                 'total_visite': total_visite,
#                                 'total_recette': total_recette,
#                                 'total_recouvrement': total_recouvrement,
#                                 'total_gratuite_ciblee': total_gratuite_ciblee,
#                                 'total_cas_sociaux': total_cas_sociaux,
#                                 'total_acte_reduit': total_acte_reduit,
#                                 'total_cmu': total_cmu,
#                                 'total_hors_cmu': total_hors_cmu,
#                             }
#                         )
#                     except KeyError as key_error:
#                         errors.append(f"Colonne manquante : {key_error}. Ligne {index + 1} ignorée.")
#                     except Exception as e:
#                         errors.append(f"Erreur lors du traitement de la ligne {index + 1} : {str(e)}")
#
#                 if errors:
#                     return JsonResponse({'status': 'partial_success', 'preview_data': preview_data, 'errors': errors})
#                 else:
#                     return JsonResponse({'status': 'success', 'preview_data': preview_data})
#
#             except Exception as e:
#                 return JsonResponse({'status': 'error', 'message': str(e)})
#
#     else:
#         form = ExcelUploadForm()
#
#     return render(request, 'dashboard/import_synthese.html', {'form': form})
def import_synthese_view(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)

        if form.is_valid():
            excel_file = request.FILES['file']

            try:
                df = pd.read_excel(excel_file, engine='openpyxl')
                data = df.to_dict(orient='records')

                # Prévisualisation des données
                preview_data = data[:5]  # On prend les 5 premières lignes pour la prévisualisation

                # Validation et sauvegarde des données
                errors = []
                for index, record in enumerate(data):
                    try:
                        centre_nom = record['CENTRES DE SANTÉ']

                        # Nettoyer et convertir les valeurs numériques
                        total_visite = int(record.get('TOTAL VISITE', 0))
                        total_recette = Decimal(str(record.get('TOTAL RECETTE', 0)).replace(' ', ''))
                        total_recouvrement = Decimal(str(record.get('TOTAL RECOUVREMENT', 0)).replace(' ', ''))
                        total_gratuite_ciblee = Decimal(str(record.get('TOTAL GRATUITÉ CIBLÉE', 0)).replace(' ', ''))
                        total_cas_sociaux = int(record.get('TOTAL CAS SOCIAUX', 0))
                        total_acte_reduit = Decimal(str(record.get('TOTAL ACTE RÉDUIS', 0)).replace(' ', ''))
                        total_cmu = Decimal(str(record.get('TOTAL CMU', 0)).replace(' ', ''))
                        total_hors_cmu = Decimal(str(record.get('TOTAL HORS CMU', 0)).replace(' ', ''))

                        date_str = record['DATE']
                        date = parse_date(str(date_str))
                        if not date:
                            errors.append(f"Format de date invalide pour {centre_nom} sur la ligne {index + 1}.")
                            continue

                        # Déterminer le type de centre de santé
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

                        # Obtenir ou créer une instance de TypeServiceSanitaire
                        type_service, created = TypeServiceSanitaire.objects.get_or_create(
                            nom=centre_type,
                            defaults={'acronyme': key}
                        )

                        # Recherche ou création du ServiceSanitaire
                        centre_sante, created = ServiceSanitaire.objects.get_or_create(
                            nom=centre_nom,
                            defaults={'type': type_service}
                        )

                        # Vérification si la synthèse existe déjà
                        if SyntheseActivites.objects.filter(centre_sante=centre_sante, date=date).exists():
                            errors.append(f"Données déjà existantes pour {centre_nom} à la date {date}. Ligne {index + 1} ignorée.")
                            continue

                        # Création de SyntheseActivites
                        SyntheseActivites.objects.create(
                            centre_sante=centre_sante,
                            date=date,
                            total_visite=total_visite,
                            total_recette=total_recette,
                            total_recouvrement=total_recouvrement,
                            total_gratuite_ciblee=total_gratuite_ciblee,
                            total_cas_sociaux=total_cas_sociaux,
                            total_acte_reduit=total_acte_reduit,
                            total_cmu=total_cmu,
                            total_hors_cmu=total_hors_cmu,
                        )
                    except KeyError as key_error:
                        errors.append(f"Colonne manquante : {key_error}. Ligne {index + 1} ignorée.")
                    except Exception as e:
                        errors.append(f"Erreur lors du traitement de la ligne {index + 1} : {str(e)}")

                if errors:
                    return JsonResponse({'status': 'partial_success', 'preview_data': preview_data, 'errors': errors})
                else:
                    return JsonResponse({'status': 'success', 'preview_data': preview_data})

            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})

    else:
        form = ExcelUploadForm()

    return render(request, 'dashboard/import_synthese.html', {'form': form})

@csrf_exempt
def confirm_import(request):
    if request.method == 'POST':
        try:
            # Logique pour confirmer l'importation
            # Par exemple, enregistrer les données en base de données
            return JsonResponse({'status': 'success', 'message': 'Importation confirmée avec succès!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})


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
            total_gratuite_ciblee=Sum('total_gratuite_ciblee'),
            total_cas_sociaux=Sum('total_cas_sociaux'),
            total_acte_reduit=Sum('total_acte_reduit'),
            total_hors_cmu=Sum('total_hors_cmu'),
        )
        .order_by('-total_visite', '-total_recette', '-total_recouvrement', '-total_cmu')[:10]
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
    # poles_totals = (
    #     PolesRegionaux.objects.prefetch_related(
    #         'healthregion_set__districtsanitaire_set__servicesanitaire_set__syntheseactivites_set'
    #     )
    #     .annotate(
    #         total_recette=Sum('healthregion__districtsanitaire__servicesanitaire__syntheseactivites__total_recette')
    #     )
    # )
    poles_totals = (
        PolesRegionaux.objects.prefetch_related(
            'healthregion_set',  # Précharger la relation avec HealthRegion
            'healthregion_set__districtsanitaire_set',  # Précharger les DistrictSanitaires de chaque HealthRegion
            'healthregion_set__districtsanitaire_set__servicesanitaire_set',  # Précharger les centres de santé
            'healthregion_set__districtsanitaire_set__servicesanitaire_set__syntheseactivites_set'
            # Précharger SyntheseActivites
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

            for service in district.servicesanitaire_set.all():
                service.total_recette = (
                    SyntheseActivites.objects.filter(
                        centre_sante=service
                    ).aggregate(total_recette=Sum('total_recette'))['total_recette']
                )

    return poles_totals


# class DashboardView(LoginRequiredMixin, TemplateView):
#     login_url = '/accounts/login/'
#     template_name = 'dashboard/index.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         filter_form = CombinedFilterForm(self.request.GET or None)
#         context['filter_form'] = filter_form
#
#         # Appliquer le filtre si sélectionné
#         synthese_data = SyntheseActivites.objects.all()
#
#         if filter_form.is_valid():
#             type_service = filter_form.cleaned_data.get('type_service')
#             if type_service:
#                 synthese_data = synthese_data.filter(centre_sante__type=type_service)
#             # Filtrage par année
#             year = filter_form.cleaned_data.get('year')
#             if year:
#                 synthese_data = synthese_data.filter(date__year=year)
#
#             # Filtrage par semestre
#             semester = filter_form.cleaned_data.get('semester')
#             if semester:
#                 if semester == '1':
#                     synthese_data = synthese_data.filter(date__month__in=[1, 2, 3, 4, 5, 6])
#                 else:
#                     synthese_data = synthese_data.filter(date__month__in=[7, 8, 9, 10, 11, 12])
#
#             # Filtrage par trimestre
#             trimester = filter_form.cleaned_data.get('trimester')
#             if trimester:
#                 if trimester == '1':
#                     synthese_data = synthese_data.filter(date__month__in=[1, 2, 3])
#                 elif trimester == '2':
#                     synthese_data = synthese_data.filter(date__month__in=[4, 5, 6])
#                 elif trimester == '3':
#                     synthese_data = synthese_data.filter(date__month__in=[7, 8, 9])
#                 elif trimester == '4':
#                     synthese_data = synthese_data.filter(date__month__in=[10, 11, 12])
#
#             # Filtrage par mois
#             month = filter_form.cleaned_data.get('month')
#             if month:
#                 synthese_data = synthese_data.filter(date__month=month)
#
#         # Données pour les graphiques
#         context['labels'] = [item.centre_sante.nom for item in synthese_data if item.centre_sante]
#         context['total_visite'] = [item.total_visite for item in synthese_data]
#         context['total_recette'] = [float(item.total_recette) for item in synthese_data]
#         context['total_cmu'] = [float(item.total_cmu) for item in synthese_data]
#         context['total_recouvrement'] = [float(item.total_recouvrement) for item in synthese_data]
#
#         context['poles'] = get_pole_totals_with_regions_and_districts()
#         context['top_districts'] = get_top_districts()
#         context['top_perform_districts_by_pole'] = self.get_top_perform_districts_by_pole()
#
#         return context
#
#     def get_top_perform_districts_by_pole(self):
#         # Dictionnaire pour stocker le district le plus performant par pôle
#         top_perform_districts = {}
#
#         # Récupérer tous les pôles régionaux
#         poles = PolesRegionaux.objects.all()
#
#         # Itérer sur chaque pôle régional
#         for pole in poles:
#             # Récupérer tous les districts associés au pôle régional
#             districts_in_pole = DistrictSanitaire.objects.filter(region__poles=pole)
#
#             # Calculer la performance des districts en fonction de la somme des recettes ou visites
#             best_district = (
#                 districts_in_pole
#                 .annotate(total_recette=Sum('servicesanitaire__syntheseactivites__total_recette'))
#                 .order_by('-total_recette')  # Trier par le total des recettes
#                 .first()
#             )
#
#             if best_district:
#                 # Ajouter au dictionnaire le pôle avec son district le plus performant
#                 top_perform_districts[pole] = best_district
#
#         return top_perform_districts
class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_form = CombinedFilterForm(self.request.GET or None)
        context['filter_form'] = filter_form

        # Appliquer le filtre si sélectionné
        synthese_data = SyntheseActivites.objects.all()

        # Filtrage par année
        selected_year = None
        if filter_form.is_valid():
            type_service = filter_form.cleaned_data.get('type_service')
            if type_service:
                synthese_data = synthese_data.filter(centre_sante__type=type_service)

            # Filtrage par année
            selected_year = filter_form.cleaned_data.get('year')
            if selected_year:
                synthese_data = synthese_data.filter(date__year=selected_year)

        # Obtenir les données mensuelles
        monthly_data = (
            synthese_data
            .filter(date__year=selected_year if selected_year else timezone.now().year)
            .annotate(month=ExtractMonth('date'))
            .values('month')
            .annotate(
                total_visite=Sum('total_visite'),
                total_recette=Sum('total_recette'),
                total_cmu=Sum('total_cmu'),
                total_recouvrement=Sum('total_recouvrement')
            )
            .order_by('month')
        )

        # Créer des listes pour chaque mois (janvier à décembre)
        months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre',
                  'Novembre', 'Décembre']
        monthly_visites = [0] * 12
        monthly_recettes = [0] * 12
        monthly_cmu = [0] * 12
        monthly_recouvrement = [0] * 12

        for data in monthly_data:
            month_index = data['month'] - 1  # Mois dans la base commence à 1 (janvier) donc soustraire 1 pour l'indice
            monthly_visites[month_index] = data['total_visite'] or 0
            monthly_recettes[month_index] = float(data['total_recette'] or 0)
            monthly_cmu[month_index] = float(data['total_cmu'] or 0)
            monthly_recouvrement[month_index] = float(data['total_recouvrement'] or 0)

        # Données pour les graphiques
        context['months'] = months
        context['monthly_visites'] = monthly_visites
        context['monthly_recettes'] = monthly_recettes
        context['monthly_cmu'] = monthly_cmu
        context['monthly_recouvrement'] = monthly_recouvrement

        context['poles'] = get_pole_totals_with_regions_and_districts()
        context['top_districts'] = get_top_districts()
        context['top_perform_districts_by_pole'] = self.get_top_perform_districts_by_pole()

        # Annoter chaque type de service sanitaire avec le nombre d'établissements qui lui sont associés
        services_by_type = TypeServiceSanitaire.objects.annotate(total_services=Count('servicesanitaire'))
        nmbreservices = ServiceSanitaire.objects.all().count()

        # Ajouter les données dans le contexte pour les afficher dans le template
        context['services_by_type'] = services_by_type
        context['nmbreservices'] = nmbreservices

        return context

    def get_top_perform_districts_by_pole(self):

        # Dictionnaire pour stocker le district le plus performant par pôle
        top_perform_districts = {}

        # Récupérer tous les pôles régionaux
        poles = PolesRegionaux.objects.all()

        # Itérer sur chaque pôle régional
        for pole in poles:
            # Récupérer tous les districts associés au pôle régional
            districts_in_pole = DistrictSanitaire.objects.filter(region__poles=pole)

            # Calculer la performance des districts en fonction de la somme des recettes ou visites
            best_district = (
                districts_in_pole
                .annotate(total_recette=Sum('servicesanitaire__syntheseactivites__total_recette'))
                .order_by('-total_recette')  # Trier par le total des recettes
                .first()
            )

            if best_district:
                # Ajouter au dictionnaire le pôle avec son district le plus performant
                top_perform_districts[pole] = best_district

        return top_perform_districts


class SyntheseActivitesView(ListView):
    model = SyntheseActivites
    context_object_name = 'synthese_data'
    template_name = 'dashboard/syntheseview.html'
    paginate_by = 10
    ordering = ['-total_recette']


class CartographyView(TemplateView):
    login_url = '/accounts/login/'
    template_name = 'dashboard/cartographie.html'
