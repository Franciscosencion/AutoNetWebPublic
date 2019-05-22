from django.shortcuts import render, redirect
from django.views.generic import (TemplateView, ListView, DetailView,
                                    CreateView, UpdateView, DeleteView)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from script.pullconfig_script import sync_config
# Create your views here.

class HomeTemplateView(TemplateView):
    template_name = 'main_app/home.html'


# Sites CBVs
class SitesListView(ListView):
    context_object_name = 'sites'
    model = models.Sites


class SitesDetailView(DetailView):
    context_object_name = 'sites_detail'
    model = models.Sites
    template_name = 'main_app/sites_detail.html'


class SiteCreateView(CreateView):
    fields = ('site_name', 'site_location',
                'site_poc_name', 'site_poc_number',
                'site_address')
    model = models.Sites

    def form_valid(self, form):
        sitename = form.cleaned_data.get('site_name')
        messages.add_message(
            self.request, messages.SUCCESS, f'Site {sitename} created!')
        return super().form_valid(form)


class SiteUpdateView(UpdateView):
    fields = ('site_name', 'site_poc_name', 'site_poc_number')
    model = models.Sites

    def form_valid(self, form):
        sitename = form.cleaned_data.get('site_name')
        messages.add_message(
            self.request, messages.SUCCESS,
            f'Site detail for {sitename} updated!')
        return super().form_valid(form)


class SiteDeleteView(DeleteView):
    context_object_name = 'site'
    model = models.Sites
    success_url = reverse_lazy('main_app:viewsites')


# Devices CBVs
class DeviceListView(ListView):
    context_object_name = 'devices'
    model = models.Devices


class DeviceDetailView(DetailView):
    context_object_name = 'device_detail'
    model = models.Devices
    template_name = 'main_app/devices_detail.html'


class DeviceCreateView(CreateView):
    fields = ('device_name', 'device_ip',
                'vendor',  'site')
    model = models.Devices

    def form_valid(self, form):
        devicename = form.cleaned_data.get('device_name')
        messages.add_message(
            self.request, messages.SUCCESS, f'Device {devicename} created!')
        return super().form_valid(form)


class DeviceUpdateView(UpdateView):
    fields = ('device_name', 'device_ip',
                'site', 'vendor')
    model = models.Devices

    def form_valid(self, form):
        devicename = form.cleaned_data.get('device_name')
        messages.add_message(
            self.request, messages.SUCCESS, f'Update to {devicename} done!')
        return super().form_valid(form)


class DeviceDeleteView(DeleteView):
    context_object_name = 'device'
    model = models.Devices
    success_url = reverse_lazy('main_app:viewdevices')


class DeviceConfigDetailView(DetailView):
    context_object_name = 'deviceconfig'
    model = models.DeviceDetail
    template_name = 'main_app/deviceconfig_view.html'


class DeviceScriptDetailView(DetailView):
    context_object_name = 'devicescript'
    model = models.DeviceDetail
    template_name = 'main_app/devicescript_view.html'

class DeviceConfigDeleteView(DeleteView):
    context_object_name = 'deviceconfig'
    model = models.DeviceDetail
    success_url = reverse_lazy('main_app:viewdevices')

@login_required
def sync_configuration(request, deviceip, deviceid):
    success_url = f'devices/{deviceid}'
    try:

        script = sync_config(deviceip, deviceid)
        # return HttpResponse(f"<p1>{script}</p1>")
        if script:
            messages.add_message(
                request, messages.SUCCESS, f'{deviceip} config sync done!')
            return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                            kwargs={'pk': deviceid}))
        else:
            messages.add_message(
                request, messages.WARNING, 'Sync Failed')
            return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                            kwargs={'pk': deviceid}))
    except Exception as error:
        return HttpResponse(f"<p1>{error}</p1>")
