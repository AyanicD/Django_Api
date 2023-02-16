from rest_framework import routers
from device_api.viewsets import EmployeeViewSet, DeviceViewSet, AttachmentViewSet, ChunkedUploadViewSet, ChunkedUploadCompleteView
from django.urls import include,path


class BaseRouter(routers.SimpleRouter):
    """Base Router class to be inherited by all Router classes."""

    def extend(self, extended_router=None):
        if extended_router:
            self.registry.extend(extended_router.registry)  # noqa


CommonRouter = BaseRouter()
CommonRouter.register(
    "employees",
    EmployeeViewSet,
    basename="employees"
)


CommonRouter.register(
    "devices",
    DeviceViewSet,
    basename="devices"
)

CommonRouter.register(
    "attachments",
    AttachmentViewSet,
    basename="attachments"
)

CommonRouter.register(
    "chunkedup",
    ChunkedUploadViewSet,
    basename="chunkedup"
)

CommonRouter.register(
    "chunkedcomp",
    ChunkedUploadCompleteView,
    basename="chunkedcomp"
)
