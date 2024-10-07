from django.urls import include, path
from rest_framework.routers import DefaultRouter

from dash.api.views import DistrictSanitaireViewSet, ServiceSanitaireViewSet, SyntheseActivitesViewSet, \
    HealthRegionViewSet

router = DefaultRouter()
router.register(r'regions', HealthRegionViewSet)
router.register(r'districts', DistrictSanitaireViewSet)
router.register(r'services', ServiceSanitaireViewSet)
router.register(r'synthese', SyntheseActivitesViewSet)

urlpatterns = [
    path('/api/', include(router.urls)),
]