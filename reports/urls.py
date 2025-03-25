# reports/urls.py
from django.urls import path
from . import views  # Import views z reports
from django.contrib.auth.views import LogoutView # Importuj LogoutView

app_name = 'reports'

urlpatterns = [
    path('', views.index, name='index'),
    path('published/', views.PublishedReportListView.as_view(), name='published_report_list'),
    path('open/', views.OpenReportListView.as_view(), name='open_report_list'),
    path('<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('logout/', LogoutView.as_view(next_page='reports:index'), name='logout'), # Používám LogoutView správně
]