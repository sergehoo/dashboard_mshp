import csv
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry

from dash.models import HealthRegion, DistrictSanitaire


class Command(BaseCommand):
    help = 'Import districts from a CSV file into the DistrictSanitaire model.'

    def add_arguments(self, parser):
        # Add a command argument to specify the file path
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import.')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        self.stdout.write(self.style.NOTICE(f"Importing districts from {csv_file_path}"))

        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    # Get or create HealthRegion (if applicable)
                    region_name = row.get('region')  # Adjust column name based on CSV structure
                    region, created = HealthRegion.objects.get_or_create(name=region_name)

                    # Parse geometry if available
                    geom_wkt = row.get('geom')  # Assuming 'geom' column contains WKT data
                    geom = GEOSGeometry(geom_wkt, srid=4326) if geom_wkt else None

                    # Create or update DistrictSanitaire record
                    district, created = DistrictSanitaire.objects.update_or_create(
                        nom=row.get('nom'),  # Adjust based on the actual CSV column names
                        defaults={
                            'region': region,
                            'geom': geom,
                        }
                    )

                    self.stdout.write(self.style.SUCCESS(f"Imported district: {district.nom}"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {csv_file_path} not found"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
