# resources.py
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from epidemie.models import Echantillon, Epidemie, DistrictSanitaire, SyntheseDistrict


class SyntheseDistrictResource(resources.ModelResource):
    maladie = fields.Field(
        column_name='maladie',
        attribute='maladie',
        widget=ForeignKeyWidget(Epidemie, 'id')  # or use another field like 'nom' if necessary
    )

    district_sanitaire = fields.Field(
        column_name='district_sanitaire',
        attribute='district_sanitaire',
        widget=ForeignKeyWidget(DistrictSanitaire, 'nom')  # assuming the district names match
    )

    class Meta:
        model = SyntheseDistrict
        import_id_fields = ['id']
        fields = (
            'id', 'maladie', 'district_sanitaire', 'nbre_cas_suspects', 'cas_positif', 'cas_negatif', 'evacue', 'decede',
            'gueri', 'suivi_en_cours', 'nbre_sujets_contacts', 'contacts_en_cours_suivi', 'contacts_sorti_suivi',
            'devenu_suspect', 'devenu_positif'
        )