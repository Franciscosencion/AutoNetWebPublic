from django.db import models
from django.urls import reverse
# Create your models here.

class Sites(models.Model):

    site_name = models.CharField(max_length=100)
    site_location = models.CharField(max_length=250)
    site_address = models.CharField(max_length=400, null=True)
    site_poc_name = models.CharField(max_length=100)
    site_poc_number = models.CharField(max_length=30)

    def __str__(self):
        return self.site_name

    def get_absolute_url(self):
        return reverse('main_app:sitesdetail', kwargs={'pk': self.pk})

class Devices(models.Model):
    VENDOR_LIST = (('C', 'Cisco'),
                                    ('J', 'Juniper'),
                                    ('A', 'Arista'),
                                    )
    device_name = models.CharField(max_length=100)
    device_ip = models.GenericIPAddressField()
    vendor = models.CharField(choices=VENDOR_LIST, max_length=10,
                                                default=VENDOR_LIST[0])
    site = models.ForeignKey(Sites,
                            on_delete=models.CASCADE,
                            related_name = 'devices',
                            )

    def __str__(self):
        return self.device_name

    def get_absolute_url(self):
        return reverse('main_app:devicedetail', kwargs={'pk': self.pk})

class DeviceDetail (models.Model):
    device_model = models.CharField(max_length=100, null=True)
    device_sn = models.CharField(max_length=250, null=True)
    device_config = models.TextField(null=True)
    device_script = models.TextField(null=True)
    last_modify = models.DateTimeField(null=True)
    device_id = models.OneToOneField(Devices, on_delete=models.CASCADE,
                                    related_name = 'config', primary_key=True)

    def __str__(self):
        return self.device_id.device_name
