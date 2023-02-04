from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    history = HistoricalRecords()

class Device(models.Model):
    name = models.CharField(max_length=100,unique=True)
    type = models.CharField(max_length=25)
    history = HistoricalRecords()
    timestamp = models.DateTimeField(default=timezone.now)
    employee = models.ForeignKey(Employee, blank=True, null=True, on_delete=models.SET_NULL)
