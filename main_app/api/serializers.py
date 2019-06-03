from rest_framework import serializers

from ..models import Sites, Devices

class SitesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sites
        fields = ['site_name', 'site_location', 'uuid',
                    'site_address', 'site_poc_name',
                    'site_poc_number']

class DevicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Devices
        fields = ['device_name', 'device_ip', 'uuid',
                    'vendor', 'site']
