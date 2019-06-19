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
    context_object_name = 'home_page'

# Sites CBVs
class SitesListView(LoginRequiredMixin, ListView):
    """ CBV to display the created sites"""
    context_object_name = 'sites'
    model = models.Sites
    paginate_by = 10


class SitesDetailView(LoginRequiredMixin, DetailView):
    """ CBV to display site details"""
    context_object_name = 'sites_detail'
    model = models.Sites
    template_name = 'main_app/sites_detail.html'


class SiteCreateView(LoginRequiredMixin, CreateView):
    """ CBV form to create new sites"""
    form_class = SitesForm
    model = models.Sites

    def form_valid(self, form):
        sitename = form.cleaned_data.get('site_name')
        messages.add_message(
            self.request, messages.SUCCESS, f'Site {sitename} created!')
        return super().form_valid(form)


class SiteUpdateView(LoginRequiredMixin, UpdateView):
    """ CBV form to update site details"""
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
    """CBV delete form to delete sites"""
    context_object_name = 'site'
    model = models.Sites
    success_url = reverse_lazy('main_app:viewsites')


# Devices CBVs
class DeviceListView(LoginRequiredMixin, ListView):
    "CBV to display created devices in the db"
    context_object_name = 'devices'
    model = models.Devices
    paginate_by = 10



class DeviceDetailView(LoginRequiredMixin, DetailView):
    "CBV to display device detail information"
    context_object_name = 'device_detail'
    model = models.Devices
    template_name = 'main_app/devices_detail.html'


class DeviceCreateView(LoginRequiredMixin, CreateView):
    "CBV form to create new devices"
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
    "CBV form to update device details"
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
    "CBV to delete devices"
    context_object_name = 'device'
    model = models.Devices
    success_url = reverse_lazy('main_app:viewdevices')


class DeviceConfigDetailView(LoginRequiredMixin, DetailView):
    "CBV display device saved configuration"
    context_object_name = 'deviceconfig'
    model = models.DeviceDetail
    template_name = 'main_app/deviceconfig_view.html'


class DeviceScriptDetailView(LoginRequiredMixin, DetailView):
    "CBV display device saved custom scripts"
    context_object_name = 'devicescript'
    model = models.DeviceDetail
    template_name = 'main_app/devicescript_view.html'

class DeviceConfigDeleteView(LoginRequiredMixin, DeleteView):
    "CBV to delete device configurations from the db."
    context_object_name = 'deviceconfig'
    model = models.DeviceDetail
    success_url = reverse_lazy('main_app:viewdevices')



def get_platform_detail(request, deviceip, deviceid):
    """
    get_platform_detail takes 3 arguements (request, ip, device_db_id)
    function will then call the population function sync_platform under
    pullconfig_script module, which will then call the OS class method
    get_platform_detail under api_scripts module.

    platform details will be returned by get_platform_detail in a dictionary
    to be populated in the DB by sync_platform function using the
    sync_platform_attributes method in class DataBaseActions under
    pullconfig_script module in the script directory.
    """
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
    """
    function will pass device ip and device db id to the population script
    function sync_device_configuration under module pullconfig_script
    which will call the method in the OS class under api_scripts module
    to pull the running configuration of the device and return it in a
    dictionary to be handled by sync_device_configuration function which
    will perform a DB update function to update the configuration in the db.
    """
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
    """
    This function will call a method in api_scripts class and pass all values
    selected through the user interface such interface, data vlan and voice vlan
    input data will be stored in a dictionary which will then be passed to
    the change_port_vlan_assignment method in the respective OS class.
    """
    success_url = f'devices/{deviceid}'
    interface_detail = request.GET.get('interface').split("=")
    data_vlan_id = request.GET.get('data_vlan_id')
    voice_vlan_id = request.GET.get('voice_vlan_id')
    change_detail = {'ip':deviceip, 'device_id': deviceid,
                    'interface_type':interface_detail[0],
                    'interface_number':interface_detail[1],
                    'data_vlan_id':int(data_vlan_id),
                    'voice_vlan_id':int(voice_vlan_id)}
    #print(change_detail)
    try:
        action = vlan_change(change_detail)
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
    """This function will call a population function get_device_vlans in
    pullconfig_script module under script directory, this function will then
    call the discover vlan method in the OS class under api_scripts module
    which will discover the vlans and return a dictionary which will be used
    by  get_device_vlans function to perform a db population using the
    DataBaseActions class under pullconfig_script module.
    """
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
    """
    This FBV will perform a query on the db and render results on the
    results.html template.
    """
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
