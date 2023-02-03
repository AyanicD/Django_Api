from device_api.serializers import (
    EmployeeSerializer,
    DeviceSerializer,
    DetailSerializer
)
import json
import smtplib, ssl
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status

from device_api.filters import (
    filter_dname, filter_email, filter_type, filter_ename
)
from device_api.emaili import your_email, password
from django.shortcuts import render
from django.http import HttpResponse
from device_api.models import Employee, Device

from rest_framework.response import Response
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
    filter_func = {
        "name": filter_ename,
        "email": filter_email,
    }
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    def list(self,request):

        emp_list = self.queryset
        query_params_keys = request.GET.keys()
        for key in query_params_keys:
            filter_func = self.filter_func.get(key, None)

            if filter_func is not None:
                emp_list = filter_func(
                    emp_list,
                    request.GET.get(key, "").split(",")
                    if request.GET.get(key, "")
                    else [],
                )
        print(emp_list)
        emp_list = EmployeeSerializer(emp_list,many=True)
        return Response(emp_list.data)

    @action(methods=["GET"], detail=False)
    def gettop(self,request):
        num = request.data['num']
        print(num)
        emp_list = self.queryset[:num]  
        print(emp_list)          
        emp_serial = EmployeeSerializer(emp_list, many=True)
        print(emp_serial.data)
        return Response(emp_serial.data)


class DeviceViewSet(viewsets.ModelViewSet):
    """
    Common class to store Devices
    """
    filter_func = {
        "name": filter_dname,
        "type": filter_type,
    }

    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    @action(methods=["POST"], detail=True)
    def alloc_dealloc(self, request,pk=None):
        "API to allocate Devices to the Employees"
        try:
            device = Device.objects.get(pk=pk)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
        print(request.data)
        allocated = ""
        if not request.data:
            allocated = "de"
            request.data['employee'] = None
            emp=device.employee
        serializer = DeviceSerializer(device, data=request.data, partial=True)
        message={}
        if serializer.is_valid():
            serializer.save()
            if not allocated:
                emp = Employee.objects.get(pk=serializer.data['employee'])   
                print(emp.email)
            message["success"]="Update Successful"
            port = 465  # For SSL
            receiver_email = emp.email
            message = f"""\
                Subject: Hi there

                {serializer.data["name"]} has been {allocated}allocated to you."""

            context = ssl.create_default_context()
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(your_email, password)
                server.sendmail(your_email, receiver_email, message)
                server.quit()
            return Response(data=message)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["GET"], detail=False)
    def gettop(self,request):
        num = request.data['num']
        print(num)
        dev_list = self.queryset[:num]  
        print(dev_list)          
        dev_serial = DeviceSerializer(dev_list, many=True)
        print(dev_serial.data)
        return Response(dev_serial.data)

    def list(self,request):

        dev_list = self.queryset
        query_params_keys = request.GET.keys()
        for key in query_params_keys:
            filter_func = self.filter_func.get(key, None)

            if filter_func is not None:
                dev_list = filter_func(
                    dev_list,
                    request.GET.get(key, "").split(",")
                    if request.GET.get(key, "")
                    else [],
                )
        print(dev_list)
        dev_list = DeviceSerializer(dev_list,many=True)
        return Response(dev_list.data)
    
    @action(methods=["GET"], detail=False)
    def alluser_type(self, request):
        query_params = request.GET
        print(query_params['type'])
        device = self.queryset.filter(type=query_params['type'])
        device = DetailSerializer(device,many=True)
 
        return Response(device.data)    
    
    @action(methods=["POST"], detail=False)
    def switch(self, request):
        req = json.loads(request.body)
        print(req["name"][0])
        print(req["name"][1])
        try:
            device1 = Device.objects.get(name=req["name"][0])
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:    
            device2 = Device.objects.get(name=req["name"][1])
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        device1.employee,device2.employee=device2.employee,device1.employee
        device1.save(update_fields=['employee'])
        device2.save(update_fields=['employee'])
        return Response(data="Success")

        

    
        

        