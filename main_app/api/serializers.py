from rest_framework import serializers

from ..models import Sites

class SitesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sites
        fields = ['site_name', 'site_location', 'uuid',
                    'site_address', 'site_poc_name',
                    'site_poc_number']
