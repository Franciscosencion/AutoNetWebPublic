import uuid as uuid_lib
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.


class Sites(models.Model):

    site_name = models.CharField(max_length=100)
    site_location = models.CharField(max_length=250)
    uuid = models.UUIDField( #used by the API to look up the record
                            db_index=True,
                            default=uuid_lib.uuid4,
                            editable=False)
    site_address = models.CharField(max_length=400, null=True)
    site_poc_name = models.CharField(max_length=100)
    site_poc_number = models.CharField(max_length=30)

    def __str__(self):
        return self.site_name

    def get_absolute_url(self):
        return reverse('main_app:sitesdetail', kwargs={'pk': self.pk})


class Devices(models.Model):
    VENDOR_LIST = (('C', 'Cisco'), ('J', 'Juniper'), ('A', 'Arista'))
    DEVICE_TYPES = (('R', 'Router'), ('S', 'Switch'), ('F', 'Firewall'))
    CISCO_OS = (('1', 'CISCO IOS'), ('2', 'CISCO IOS-XE'),
                ('3', 'CISCO IOS-XR'), ('4', 'CISCO NX-OS'))
    device_name = models.CharField(max_length=100)
    device_ip = models.GenericIPAddressField()
    device_model = models.CharField(max_length=100, null=True, blank=True)
    device_sn = models.CharField(max_length=250, null=True, blank=True)
    uuid = models.UUIDField( #used by the API to look up the record
                            db_index=True,
                            default=uuid_lib.uuid4,
                            editable=False)
    vendor = models.CharField(choices=VENDOR_LIST, max_length=10,
                                                default=VENDOR_LIST[0])
    device_type = models.CharField(choices=DEVICE_TYPES, max_length=10,
                                                default=DEVICE_TYPES[0])
    operating_system = models.CharField(choices=CISCO_OS, max_length=10,
                                                default=CISCO_OS)
    site = models.ForeignKey(Sites,
                            on_delete=models.CASCADE,
                            related_name = 'devices',
                            )
    objects = models.Manager()
    def __str__(self):
        return self.device_name

    def get_absolute_url(self):
        return reverse('main_app:devicedetail', kwargs={'pk': self.pk})


class DeviceDetail (models.Model):

    device_config = models.TextField(null=True)
    device_script = models.TextField(null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='createdby',
                                        on_delete=models.PROTECT, null=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='modifiedby',
                                        on_delete=models.PROTECT, null=True)
    config_created = models.DateTimeField(auto_now_add=True)
    last_modify = models.DateTimeField(blank=True, null=True) #null=True
    device_id = models.OneToOneField(Devices, on_delete=models.CASCADE,
                                    related_name = 'config', primary_key=True)

    def __str__(self):
        return self.device_id.device_name


class DeviceInterfaces(models.Model):
    """
    Model for device interfaces
    """
    interface_type = models.CharField(max_length=200, null=True, blank=True)
    interface_number = models.CharField(max_length=200, null=True, blank=True)
    device = models.ForeignKey(Devices, related_name='device_interface',
                                        on_delete=models.CASCADE,
                                        null=True,
                                        blank=True)
    def __str__(self):
        return (f'{self.device.device_name} - {self.interface_type}{self.interface_number}')


class DeviceVlans(models.Model):
    """
    Model for device vlans
    """
    vlan_name = models.CharField(max_length=200, null=True, blank=True)
    vlan_id = models.IntegerField(null=True, blank=True)
    device = models.ForeignKey(Devices, related_name='vlans',
                                        on_delete=models.CASCADE,
                                        null=True,
                                        blank=True)

    def __str__(self):
        return self.device.device_name + "_" + self.vlan_name
