from django.contrib import admin
from .models import Location, FireStation, FireFighter, FireTruck, WeatherCondition, FireIncident

admin.site.register(Location)
admin.site.register(FireStation)
admin.site.register(FireFighter)
admin.site.register(FireTruck)
admin.site.register(WeatherCondition)
admin.site.register(FireIncident)
