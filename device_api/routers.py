from rest_framework import routers
from device_api.viewsets import EmployeeViewSet, DeviceViewSet
from django.urls import include,path


class BaseRouter(routers.SimpleRouter):
    """Base Router class to be inherited by all Router classes."""

    def extend(self, extended_router=None):
        if extended_router:
            self.registry.extend(extended_router.registry)  # noqa


EmployeeRouter = BaseRouter()
EmployeeRouter.register(
    "employees",
    EmployeeViewSet,
)


DeviceRouter = BaseRouter()
DeviceRouter.register(
    "devices",
    DeviceViewSet,
)
