from django.urls import path

from core.reports.views import ReportPosteView

urlpatterns = [
    # reports
    path('postes/', ReportPosteView.as_view(), name='postes_report'),
    path('postes/report/pdf/', ReportPosteView.as_view(), name='postes_report_pdf'),
]