from device_api.models import Employee, Device
from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    """Base Serializer class to be inherited by other Serializer classes."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # noqa


class BaseReadOnlySerializer(serializers.Serializer):
    """Base Read-Only Serializer class to be inherited by other Read-Only Serializer classes."""

    id = serializers.UUIDField()
    created_at = serializers.DateTimeField()
    modified_at = serializers.DateTimeField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # noqa


class EmployeeSerializer(BaseModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

        
class DeviceSerializer(BaseModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"