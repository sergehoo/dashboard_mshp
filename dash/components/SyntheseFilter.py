from django_unicorn.components import UnicornView

from dash.forms import FilterForm
from dash.models import DistrictSanitaire, HealthRegion, SyntheseActivites


# class SyntheseFilterView(UnicornView):
#     # Filters for date and location
#     date_filter_type = ""
#     selected_month = ""
#     selected_year = ""
#     selected_quarter = ""
#     selected_semester = ""
#     selected_district = ""
#     selected_region = ""
#
#     # Data for dropdowns
#     districts = DistrictSanitaire.objects.all()
#     regions = HealthRegion.objects.all()
#
#     # Default list for the filtered results
#     filtered_data = []
#
#     def mount(self):
#         # Load initial data on mount
#         self.filter_data()
#
#     def filter_data(self):
#         queryset = SyntheseActivites.objects.all()
#
#         # Date filtering logic
#         if self.date_filter_type == "month":
#             if self.selected_year and self.selected_month:
#                 queryset = queryset.filter(date__year=self.selected_year, date__month=self.selected_month)
#
#         elif self.date_filter_type == "quarter":
#             if self.selected_year and self.selected_quarter:
#                 start_month = (int(self.selected_quarter) - 1) * 3 + 1
#                 end_month = start_month + 2
#                 queryset = queryset.filter(date__year=self.selected_year, date__month__gte=start_month,
#                                            date__month__lte=end_month)
#
#         elif self.date_filter_type == "semester":
#             if self.selected_year and self.selected_semester:
#                 if self.selected_semester == "1":
#                     queryset = queryset.filter(date__year=self.selected_year, date__month__gte=1, date__month__lte=6)
#                 else:
#                     queryset = queryset.filter(date__year=self.selected_year, date__month__gte=7, date__month__lte=12)
#
#         elif self.date_filter_type == "year":
#             if self.selected_year:
#                 queryset = queryset.filter(date__year=self.selected_year)
#
#         # District and Region filtering logic
#         if self.selected_district:
#             queryset = queryset.filter(centre_sante__district__id=self.selected_district)
#
#         if self.selected_region:
#             queryset = queryset.filter(centre_sante__district__region__id=self.selected_region)
#
#         # Store the filtered queryset
#         self.filtered_data = queryset
#
#     def reset_filters(self):
#         # Reset all filters
#         self.date_filter_type = ""
#         self.selected_month = ""
#         self.selected_year = ""
#         self.selected_quarter = ""
#         self.selected_semester = ""
#         self.selected_district = ""
#         self.selected_region = ""
#         self.filter_data()


