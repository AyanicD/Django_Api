from device_api.routers import BaseRouter, CommonRouter

v1_router = BaseRouter()

v1_router.extend(CommonRouter)

