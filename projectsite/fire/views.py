from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from fire.models import Locations, Incident, FireStation

class HomePageView(ListView):
    model = Locations
    context_object_name = 'home'
    template_name = "home.html"

class DashboardChartView(TemplateView):
    template_name = 'chart.html'

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
    severity_levels = ['Minor Fire', 'Moderate Fire', 'Major Fire']
    severity_counts = Incident.objects.values('severity_level').annotate(count=Count('id'))
    
    # Initialize with zeros
    data = {
        'labels': severity_levels,
        'datasets': [{
            'data': [0] * len(severity_levels),
            'backgroundColor': ['#1d7af3', '#f3545d', '#fdaf4b']
        }]
    }
    
    # Fill in actual counts
    for item in severity_counts:
        if item['severity_level'] in severity_levels:
            idx = severity_levels.index(item['severity_level'])
            data['datasets'][0]['data'][idx] = item['count']
    
    return JsonResponse(data)

def doughnut_chart(request):
    severity_levels = ['Minor Fire', 'Moderate Fire', 'Major Fire']
    severity_counts = Incident.objects.values('severity_level').annotate(count=Count('id'))
    
    # Initialize with zeros
    data = {
        'labels': severity_levels,
        'datasets': [{
            'data': [0] * len(severity_levels),
            'backgroundColor': ['#f3545d', '#fdaf4b', '#1d7af3']
        }]
    }
    
    # Fill in actual counts
    for item in severity_counts:
        if item['severity_level'] in severity_levels:
            idx = severity_levels.index(item['severity_level'])
            data['datasets'][0]['data'][idx] = item['count']
    
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
