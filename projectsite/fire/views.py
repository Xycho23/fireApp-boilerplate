from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from fire.models import Locations, Incident, FireStation
import logging

logger = logging.getLogger(__name__)

class HomePageView(ListView):
    model = Locations
    context_object_name = 'home'
    template_name = "home.html"

class DashboardChartView(TemplateView):
    template_name = 'chart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add FireStation data to context for debugging
        stations = FireStation.objects.all()
        logger.debug(f"FireStations loaded: {stations.count()}")
        context['stations'] = stations
        return context

class MapStationView(ListView):
    model = FireStation
    template_name = 'map-station.html'
    context_object_name = 'stations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stations'] = FireStation.objects.all()
        return context

class MapIncidentsView(ListView):
    model = Incident
    template_name = 'map-incidents.html'
    context_object_name = 'incidents'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['incidents'] = Incident.objects.all()
        return context

def pie_chart(request):
    try:
        severity_levels = ['Minor Fire', 'Moderate Fire', 'Major Fire']
        severity_counts = Incident.objects.values('severity_level').annotate(count=Count('id'))
        
        logger.debug(f"Severity counts: {list(severity_counts)}")
        
        data = {
            'labels': severity_levels,
            'datasets': [{
                'data': [0] * len(severity_levels),
                'backgroundColor': ['#1d7af3', '#f3545d', '#fdaf4b'],
                'borderWidth': 1
            }]
        }
        
        for item in severity_counts:
            if item['severity_level'] in severity_levels:
                idx = severity_levels.index(item['severity_level'])
                data['datasets'][0]['data'][idx] = item['count']
        
        logger.debug(f"Pie chart data: {data}")
        return JsonResponse(data)
    except Exception as e:
        logger.error(f"Error in pie_chart: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

def doughnut_chart(request):
    severity_levels = ['Minor Fire', 'Moderate Fire', 'Major Fire']
    severity_counts = Incident.objects.values('severity_level').annotate(count=Count('id')).order_by('severity_level')
    
    data = {
        'labels': severity_levels,
        'datasets': [{
            'data': [0] * len(severity_levels),
            'backgroundColor': ['#f3545d', '#fdaf4b', '#1d7af3'],
            'borderWidth': 1,
            'cutout': '60%'
        }]
    }
    
    print("Severity Counts:", list(severity_counts))  # Debug print
    
    for item in severity_counts:
        if item['severity_level'] in severity_levels:
            idx = severity_levels.index(item['severity_level'])
            data['datasets'][0]['data'][idx] = item['count']
    
    print("Final Data:", data)  # Debug print
    return JsonResponse(data)

def line_chart(request):
    monthly_counts = Incident.objects.annotate(
        month=ExtractMonth('date_time')  # Changed from date_reported to date_time
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    data = {i: 0 for i in range(1, 13)}
    for item in monthly_counts:
        data[item['month']] = item['count']
    return JsonResponse(data)

def multiline_chart(request):
    monthly_counts = Incident.objects.annotate(
        month=ExtractMonth('date_time')  # Changed from date_reported to date_time
    ).values('month', 'location__name').annotate(  # Added __name to get location name
        count=Count('id')
    ).order_by('month')
    
    data = {}
    for item in monthly_counts:
        location_name = item['location__name']
        if location_name not in data:
            data[location_name] = {i: 0 for i in range(1, 13)}
        data[location_name][item['month']] = item['count']
    return JsonResponse(data)

def multibar_chart(request):
    severity_levels = ['Minor Fire', 'Moderate Fire', 'Major Fire']
    monthly_severity = (
        Incident.objects
        .annotate(month=ExtractMonth('date_time'))
        .values('month', 'severity_level')
        .annotate(count=Count('id'))
        .order_by('month', 'severity_level')
    )
    
    # Initialize data structure
    data = {level: {i: 0 for i in range(1, 13)} for level in severity_levels}
    
    # Fill in actual counts
    for item in monthly_severity:
        severity = item['severity_level']
        month = item['month']
        if severity in data:
            data[severity][month] = item['count']
    
    return JsonResponse(data)
