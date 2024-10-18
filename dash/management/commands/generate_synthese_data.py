import random
from datetime import timedelta

from django.core.management import BaseCommand
from django.utils import timezone

from dash.models import ServiceSanitaire, SyntheseActivites


class Command(BaseCommand):
    help = 'Generate synthetic data for SyntheseActivites over the past 24 months'

    def handle(self, *args, **kwargs):
        # Get all ServiceSanitaire centers
        centres = ServiceSanitaire.objects.all()

        if not centres.exists():
            self.stdout.write(self.style.ERROR("No ServiceSanitaire found in the database."))
            return

        today = timezone.now().date()
        start_date = today - timedelta(days=730)  # Approximately 2 years ago (24 months)

        # Generate data for each month for the past 24 months
        current_date = start_date
        while current_date <= today:
            for centre in centres:
                total_visite = random.randint(50, 500)
                total_recette = round(random.uniform(500.0, 5000.0), 2)
                total_recouvrement = round(random.uniform(200.0, 3000.0), 2)
                total_gratuite_ciblee = round(random.uniform(50.0, 1000.0), 2)
                total_cas_sociaux = random.randint(5, 50)
                total_acte_reduit = round(random.uniform(20.0, 500.0), 2)
                total_cmu = round(random.uniform(100.0, 1000.0), 2)
                total_hors_cmu = round(random.uniform(100.0, 1000.0), 2)

                SyntheseActivites.objects.create(
                    centre_sante=centre,
                    total_visite=total_visite,
                    total_recette=total_recette,
                    total_recouvrement=total_recouvrement,
                    total_gratuite_ciblee=total_gratuite_ciblee,
                    total_cas_sociaux=total_cas_sociaux,
                    total_acte_reduit=total_acte_reduit,
                    total_cmu=total_cmu,
                    total_hors_cmu=total_hors_cmu,
                    date=current_date
                )

            # Move to the next month
            current_date += timedelta(days=30)

        self.stdout.write(self.style.SUCCESS('Successfully generated synthetic data for the past 24 months.'))