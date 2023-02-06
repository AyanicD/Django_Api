from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from device_api.models import Device, Employee

admin.site.register(Device, SimpleHistoryAdmin)
admin.site.register(Employee, SimpleHistoryAdmin)