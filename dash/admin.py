from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from dash.forms import DistrictSanitaireForm, SyntheseActivitesForm
from dash.models import SyntheseActivites, HealthRegion, PolesRegionaux, ServiceSanitaire, DistrictSanitaire


# Register your models here.

@admin.register(SyntheseActivites)
class SyntheseDistrictAdmin(ImportExportModelAdmin):
    # resource_class = SyntheseDistrictResource
    # form = SyntheseActivitesForm
    search_fields = ['centre_sante__nom']
    list_display = ('centre_sante', 'total_visite', 'total_recette')


@admin.register(DistrictSanitaire)
class DistrictSanitaireAdmin(ImportExportModelAdmin):
    # resource_class = SyntheseDistrictResource
    # form = DistrictSanitaireForm
    list_display = ('nom', 'region')
    search_fields = ['nom', 'region__name']
    list_filter = ['region']


@admin.register(ServiceSanitaire)
class ServiceSanitaireDistrictAdmin(ImportExportModelAdmin):
    # resource_class = SyntheseDistrictResource
    list_display = ('nom', 'district')
    search_fields = ['nom', 'district__nom']
    list_filter = ['district__nom', 'nom']



@admin.register(PolesRegionaux)
class PolesRegionauxAdmin(ImportExportModelAdmin):
    # resource_class = SyntheseDistrictResource
    # form = DistrictSanitaireForm
    list_display = ('id', 'name')
    search_fields = ['name', 'id']
    # list_filter = ['region']

# admin.site.register(ServiceSanitaire)
# admin.site.register(DistrictSanitaire)


@admin.register(HealthRegion)
class HealthRegionDistrictAdmin(ImportExportModelAdmin):
    # resource_class = SyntheseDistrictResource
    list_display = ('name', 'poles')
