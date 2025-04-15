from django.contrib import admin
from django.urls import path

from fire.views import HomePageView
from fire import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('dashboard-chart/', views.DashboardChartView.as_view(), name='dashboard-chart'),
    path('pie-chart/', views.pie_chart, name='pie-chart'),
    path('line-chart/', views.line_chart, name='line-chart'),
    path('multiline-chart/', views.multiline_chart, name='multiline-chart'),
    path('multibar-chart/', views.multibar_chart, name='multibar-chart'),
    path('map-station/', views.MapStationView.as_view(), name='map-station'),
    path('map-incidents/', views.MapIncidentsView.as_view(), name='map-incidents'),
    path('doughnut-chart/', views.doughnut_chart, name='doughnut-chart'),
]
