from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Sites)
admin.site.register(models.Devices)
admin.site.register(models.DeviceDetail)
admin.site.register(models.DeviceInterfaces)
admin.site.register(models.DeviceVlans)
