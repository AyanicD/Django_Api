from device_api.routers import BaseRouter, EmployeeRouter, DeviceRouter

v1_router = BaseRouter()

v1_router.extend(EmployeeRouter)
v1_router.extend(DeviceRouter)
