from django.shortcuts import render, redirect, get_object_or_404
from .models import Location, FireIncident, FireStation, FireFighter, FireTruck, WeatherCondition
from django.contrib import messages
from decimal import Decimal

def index(request):
    return render(request, 'mainsite/index.html')

def dashboard_chart(request):
    return render(request, 'mainsite/dashboard_chart.html')

def map_station(request):
    stations = FireStation.objects.all()
    return render(request, 'map-station.html', {'stations': stations})  # Changed from mainsite/map_station.html

def map_incidents(request):
    incidents = FireIncident.objects.all()
    return render(request, 'map-incidents.html', {'incidents': incidents})  # Changed from mainsite/map_incidents.html

# Location views
def location_list(request):
    locations = Location.objects.all()
    return render(request, 'management/location_list.html', {'locations': locations})

def location_add(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        Location.objects.create(
            address=address,
            latitude=latitude,
            longitude=longitude
        )
        messages.success(request, 'Location added successfully!')
        return redirect('location-list')
    return render(request, 'management/location_form.html')

def location_edit(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        location.address = request.POST.get('address')
        location.latitude = request.POST.get('latitude')
        location.longitude = request.POST.get('longitude')
        location.save()
        messages.info(request, 'Location updated successfully!')
        return redirect('location-list')
    return render(request, 'management/location_form.html', {'location': location})

def location_delete(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        location.delete()
        messages.warning(request, 'Location deleted successfully!')
        return redirect('location-list')
    return render(request, 'management/location_confirm_delete.html', {'location': location})

# FireStation CRUD
def firestation_list(request):
    stations = FireStation.objects.all()
    return render(request, 'management/firestation_list.html', {'stations': stations})

def firestation_add(request):
    locations = Location.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        location_id = request.POST.get('location')
        contact_number = request.POST.get('contact_number')
        location = get_object_or_404(Location, pk=location_id)
        FireStation.objects.create(
            name=name,
            location=location,
            contact_number=contact_number
        )
        messages.success(request, 'Fire station added successfully!')
        return redirect('firestation-list')
    return render(request, 'management/firestation_form.html', {'locations': locations})

def firestation_edit(request, pk):
    station = get_object_or_404(FireStation, pk=pk)
    locations = Location.objects.all()
    if request.method == 'POST':
        station.name = request.POST.get('name')
        location_id = request.POST.get('location')
        station.contact_number = request.POST.get('contact_number')
        station.location = get_object_or_404(Location, pk=location_id)
        station.save()
        messages.info(request, 'Fire station updated successfully!')
        return redirect('firestation-list')
    return render(request, 'management/firestation_form.html', {'station': station, 'locations': locations})

def firestation_delete(request, pk):
    station = get_object_or_404(FireStation, pk=pk)
    if request.method == 'POST':
        station.delete()
        messages.warning(request, 'Fire station deleted successfully!')
        return redirect('firestation-list')
    return render(request, 'management/firestation_confirm_delete.html', {'station': station})

# FireFighter CRUD
def firefighter_list(request):
    firefighters = FireFighter.objects.all()
    return render(request, 'management/firefighter_list.html', {'firefighters': firefighters})

def firefighter_add(request):
    stations = FireStation.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        badge_number = request.POST.get('badge_number')
        station_id = request.POST.get('station')
        position = request.POST.get('position')
        station = get_object_or_404(FireStation, pk=station_id)
        FireFighter.objects.create(
            name=name,
            badge_number=badge_number,
            station=station,
            position=position
        )
        messages.success(request, 'Firefighter added successfully!')
        return redirect('firefighter-list')
    return render(request, 'management/firefighter_form.html', {'stations': stations})

def firefighter_edit(request, pk):
    firefighter = get_object_or_404(FireFighter, pk=pk)
    stations = FireStation.objects.all()
    if request.method == 'POST':
        firefighter.name = request.POST.get('name')
        firefighter.badge_number = request.POST.get('badge_number')
        station_id = request.POST.get('station')
        firefighter.position = request.POST.get('position')
        firefighter.station = get_object_or_404(FireStation, pk=station_id)
        firefighter.save()
        messages.info(request, 'Firefighter updated successfully!')
        return redirect('firefighter-list')
    return render(request, 'management/firefighter_form.html', {'firefighter': firefighter, 'stations': stations})

def firefighter_delete(request, pk):
    firefighter = get_object_or_404(FireFighter, pk=pk)
    if request.method == 'POST':
        firefighter.delete()
        messages.warning(request, 'Firefighter deleted successfully!')
        return redirect('firefighter-list')
    return render(request, 'management/firefighter_confirm_delete.html', {'firefighter': firefighter})

# FireTruck CRUD
def firetruck_list(request):
    firetrucks = FireTruck.objects.all()
    return render(request, 'management/firetruck_list.html', {'firetrucks': firetrucks})

def firetruck_add(request):
    stations = FireStation.objects.all()
    if request.method == 'POST':
        vehicle_number = request.POST.get('vehicle_number')
        type = request.POST.get('type')
        capacity = request.POST.get('capacity')
        station_id = request.POST.get('station')
        station = get_object_or_404(FireStation, pk=station_id)
        FireTruck.objects.create(
            vehicle_number=vehicle_number,
            type=type,
            capacity=capacity,
            station=station
        )
        messages.success(request, 'Fire truck added successfully!')
        return redirect('firetruck-list')
    return render(request, 'management/firetruck_form.html', {'stations': stations})

def firetruck_edit(request, pk):
    firetruck = get_object_or_404(FireTruck, pk=pk)
    stations = FireStation.objects.all()
    if request.method == 'POST':
        firetruck.vehicle_number = request.POST.get('vehicle_number')
        firetruck.type = request.POST.get('type')
        firetruck.capacity = request.POST.get('capacity')
        station_id = request.POST.get('station')
        firetruck.station = get_object_or_404(FireStation, pk=station_id)
        firetruck.save()
        messages.info(request, 'Fire truck updated successfully!')
        return redirect('firetruck-list')
    return render(request, 'management/firetruck_form.html', {'firetruck': firetruck, 'stations': stations})

def firetruck_delete(request, pk):
    firetruck = get_object_or_404(FireTruck, pk=pk)
    if request.method == 'POST':
        firetruck.delete()
        messages.warning(request, 'Fire truck deleted successfully!')
        return redirect('firetruck-list')
    return render(request, 'management/firetruck_confirm_delete.html', {'firetruck': firetruck})

# WeatherCondition CRUD
def weather_list(request):
    weather_conditions = WeatherCondition.objects.all().order_by('-date_recorded')
    return render(request, 'management/weather_list.html', {'weather_conditions': weather_conditions})

def weather_add(request):
    if request.method == 'POST':
        temperature = request.POST.get('temperature')
        humidity = request.POST.get('humidity')
        wind_speed = request.POST.get('wind_speed')
        WeatherCondition.objects.create(
            temperature=float(temperature),
            humidity=float(humidity),
            wind_speed=float(wind_speed)
        )
        messages.success(request, 'Weather condition added successfully!')
        return redirect('weather-list')
    return render(request, 'management/weather_form.html')

def weather_edit(request, pk):
    condition = get_object_or_404(WeatherCondition, pk=pk)
    if request.method == 'POST':
        condition.temperature = float(request.POST.get('temperature'))
        condition.humidity = float(request.POST.get('humidity'))
        condition.wind_speed = float(request.POST.get('wind_speed'))
        condition.save()
        messages.info(request, 'Weather condition updated successfully!')
        return redirect('weather-list')
    return render(request, 'management/weather_form.html', {'condition': condition})

def weather_delete(request, pk):
    condition = get_object_or_404(WeatherCondition, pk=pk)
    if request.method == 'POST':
        condition.delete()
        messages.warning(request, 'Weather condition deleted successfully!')
        return redirect('weather-list')
    return render(request, 'management/weather_confirm_delete.html', {'condition': condition})

# FireIncident CRUD
def incident_list(request):
    incidents = FireIncident.objects.all()
    return render(request, 'management/incident_list.html', {'incidents': incidents})

def incident_add(request):
    locations = Location.objects.all()
    if request.method == 'POST':
        description = request.POST.get('description')
        location_id = request.POST.get('location')
        location = get_object_or_404(Location, pk=location_id)
        FireIncident.objects.create(
            description=description,
            location=location
        )
        messages.success(request, 'Fire incident added successfully!')
        return redirect('incident-list')
    return render(request, 'management/incident_form.html', {'locations': locations})

def incident_edit(request, pk):
    incident = get_object_or_404(FireIncident, pk=pk)
    locations = Location.objects.all()
    if request.method == 'POST':
        incident.description = request.POST.get('description')
        location_id = request.POST.get('location')
        incident.location = get_object_or_404(Location, pk=location_id)
        incident.save()
        messages.info(request, 'Fire incident updated successfully!')
        return redirect('incident-list')
    return render(request, 'management/incident_form.html', {'incident': incident, 'locations': locations})

def incident_delete(request, pk):
    incident = get_object_or_404(FireIncident, pk=pk)
    if request.method == 'POST':
        incident.delete()
        messages.warning(request, 'Fire incident deleted successfully!')
        return redirect('incident-list')
    return render(request, 'management/incident_confirm_delete.html', {'incident': incident})