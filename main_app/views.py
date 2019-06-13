from django.shortcuts import render, redirect
from django.views.generic import (TemplateView, ListView, DetailView,
                                    CreateView, UpdateView, DeleteView)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from requests.exceptions import ConnectionError
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q as Query
from netmiko.ssh_exception import (AuthenticationException,
                                    NetMikoTimeoutException)
from paramiko.ssh_exception import SSHException
from . import models
from .forms import SitesForm, DeviceForm
from script.pullconfig_script import (sync_platform,
                                        sync_device_configuration,
                                        vlan_change,
                                        get_device_vlans,
                                        )
from script.api_scripts import AuthenticationError

# Create your views here.

class HomeTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'main_app/home.html'


# Sites CBVs
class SitesListView(LoginRequiredMixin, ListView):
    context_object_name = 'sites'
    model = models.Sites
    paginate_by = 10


class SitesDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'sites_detail'
    model = models.Sites
    template_name = 'main_app/sites_detail.html'


class SiteCreateView(LoginRequiredMixin, CreateView):
    # fields = ('site_name', 'site_location',
    #             'site_poc_name', 'site_poc_number',
    #             'site_address')
    form_class = SitesForm
    model = models.Sites

    def form_valid(self, form):
        sitename = form.cleaned_data.get('site_name')
        messages.add_message(
            self.request, messages.SUCCESS, f'Site {sitename} created!')
        return super().form_valid(form)


class SiteUpdateView(LoginRequiredMixin, UpdateView):
    # fields = ('site_name', 'site_poc_name', 'site_poc_number')
    form_class = SitesForm
    model = models.Sites

    def form_valid(self, form):
        sitename = form.cleaned_data.get('site_name')
        messages.add_message(
            self.request, messages.SUCCESS,
            f'Site detail for {sitename} updated!')
        return super().form_valid(form)


class SiteDeleteView(LoginRequiredMixin, DeleteView):
    context_object_name = 'site'
    model = models.Sites
    success_url = reverse_lazy('main_app:viewsites')


# Devices CBVs
class DeviceListView(LoginRequiredMixin, ListView):
    context_object_name = 'devices'
    model = models.Devices
    paginate_by = 10



class DeviceDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'device_detail'
    model = models.Devices
    template_name = 'main_app/devices_detail.html'


class DeviceCreateView(LoginRequiredMixin, CreateView):
    # fields = ('device_name', 'device_ip',
    #             'vendor',  'site')
    form_class = DeviceForm
    model = models.Devices

    def form_valid(self, form):
        devicename = form.cleaned_data.get('device_name')
        messages.add_message(
            self.request, messages.SUCCESS, f'Device {devicename} created!')
        return super().form_valid(form)


class DeviceUpdateView(LoginRequiredMixin, UpdateView):
    # fields = ('device_name', 'device_ip',
    #             'site', 'vendor')
    form_class = DeviceForm
    model = models.Devices

    def form_valid(self, form):
        devicename = form.cleaned_data.get('device_name')
        messages.add_message(
            self.request, messages.SUCCESS, f'Update to {devicename} done!')
        return super().form_valid(form)


class DeviceDeleteView(LoginRequiredMixin, DeleteView):
    context_object_name = 'device'
    model = models.Devices
    success_url = reverse_lazy('main_app:viewdevices')


class DeviceConfigDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'deviceconfig'
    model = models.DeviceDetail
    template_name = 'main_app/deviceconfig_view.html'


class DeviceScriptDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'devicescript'
    model = models.DeviceDetail
    template_name = 'main_app/devicescript_view.html'

class DeviceConfigDeleteView(LoginRequiredMixin, DeleteView):
    context_object_name = 'deviceconfig'
    model = models.DeviceDetail
    success_url = reverse_lazy('main_app:viewdevices')



def get_platform_detail(request, deviceip, deviceid):
    success_url = f'devices/{deviceid}'
    try:
        sync_platform(deviceip, deviceid)
        messages.add_message(
            request, messages.SUCCESS, f'platform details synced')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except ConnectionError:
        messages.add_message(
            request, messages.ERROR, f'IP {deviceip} unreachable')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except AuthenticationError:
        messages.add_message(
            request, messages.ERROR, 'Invalid username and password')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except AuthenticationException:
        messages.add_message(
            request, messages.ERROR, 'Invalid username and password')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except NetMikoTimeoutException:
        messages.add_message(
            request, messages.ERROR, 'Connection request timeout')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except SSHException:
        messages.add_message(
            request, messages.ERROR, 'Unable to establish SSH session, SSH enabled?')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except Exception as error:
        messages.add_message(
            request, messages.WARNING, f'Unknown error has occurred: {error}')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))



