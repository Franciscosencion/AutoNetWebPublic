from django.shortcuts import render
from django.views.generic import (TemplateView, ListView, DetailView,
                                    CreateView, UpdateView, DeleteView)
from django.urls import reverse_lazy
from . import models
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

class SiteUpdateView(UpdateView):
    fields = ('site_name', 'site_poc_name', 'site_poc_number')
    model = models.Sites

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
                'device_model', 'device_sn',
                'site')
    model = models.Devices
