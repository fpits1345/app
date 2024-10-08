from django.urls import path

from core.reports.views import ReportPosteView

urlpatterns = [
    # reports
    path('postes/', ReportPosteView.as_view(), name='postes_report'),
]