from django.db import models

# Create your models here.

class Sites(models.Model):

    site_name = models.CharField(max_length=100)
    site_location = models.CharField(max_length=250)
    site_poc_name = models.CharField(max_length=100)
    site_poc_number = models.CharField(max_length=30)

    def __str__(self):
        return self.site_name

class Devices(models.Model):

    device_name = models.CharField(max_length=100)
    device_ip = models.CharField(max_length=40)
    device_model = models.CharField(max_length=100)
    device_sn = models.CharField(max_length=250)
    site = models.ForeignKey(Sites,
                            on_delete=models.CASCADE,
                            related_name = 'devices',
                            )

    def __str__(self):
        return self.device_name
