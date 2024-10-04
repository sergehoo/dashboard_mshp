import pandas as pd
from django.core.management.base import BaseCommand
from geopy.geocoders import Nominatim
from dash.models import DistrictSanitaire, ServiceSanitaire


# class Command(BaseCommand):
#     help = 'Importe les centres de santé depuis un fichier Excel et les géocode'
#
#     # Fonction pour remplacer les acronymes par leurs équivalents
#     def expand_acronyms(self, nom_centre):
#         acronyms = {
#             'CHR': 'Centre de Santé Régional',
#             'CHU': 'Centre de Santé Universitaire',
#             'HG': 'Hopital Général',
#             'CSR': 'Centre de Santé Régional',
#             'CSU': 'Centre de Sante Urbain'
#         }
#         # Remplacer chaque acronyme dans le nom du centre
#         for acronym, full_name in acronyms.items():
#             nom_centre = nom_centre.replace(acronym, full_name)
#         return nom_centre
#
#     def handle(self, *args, **kwargs):
#         file_path = 'static/centre_sante.xlsx'  # Chemin vers le fichier Excel
#         data = pd.read_excel(file_path, sheet_name='Feuil1')
#
#         # Utiliser Nominatim pour géocoder
#         geolocator = Nominatim(user_agent="geoapiExercises")
#
#         def geocode_location(nom_centre):
#             try:
#                 location = geolocator.geocode(nom_centre + ", Côte d'Ivoire")
#                 if location:
#                     return (location.latitude, location.longitude)
#                 return None
#             except Exception as e:
#                 self.stdout.write(self.style.ERROR(f"Erreur lors du géocodage de {nom_centre}: {e}"))
#                 return None
#
#         # Boucler sur les centres de santé pour les ajouter à la base de données
#         for index, row in data.iterrows():
#             nom_centre = row['CENTRES DE SANTÉ']
#
#             # Remplacer les acronymes avant de faire le géocodage
#             nom_centre_expanded = self.expand_acronyms(nom_centre)
#
#             # Géocoder l'adresse
#             coords = geocode_location(nom_centre_expanded)
#
#             if coords:
#                 latitude, longitude = coords
#                 geom_point = f"POINT({longitude} {latitude})"
#
#                 # Chercher un district correspondant (à adapter si nécessaire)
#                 district_name = "Nom du district"  # Vous pouvez ajuster cette partie si des districts existent
#                 district, created = DistrictSanitaire.objects.get_or_create(nom=district_name)
#
#                 # Créer le ServiceSanitaire et l'enregistrer dans la base de données
#                 ServiceSanitaire.objects.create(
#                     nom=nom_centre,
#                     geom=geom_point,
#                     district=district,  # Associer le district si pertinent
#                     completeness="partiel",  # À ajuster selon vos besoins
#                     version=1  # Exemple de version initiale
#                 )
#
#                 self.stdout.write(self.style.SUCCESS(f"Centre {nom_centre} ajouté avec succès!"))
#             else:
#                 self.stdout.write(self.style.WARNING(f"Coordonnées introuvables pour {nom_centre}."))

class Command(BaseCommand):
    help = 'Importe les centres de santé depuis un fichier Excel et les géocode'

    # Fonction pour remplacer les acronymes par leurs équivalents
    def expand_acronyms(self, nom_centre):
        acronyms = {
            'CHR': 'Centre de Santé Régional',
            'CHU': 'Centre de Santé Universitaire',
            'HG': 'Hopital Général',
            'CSR': 'Centre de Santé Régional',
            'CSU': 'Centre de Sante Urbain'
        }
        # Remplacer chaque acronyme dans le nom du centre
        for acronym, full_name in acronyms.items():
            nom_centre = nom_centre.replace(acronym, full_name)
        return nom_centre

    def handle(self, *args, **kwargs):
        file_path = 'static/centre_sante.xlsx'  # Chemin vers le fichier Excel
        data = pd.read_excel(file_path, sheet_name='Feuil1')

        # Utiliser Nominatim pour géocoder
        geolocator = Nominatim(user_agent="geoapiExercises")

        def geocode_location(nom_centre):
            try:
                location = geolocator.geocode(nom_centre + ", Côte d'Ivoire")
                if location:
                    return (location.latitude, location.longitude)
                return None
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erreur lors du géocodage de {nom_centre}: {e}"))
                return None

        # Boucler sur les centres de santé pour les ajouter à la base de données
        for index, row in data.iterrows():
            nom_centre = row['CENTRES DE SANTÉ']

            # Remplacer les acronymes avant de faire le géocodage
            nom_centre_expanded = self.expand_acronyms(nom_centre)

            # Géocoder l'adresse
            coords = geocode_location(nom_centre_expanded)

            # Si le géocodage a fonctionné, définir le geom
            if coords:
                latitude, longitude = coords
                geom_point = f"POINT({longitude} {latitude})"
            else:
                geom_point = None  # Si pas de coordonnées trouvées, laisser geom à None

            # Chercher un district correspondant (vous pouvez ajuster cette partie si nécessaire)
            district_name = "Nom du district"  # Remplacez par la logique de récupération du nom de district
            district, created = DistrictSanitaire.objects.get_or_create(nom=district_name)

            # Vérifier si le centre existe déjà
            existing_service = ServiceSanitaire.objects.filter(nom=nom_centre, district=district).first()

            if existing_service:
                # Si le service existe, mettre à jour ses coordonnées
                existing_service.geom = geom_point  # Mettre à jour geom
                existing_service.completeness = "partiel"  # Ajustez si nécessaire
                existing_service.save()
                self.stdout.write(self.style.WARNING(f"Centre {nom_centre} mis à jour avec succès!"))
            else:
                # Créer le ServiceSanitaire et l'enregistrer dans la base de données
                ServiceSanitaire.objects.create(
                    nom=nom_centre,
                    geom=geom_point,  # Peut être None si géocodage échoué
                    district=district,  # Associer le district si pertinent
                    completeness="partiel",  # À ajuster selon vos besoins
                    version=1  # Exemple de version initiale
                )
                self.stdout.write(self.style.SUCCESS(f"Centre {nom_centre} ajouté avec succès!"))