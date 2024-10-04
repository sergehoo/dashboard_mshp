"""
URL configuration for dashboard_mshp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from dash.views import DashboardView, SyntheseActivitesView, import_synthese_view, preview_import_view, \
    confirm_import_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    # path("accounts/", include("allauth.socialaccount.urls")),
    path("unicorn/", include("django_unicorn.urls")),
    path("dash", include("dash.api.urls")),
    path('', DashboardView.as_view(), name='dashboard'),
    path('synthesedddd/Liste', SyntheseActivitesView.as_view(), name='syntheselist'),
    path('import-synthese/', import_synthese_view, name='import_synthese'),
    path('import-synthese/', preview_import_view, name='preview_import'),
    path('import-synthese/confirm/', confirm_import_view, name='confirm_import'),
    # path('synthese-activites/', SyntheseActivitesListView.as_view(), name='synthese_activites'),

]
