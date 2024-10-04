from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from dash.forms import DistrictSanitaireForm, SyntheseActivitesForm
from dash.models import SyntheseActivites, HealthRegion, PolesRegionaux, ServiceSanitaire, DistrictSanitaire


# Register your models here.

@admin.register(SyntheseActivites)
class SyntheseDistrictAdmin(ImportExportModelAdmin):
    # resource_class = SyntheseDistrictResource
    # form = SyntheseActivitesForm
    list_display = ('centre_sante', 'total_visite')


@admin.register(DistrictSanitaire)
class DistrictSanitaireAdmin(ImportExportModelAdmin):
    # resource_class = SyntheseDistrictResource
    form = DistrictSanitaireForm
    list_display = ('nom', 'region')
    search_fields = ['nom', 'region__nom']
    list_filter = ['region']


@admin.register(ServiceSanitaire)
class ServiceSanitaireDistrictAdmin(ImportExportModelAdmin):
    # resource_class = SyntheseDistrictResource
    list_display = ('nom', 'district')
    search_fields = ['nom', 'district__nom']
    list_filter = ['district__nom', 'nom']


admin.site.register(PolesRegionaux)


# admin.site.register(ServiceSanitaire)
# admin.site.register(DistrictSanitaire)


@admin.register(HealthRegion)
class HealthRegionDistrictAdmin(ImportExportModelAdmin):
    # resource_class = SyntheseDistrictResource
    list_display = ('name', 'poles')
