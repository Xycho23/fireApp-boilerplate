from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from .models import FireIncident

class HomePageView(TemplateView):
    template_name = 'home.html'

class DashboardChartView(TemplateView):
    template_name = 'chart.html'

class MapIncidentsView(TemplateView):
    template_name = 'map-incidents.html'

def pie_chart(request):
    severity_counts = FireIncident.objects.values('severity_level').annotate(count=Count('id'))
    data = {item['severity_level']: item['count'] for item in severity_counts}
    return JsonResponse(data)

def line_chart(request):
    monthly_counts = FireIncident.objects.annotate(
        month=ExtractMonth('date_reported')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    data = {i: 0 for i in range(1, 13)}
    for item in monthly_counts:
        data[item['month']] = item['count']
    return JsonResponse(data)

def multiline_chart(request):
    monthly_counts = FireIncident.objects.annotate(
        month=ExtractMonth('date_reported')
    ).values('month', 'location').annotate(
        count=Count('id')
    ).order_by('month')
    
    data = {}
    for item in monthly_counts:
        if item['location'] not in data:
            data[item['location']] = {i: 0 for i in range(1, 13)}
        data[item['location']][item['month']] = item['count']
    return JsonResponse(data)

def multibar_chart(request):
    monthly_severity = FireIncident.objects.annotate(
        month=ExtractMonth('date_reported')
    ).values('month', 'severity_level').annotate(
        count=Count('id')
    ).order_by('month')
    
    data = {}
    for item in monthly_severity:
        if item['severity_level'] not in data:
            data[item['severity_level']] = {i: 0 for i in range(1, 13)}
        data[item['severity_level']][item['month']] = item['count']
    return JsonResponse(data)