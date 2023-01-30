from device_api.serializers import (
    EmployeeSerializer,
    DeviceSerializer,
)
from rest_framework import viewsets
from rest_framework.decorators import action


from django.shortcuts import render
from django.http import HttpResponse
from device_api.models import Employee, Device

import device_api.response
def create_user(request):
    return HttpResponse("user")

def about(request):
    return render(request, 'blog/home.html')


class BaseModelViewSet(viewsets.ModelViewSet):
    """Base Model ViewSet class to be inherited by other ViewSet classes."""

    def get_permissions(self):
        """
        Override the get_permissions method to get your defined permissions for this ViewSet.
        """
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except (AttributeError, KeyError):
            return [permission() for permission in self.permission_classes]

    def paginate_response(self, query_set, context={}):
        page = self.paginate_queryset(query_set)
        return self.get_paginated_response(
            self.get_serializer(page, many=True, context=context).data
        )


class BaseGenericViewSet(viewsets.GenericViewSet):
    """Base Generic ViewSet class to be inherited by other ViewSet classes."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # noqa

    def get_permissions(self):
        """
        Override the get_permissions method to get your defined permissions for this ViewSet.
        """
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except (AttributeError, KeyError):
            return [permission() for permission in self.permission_classes]


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    Common class to store Employees
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class DeviceViewSet(viewsets.ModelViewSet):
    """
    Common class to store Devices
    """


    queryset = Device.objects.all()
    serializer_class = DeviceSerializer