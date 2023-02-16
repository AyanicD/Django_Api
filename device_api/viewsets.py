from device_api.serializers import (
    EmployeeSerializer,
    DeviceSerializer,
    DetailSerializer,
    AttachmentSerializer,
    ChunkedUploadSerialiser

)
import json , re
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
from django.core.files.base import ContentFile
from device_api.models import Employee, Device, Attachment, ChunkedUpload

from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from django.utils import timezone

COMPLETE = 2

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

class AttachmentViewSet(viewsets.ModelViewSet):
    """
    Common class to store Attachment
    """

    queryset = Attachment.objects.all().order_by("name")
    serializer_class = AttachmentSerializer

class ChunkedUploadBaseViewSet(viewsets.ModelViewSet):
    """
    Base viewset for the rest of chunked upload views.
    """

    # Has to be a ChunkedUpload subclass
    model = ChunkedUpload
    serializer_class = ChunkedUploadSerialiser
    user_field_name = 'user'  # the field name that point towards the AUTH_USER in ChunkedUpload class or its subclasses
    queryset = ChunkedUpload.objects.all()

    def save(self, chunked_upload, request, new=False):
        """
        Method that calls save(). Overriding may be useful is save() needs
        special args or kwargs.
        """
        chunked_upload.save()

    def _save(self, chunked_upload):
        """
        Wraps save() method.
        """
        new = chunked_upload.id is None
        self.save(chunked_upload, self.request, new=new)

    def _post(self, request, *args, **kwargs):
        raise NotImplementedError

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.
        """
        
        return self._post(request, *args, **kwargs)



class ChunkedUploadViewSet(ChunkedUploadBaseViewSet):
    """
    Uploads large files in multiple chunks. Also, has the ability to resume
    if the upload is interrupted.
    """

    field_name = 'file'
    content_range_header = 'HTTP_CONTENT_RANGE'
    content_range_pattern = re.compile(
        r'^bytes (?P<start>\d+)-(?P<end>\d+)/(?P<total>\d+)$'
    )
    max_bytes = None # Max amount of data that can be uploaded
    # If `fail_if_no_header` is True, an exception will be raised if the
    # content-range header is not found. Default is False to match Jquery File
    # Upload behavior (doesn't send header if the file is smaller than chunk)
    fail_if_no_header = False

    def get_extra_attrs(self, request):
        """
        Extra attribute values to be passed to the new ChunkedUpload instance.
        Should return a dictionary-like object.
        """
        attrs = {}
        if hasattr(self.model, self.user_field_name) and hasattr(request, 'user'):
            attrs[self.user_field_name] = request.user
        return attrs

    def create_chunked_upload(self, save=False, **attrs):
        """
        Creates new chunked upload instance. Called if no 'upload_id' is
        found in the POST data.
        """
        chunked_upload = self.model(**attrs)
        # file starts empty
        chunked_upload.file.save(name='', content=ContentFile(''), save=save)
        return chunked_upload

    def is_valid_chunked_upload(self, chunked_upload):
        """
        Check if chunked upload has already expired or is already complete.
        """
        if chunked_upload.expired:
            raise Response(status=status.HTTP_410_GONE,
                                     detail='Upload has expired')
        error_msg = 'Upload has already been marked as "%s"'
        if chunked_upload.status == COMPLETE:
            raise Response(status=status.HTTP_400_BAD_REQUEST,
                                     detail=error_msg % 'complete')

    def get_response_data(self, chunked_upload, request):
        """
        Data for the response. Should return a dictionary-like object.
        """
        return {
            'upload_id': chunked_upload.upload_id,
            'offset': chunked_upload.offset,
            'expires': chunked_upload.expires_on
        }

    def _post(self, request, *args, **kwargs):
        chunk = request.FILES.get(self.field_name)
        if chunk is None:
            raise Response(status=status.HTTP_400_BAD_REQUEST,
                                     detail='No chunk file was submitted')
        self.validate(request)

        upload_id = request.POST.get('upload_id')
        if upload_id:
            chunked_upload = get_object_or_404(self.queryset,
                                               upload_id=upload_id)
            self.is_valid_chunked_upload(chunked_upload)
        else:
            attrs = {'filename': chunk.name}

            attrs.update(self.get_extra_attrs(request))
            chunked_upload = self.create_chunked_upload(save=False, **attrs)

        content_range = request.META.get(self.content_range_header, '')
        match = self.content_range_pattern.match(content_range)
        if match:
            start = int(match.group('start'))
            end = int(match.group('end'))
            total = int(match.group('total'))
        elif self.fail_if_no_header:
            raise Response(status=status.HTTP_400_BAD_REQUEST,
                                     detail='Error in request headers')
        else:
            # Use the whole size when HTTP_CONTENT_RANGE is not provided
            start = 0
            end = chunk.size - 1
            total = chunk.size

        chunk_size = end - start + 1
        max_bytes = self.max_bytes

        if max_bytes is not None and total > max_bytes:
            raise Response(
                status=status.HTTP_400_BAD_REQUEST,
                detail='Size of file exceeds the limit (%s bytes)' % max_bytes
            )
        if chunked_upload.offset != start:
            raise Response(status=status.HTTP_400_BAD_REQUEST,
                                     detail='Offsets do not match',
                                     offset=chunked_upload.offset)
        if chunk.size != chunk_size:
            raise Response(status=status.HTTP_400_BAD_REQUEST,
                                     detail="File size doesn't match headers")

        chunked_upload.append_chunk(chunk, chunk_size=chunk_size, save=False)

        self._save(chunked_upload)

        return Response(self.get_response_data(chunked_upload, request),
                        status=status.HTTP_200_OK)


class ChunkedUploadCompleteView(ChunkedUploadBaseViewSet):
    """
    Completes an chunked upload. Method `on_completion` is a placeholder to
    define what to do when upload is complete.
    """

    # I wouldn't recommend to turn off the md5 check, unless is really
    # impacting your performance. Proceed at your own risk.
    do_md5_check = True

    def on_completion(self, uploaded_file, request):
        """
        Placeholder method to define what to do when upload is complete.
        """

    def is_valid_chunked_upload(self, chunked_upload):
        """
        Check if chunked upload is already complete.
        """
        if chunked_upload.status == COMPLETE:
            error_msg = "Upload has already been marked as complete"
            return Response(status=status.HTTP_400_BAD_REQUEST,
                                      detail=error_msg)

    def md5_check(self, chunked_upload, md5):
        """
        Verify if md5 checksum sent by client matches generated md5.
        """
        if chunked_upload.md5 != md5:
            raise Response(status=status.HTTP_400_BAD_REQUEST,
                                     detail='md5 checksum does not match')

    def _post(self, request, *args, **kwargs):
        upload_id = request.POST.get('upload_id')
        md5 = request.POST.get('md5')

        error_msg = None
        if self.do_md5_check:
            if not upload_id or not md5:
                error_msg = "Both 'upload_id' and 'md5' are required"
        elif not upload_id:
            error_msg = "'upload_id' is required"
        if error_msg:
            raise Response(status=status.HTTP_400_BAD_REQUEST,
                                     detail=error_msg)

        chunked_upload = get_object_or_404(self.queryset,
                                           upload_id=upload_id)

        self.validate(request)
        self.is_valid_chunked_upload(chunked_upload)
        if self.do_md5_check:
            self.md5_check(chunked_upload, md5)

        chunked_upload.status = COMPLETE
        chunked_upload.completed_on = timezone.now()
        self._save(chunked_upload)
        self.on_completion(chunked_upload.get_uploaded_file(), request)

        return Response(self.get_response_data(chunked_upload, request),
                        status=status.HTTP_200_OK)

        

    
        

        