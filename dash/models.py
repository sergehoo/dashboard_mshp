import datetime
import random
import string
import uuid

from django.contrib.auth.models import User

from django.utils.timezone import now
from simple_history.models import HistoricalRecords
from django.contrib.gis.db import models
from django.db.models import Sum

# Create your models here.
Sexe_choices = [
    ('Homme', 'Homme'),
    ('Femme', 'Femme'),

]
Resultat_choices = [
    ('POSITIF', 'POSITIF'),
    ('NEGATIF', 'NEGATIF'),

]
situation_matrimoniales_choices = [
    ('Celibataire', 'Celibataire'),
    ('Concubinage', 'Concubinage'),
    ('Marie', 'Marié'),
    ('Divorce', 'Divorcé'),
    ('Veuf', 'Veuf'),
    ('Autre', 'Autre'),
]
Goupe_sanguin_choices = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
]
Patient_statut_choices = [
    ('Admis', 'Admis'),
    ('Sorti', 'Sorti'),
    ('Transféré', 'Transféré'),
    ('Décédé', 'Décédé'),
    ('Sous observation', 'Sous observation'),
    ('Sous traitement', 'Sous traitement'),
    ('Chirurgie programmée', 'Chirurgie programmée'),
    ('En chirurgie', 'En chirurgie'),
    ('Récupération post-opératoire', 'Récupération post-opératoire'),
    ('USI', 'Unité de soins intensifs (USI)'),
    ('Urgence', 'Urgence'),
    ('Consultation externe', 'Consultation externe'),
    ('Réhabilitation', 'Réhabilitation'),
    ('En attente de diagnostic', 'En attente de diagnostic'),
    ('Traitement en cours', 'Traitement en cours'),
    ('Suivi programmé', 'Suivi programmé'),
    ('Consultation', 'Consultation'),
    ('Sortie en attente', 'Sortie en attente'),
    ('Isolement', 'Isolement'),
    ('Ambulantoire', 'Ambulantoire'),
    ('Aucun', 'Aucun')
]


class PolesRegionaux(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name if self.name else "Unnamed Pole"


class HealthRegion(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    poles = models.ForeignKey(PolesRegionaux, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Region"


class DistrictSanitaire(models.Model):
    nom = models.CharField(max_length=100, null=True, blank=True, )
    region = models.ForeignKey(HealthRegion, on_delete=models.CASCADE, null=True, blank=True, )
    geom = models.PointField(null=True, blank=True, )
    geojson = models.JSONField(null=True, blank=True, )
    previous_rank = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.nom}---->{self.region}'


class TypeServiceSanitaire(models.Model):
    nom = models.CharField(max_length=500, null=True, blank=True)
    acronyme = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.acronyme}"


class ServiceSanitaire(models.Model):
    nom = models.CharField(max_length=100, null=True, blank=True)
    type = models.ForeignKey(TypeServiceSanitaire, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(DistrictSanitaire, on_delete=models.CASCADE, null=True, blank=True, )
    geom = models.PointField(srid=4326, null=True, blank=True)
    upstream = models.CharField(max_length=255, null=True, blank=True)
    date_modified = models.DateTimeField(null=True, blank=True)
    source_url = models.URLField(max_length=500, null=True, blank=True)
    completeness = models.CharField(max_length=100, null=True, blank=True)
    uuid = models.UUIDField(null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True)
    what3words = models.CharField(max_length=255, null=True, blank=True)
    version = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.nom}- {self.district} {self.geom}"


class SyntheseActivites(models.Model):
    centre_sante = models.ForeignKey(ServiceSanitaire, on_delete=models.SET_NULL, null=True, blank=True)
    total_visite = models.IntegerField(null=True, blank=True, verbose_name="Total Visite")
    total_recette = models.DecimalField(max_digits=22, decimal_places=2, null=True, blank=True, verbose_name="Total Recette")
    total_recouvrement = models.DecimalField(max_digits=22, decimal_places=2, null=True, blank=True,verbose_name="Total Recouvrement")
    total_gratuite_ciblee = models.DecimalField(max_digits=22, decimal_places=2, null=True, blank=True,verbose_name="Total Gratuité Ciblée")
    total_cas_sociaux = models.IntegerField(null=True, blank=True, verbose_name="Total Cas Sociaux")
    total_acte_reduit = models.DecimalField(max_digits=22, decimal_places=2, null=True, blank=True,verbose_name="Total Acte Réduit")
    total_cmu = models.DecimalField(max_digits=22, decimal_places=2, null=True, blank=True,verbose_name="Total CMU")
    total_hors_cmu = models.DecimalField(max_digits=22, decimal_places=2, null=True, blank=True,verbose_name="Total Hors CMU")
    date = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    deleted_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.centre_sante} - {self.date}"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee", )
    gender = models.CharField(choices=Sexe_choices, max_length=100, null=True, blank=True, )
    situation_matrimoniale = models.CharField(choices=situation_matrimoniales_choices, max_length=100, null=True,
                                              blank=True, )
    phone = models.CharField(null=True, blank=True, max_length=20, default='+22507070707')
    birthdate = models.DateField(null=True, blank=True)
    # dpt = models.ForeignKey('Service', on_delete=models.CASCADE, verbose_name="service", blank=True, null=True)
    district = models.ForeignKey('DistrictSanitaire', on_delete=models.CASCADE, verbose_name="District Sanitaire",
                                 blank=True, null=True)
    service = models.ForeignKey('ServiceSanitaire', on_delete=models.CASCADE, verbose_name="Service Sanitaire",
                                blank=True, null=True)
    job_title = models.CharField(null=True, blank=True, max_length=50, verbose_name="Titre du poste")

    slug = models.SlugField(null=True, blank=True, help_text="slug field", verbose_name="slug ", unique=True,
                            editable=False)

    # role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='District')
    created_at = models.DateTimeField(auto_now_add=now, )

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.user.username}- {self.user.first_name} {self.user.last_name}"

    class Meta:
        permissions = (
            ("access_all", "access all"),
            ("access_region", "access region"),
            ("access_district", "access district"),
            # ("can_view_district", "Can view district"),
            # ("can_view_region", "Can view region"),
            # ("can_view_national", "Can view national"),
            # ("can_edit_employee", "Can edit employee details"),
            # ("can_delete_employee", "Can delete employee"),
            ("can_assign_roles", "Can assign roles to employees"),
        )


