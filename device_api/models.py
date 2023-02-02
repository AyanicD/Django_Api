from django.db import models
from django.utils import timezone

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

class Device(models.Model):
    name = models.CharField(max_length=100,unique=True)
    type = models.CharField(max_length=25)
    history = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    employee = models.ForeignKey(Employee, blank=True, null=True, on_delete=models.SET_NULL)
