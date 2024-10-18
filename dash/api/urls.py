from django.urls import include, path
from rest_framework.routers import DefaultRouter

from dash.api.views import DistrictSanitaireViewSet, ServiceSanitaireViewSet, SyntheseActivitesViewSet, \
    HealthRegionViewSet, ChartDataViewSet, TypeServiceViewSet

router = DefaultRouter()
router.register(r'regions', HealthRegionViewSet)
router.register(r'districts', DistrictSanitaireViewSet)
router.register(r'services', ServiceSanitaireViewSet)
router.register(r'synthese', SyntheseActivitesViewSet)
router.register(r'chart-data', ChartDataViewSet, basename='chart-data')
router.register(r'type-services', TypeServiceViewSet, basename='type-services')

urlpatterns = [
    path('/api/', include(router.urls)),
]