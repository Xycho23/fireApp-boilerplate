from django.db import models

class Location(models.Model):
    address = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.address

class FireStation(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class FireFighter(models.Model):
    name = models.CharField(max_length=100)
    badge_number = models.CharField(max_length=20)
    station = models.ForeignKey(FireStation, on_delete=models.CASCADE)
    position = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.badge_number}"

class FireTruck(models.Model):
    vehicle_number = models.CharField(max_length=20)
    type = models.CharField(max_length=50)
    capacity = models.IntegerField()
    station = models.ForeignKey(FireStation, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.type} - {self.vehicle_number}"

class WeatherCondition(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    date_recorded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Weather on {self.date_recorded}"

class FireIncident(models.Model):
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date_reported = models.DateTimeField(auto_now_add=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    description = models.TextField()
    weather_condition = models.ForeignKey(WeatherCondition, on_delete=models.SET_NULL, null=True)
    responding_station = models.ForeignKey(FireStation, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Fire at {self.location} - {self.date_reported}"