class Patient(models.Model):
    code_patient = models.CharField(max_length=225, blank=True, unique=True, editable=False)
    nom = models.CharField(max_length=225, blank=True)
    prenoms = models.CharField(max_length=225, blank=True)
    contact = models.CharField(max_length=225, blank=True)
    situation_matrimoniale = models.CharField(max_length=225, choices=situation_matrimoniales_choices, blank=True)
    lieu_naissance = models.CharField(max_length=200, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    genre = models.CharField(max_length=10, choices=Sexe_choices, blank=True, )
    nationalite = models.CharField(max_length=200, blank=True, )
    profession = models.CharField(max_length=200, null=True, blank=True)
    nbr_enfants = models.PositiveIntegerField(default=0, blank=True)
    groupe_sanguin = models.CharField(choices=Goupe_sanguin_choices, max_length=20, blank=True, null=True)
    niveau_etude = models.CharField(max_length=500, null=True, blank=True)
    employeur = models.CharField(max_length=500, null=True, blank=True)
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=now)
    # commune = models.ForeignKey(Commune, on_delete=models.SET_NULL, null=True, blank=True)
    hopital = models.ForeignKey(ServiceSanitaire, on_delete=models.SET_NULL, null=True, blank=True)
    quartier = models.CharField(max_length=500, null=True, blank=True)
    # ville = models.ForeignKey('City', on_delete=models.SET_NULL, null=True)
    status = models.CharField(choices=Patient_statut_choices, max_length=100, default='Aucun', null=True, blank=True)
    gueris = models.BooleanField(default=False)
    decede = models.BooleanField(default=False)
    cascontact = models.ManyToManyField('self', blank=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['-created_at']
        permissions = (('voir_patient', 'Peut voir patient'),)

    def save(self, *args, **kwargs):
        # Générer un code_patient unique constitué de chiffres et de caractères alphabétiques
        if not self.code_patient:
            # Générer 16 chiffres à partir de l'UUID
            digits = ''.join(filter(str.isdigit, str(uuid.uuid4().int)))[:8]
            # Générer 4 caractères alphabétiques aléatoires
            letters = ''.join(random.choices(string.ascii_uppercase, k=4))
            # Combiner les chiffres et les lettres pour former le code_patient
            self.code_patient = digits + letters

        super(Patient, self).save(*args, **kwargs)

    @property
    def calculate_age(self):
        if self.date_naissance:
            today = datetime.date.today()
            age = today.year - self.date_naissance.year - (
                    (today.month, today.day) < (self.date_naissance.month, self.date_naissance.day))
            return age
        else:
            return None

    @property
    def latest_constante(self):
        return self.constantes.order_by('-created_at').first()

    def __str__(self):
        return f'{self.prenoms} {self.nom} -- {self.commune}--{self.genre}'
