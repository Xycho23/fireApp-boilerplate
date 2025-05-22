from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard_chart, name='dashboard-chart'),
    
    # Maps
    path('maps/stations/', views.map_station, name='map-station'),
    path('maps/incidents/', views.map_incidents, name='map-incidents'),
    
    # Location Management
    path('locations/', views.location_list, name='location-list'),
    path('locations/add/', views.location_add, name='location-add'),
    path('locations/<int:pk>/edit/', views.location_edit, name='location-edit'),
    path('locations/<int:pk>/delete/', views.location_delete, name='location-delete'),
    
    # Fire Incident Management
    path('incidents/', views.incident_list, name='incident-list'),
    path('incidents/add/', views.incident_add, name='incident-add'),
    path('incidents/<int:pk>/edit/', views.incident_edit, name='incident-edit'),
    path('incidents/<int:pk>/delete/', views.incident_delete, name='incident-delete'),
    
    # Fire Station Management
    path('firestations/', views.firestation_list, name='firestation-list'),
    path('firestations/add/', views.firestation_add, name='firestation-add'),
    path('firestations/<int:pk>/edit/', views.firestation_edit, name='firestation-edit'),
    path('firestations/<int:pk>/delete/', views.firestation_delete, name='firestation-delete'),
    
    # Firefighter Management
    path('firefighters/', views.firefighter_list, name='firefighter-list'),
    path('firefighters/add/', views.firefighter_add, name='firefighter-add'),
    path('firefighters/<int:pk>/edit/', views.firefighter_edit, name='firefighter-edit'),
    path('firefighters/<int:pk>/delete/', views.firefighter_delete, name='firefighter-delete'),
    
    # Fire Truck Management
    path('firetrucks/', views.firetruck_list, name='firetruck-list'),
    path('firetrucks/add/', views.firetruck_add, name='firetruck-add'),
    path('firetrucks/<int:pk>/edit/', views.firetruck_edit, name='firetruck-edit'),
    path('firetrucks/<int:pk>/delete/', views.firetruck_delete, name='firetruck-delete'),
    
    # Weather Condition Management
    path('weather/', views.weather_list, name='weather-list'),
    path('weather/add/', views.weather_add, name='weather-add'),
    path('weather/<int:pk>/edit/', views.weather_edit, name='weather-edit'),
    path('weather/<int:pk>/delete/', views.weather_delete, name='weather-delete'),
]