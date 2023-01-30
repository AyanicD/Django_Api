from django.urls import path
from . import viewsets

urlpatterns = [
    path('create', viewsets.create_user, name='create-user'),
]