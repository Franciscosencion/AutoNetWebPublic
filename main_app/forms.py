from django import forms
from .models import Sites, Devices


class SitesForm(forms.ModelForm):
    """
    this form class will be used to customize the form widgets based on custom
    css stylesheet
    """
    class Meta():
        model = Sites
        fields = ('site_name', 'site_location', 'site_address',
                    'site_poc_name', 'site_poc_number')
        widgets = {
                    'site_name': forms.TextInput(attrs={
                    'class':'textinputclass', 'placeholder': 'Site Name'}),
                    'site_location':forms.TextInput(attrs={
                    'class':'textinputclass', 'placeholder': 'Location'}),
                    'site_address':forms.TextInput(attrs={
                    'class':'textinputclass', 'placeholder': 'Address'}),
                    'site_poc_name':forms.TextInput(attrs={
                    'class':'textinputclass', 'placeholder': 'Point of Contact'}),
                    'site_poc_number':forms.TextInput(attrs={
                    'class':'textinputclass', 'placeholder': 'POC Number'}),
        }


class DeviceForm(forms.ModelForm):
    """
    this form class will be used to customize the form widgets based on custom
    css stylesheet
    """

    class Meta():
        model = Devices
        fields = ('device_name', 'device_ip', 'vendor', 'device_type',
                    'operating_system', 'device_username',
                    'device_password','site')
        widgets = {
                    'device_name': forms.TextInput(attrs={
                    'class':'textinputclass', 'placeholder': 'Device Name'}),
                    'device_ip':forms.TextInput(attrs={
                    'class':'textinputclass', 'placeholder': 'IP Address'}),
                    'vendor':forms.Select(attrs={
                    'class':'mycustom-select', 'id':'vendor-select'}),
                    'device_type':forms.Select(attrs={
                    'class':'mycustom-select', 'id':'device-type-select'}),
                    'operating_system':forms.Select(attrs={
                    'class':'mycustom-select', 'id':'os-select'}),
                    'device_username':forms.TextInput(attrs={
                    'class':'textinputclass', 'placeholder': 'username'}),
                    'device_password':forms.TextInput(attrs={
                    'class':'textinputclass', 'type':'password',
                    'placeholder': 'password'}),
                    'site':forms.Select(attrs={
                    'class':'mycustom-select', 'id':'site-select'}),
        }
