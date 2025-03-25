from django.urls import path
from reports import views

app_name = 'reports'

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('published/', views.PublishedReportListView.as_view(), name='published_report_list'),
    path('open/', views.OpenReportListView.as_view(), name='open_report_list'),
    
]