@login_required
def sync_configuration(request, deviceip, deviceid):
    success_url = f'devices/{deviceid}'
    try:
        user = request.user
        sync_device_configuration(deviceip, deviceid, user)
        messages.add_message(
            request, messages.SUCCESS, f'Configuration has been synced')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except ConnectionError:
        messages.add_message(
            request, messages.ERROR, f'IP {deviceip} unreachable')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except AuthenticationError:
        messages.add_message(
            request, messages.ERROR, 'Invalid username and password')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except AuthenticationException:
        messages.add_message(
            request, messages.ERROR, 'Invalid username and password')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except NetMikoTimeoutException:
        messages.add_message(
            request, messages.ERROR, 'Connection request timeout')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except SSHException:
        messages.add_message(
            request, messages.ERROR, 'Unable to establish SSH session, SSH enabled?')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except Exception as error:
        messages.add_message(
            request, messages.WARNING, f'Unknown error has occurred: {error}')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))

@login_required
def port_vlan_assignment(request, deviceip, deviceid):
    success_url = f'devices/{deviceid}'
    device_ip = deviceip
    device_id = deviceid
    interface_type = request.GET.get('interface_type')
    interfaces = request.GET.get('interface')
    data_vlan_id = request.GET.get('data_vlan')
    voice_vlan_id = request.GET.get('voice_vlan_id')
    print(device_ip)
    print(device_id)
    print(interface_type)
    print(interfaces)

    try:
        action = vlan_change(deviceip, interface_type,
                            interfaces, int(data_vlan_id),
                            int(voice_vlan_id))
        messages.add_message(
            request, messages.SUCCESS, f'{action}')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except ConnectionError:
        messages.add_message(
            request, messages.ERROR, f'IP {deviceip} unreachable')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except AuthenticationError:
        messages.add_message(
            request, messages.ERROR, 'Invalid username and password')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except AuthenticationException:
        messages.add_message(
            request, messages.ERROR, 'Invalid username and password')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except NetMikoTimeoutException:
        messages.add_message(
            request, messages.ERROR, 'Connection request timeout')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except SSHException:
        messages.add_message(
            request, messages.ERROR, 'Unable to establish SSH session, SSH enabled?')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except Exception as error:
        messages.add_message(
            request, messages.WARNING, f'Unknown error has occurred: {error}')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))

@login_required
def sync_device_vlans(request, deviceip, deviceid):
    success_url = f'devices/{deviceid}'
    try:

        get_device_vlans(deviceip, deviceid)
        messages.add_message(
            request, messages.SUCCESS, f'VLANs synced')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except ConnectionError:
        messages.add_message(
            request, messages.ERROR, f'IP {deviceip} unreachable')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except AuthenticationError:
        messages.add_message(
            request, messages.ERROR, 'Invalid username and password')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except AuthenticationException:
        messages.add_message(
            request, messages.ERROR, 'Invalid username and password')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except NetMikoTimeoutException:
        messages.add_message(
            request, messages.ERROR, 'Connection request timeout')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except SSHException:
        messages.add_message(
            request, messages.ERROR, 'Unable to establish SSH session, SSH enabled?')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))
    except Exception as error:
        messages.add_message(
            request, messages.WARNING, f'Unknown error has occurred: {error}')
        return HttpResponseRedirect(reverse(f'main_app:devicedetail',
                                        kwargs={'pk': deviceid}))

@login_required
def device_search_function(request):
    name = request.GET.get('item')
    # return HttpResponse(f'<h2>{name}</h2>')
    try:
        #results = models.Devices.objects.active()
        results = models.Devices.objects.filter(
                    Query(device_name__startswith=name) |
                    Query(device_name__icontains=name) |
                    Query(device_ip__startswith=name) |
                    Query(device_ip__icontains=name)
                    )

    except Exception as error:
        return HttpResponse(error)
    return render(request, 'main_app/results.html', {'results':results})
