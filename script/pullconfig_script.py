import os, datetime, re
from multiprocessing import Pool
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NetAutoMgmt.settings')
import django
django.setup()
from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from requests.exceptions import ConnectionError
#custom modules
from main_app.models import DeviceDetail, Devices, DeviceInterfaces


_config = """
This is a test config run using an automated script
"""
class PatternFinder:
    """
    this class will be use to perform regex seraching for any given pattern and data
    """
    def __init__(self, pattern, data):
        self.pattern = pattern
        self.data = data

    def find_match(self):
        """this method will perform the pattern search and return match"""
        pattern = re.compile(self.pattern)
        match = pattern.finditer(self.data)
        try:
            match = [x.group(1) for x in match]
            if len(match) > 1:
                match = ", ".join(match)
            return match
        except Exception as error:
            return(error)


def sync_config(device_ip, device_id, user):

    """
    sync_config will utilize netmiko API to connect to remote device and
    pull the configuration, after that using the values received ip and device
    id configuration will be either updated or created if it does not exist
    """

    try:
        device_object = Devices.objects.get(id=device_id)
        #find serial number & model
        if device_object.vendor == "C":
            if device_object.operating_system == '1':
                #operating system 1 is Cisco IOS
                from .api_scripts import (CiscoIOS)
                platform_detail =CiscoIOS(device_ip)
                pass
            elif device_object.operating_system == '2':
                #Cisco IOS-XE
                from .api_scripts import (CiscoIOSXE)
                platform_detail = CiscoIOSXE(device_ip)
            elif device_object.operating_system == '3':
                # Cisco IOS-XR
                pass
            elif device_object.operating_system == '4':
                # Cisco NX-OS
                pass

        device_detail = platform_detail.get_platform_detail()
        #get constructed config through RESTCONF
        #running_config = platform_detail.get_running_config()
        #get unconstructed config through Netmiko
        device_config = platform_detail.get_running_config()
        object = DeviceDetail.objects.get(device_id_id=device_id)
        # update record if configuration record exist
        DeviceDetail.objects.filter(device_id_id=device_id).update(
                                device_config=device_config[
                                'running_config'],
                                device_script="NA",
                                modified_by = user,
                                last_modify = timezone.now())

        Devices.objects.filter(id=device_id).update(
                                device_model=device_detail["model"],
                                device_sn=device_detail["serial_number"])
        #last_modify=datetime.datetime.now()
        return HttpResponse(status=202)
    except ObjectDoesNotExist:
        # New object will be created if ObjectDoesNotExist exception triggers
        sync_conf = DeviceDetail.objects.get_or_create(
                                device_config=device_config[
                                'running_config'],
                                device_script="NA",
                                created_by = user,
                                modified_by = user,
                                device_id_id=device_id)[0]
        sync_conf.save()
        Devices.objects.filter(id=device_id).update(
                                device_model=device_detail["model"],
                                device_sn=device_detail["serial_number"])



        return HttpResponse(status=201)
    except UnboundLocalError as error:
        raise error
    except ConnectionError as error:
        raise error

def sync_interfaces(device_ip, device_id):
    try:
        device_object = Devices.objects.get(id=device_id)
        #find serial number & model
        if device_object.vendor == "C":
            if device_object.operating_system == '1':
                #operating system 1 is Cisco IOS
                from .api_scripts import (CiscoIOS)
                interfaces =CiscoIOS(device_ip)
                pass
            elif device_object.operating_system == '2':
                #Cisco IOS-XE
                from .api_scripts import (CiscoIOSXE)
                interfaces = CiscoIOSXE(device_ip)
            elif device_object.operating_system == '3':
                # Cisco IOS-XR
                pass
            elif device_object.operating_system == '4':
                # Cisco NX-OS
                pass

        device_interfaces = interfaces.get_interfaces()
        object = DeviceInterfaces.objects.get(device_id=device_id)
        # update record if configuration record exist
        interface_list = list()
        for interface_type, interfaces in device_interfaces.items():
            for interface in interfaces:
                interface_list.append(interface)
        all_interfaces = "\n".join(interface_list)
        DeviceInterfaces.objects.filter(device_id=device_id).update(
                                interfaces=all_interfaces)

        #last_modify=datetime.datetime.now()
        return HttpResponse(status=202)
    except ObjectDoesNotExist:
        # New object will be created if ObjectDoesNotExist exception triggers
        interface_list = list()
        for interface_type, interfaces in device_interfaces.items():
            for interface in interfaces:
                interface_list.append(interface)
        all_interfaces = "\n".join(interface_list)
        sync_conf = DeviceInterfaces.objects.get_or_create(
                                            interfaces=all_interfaces,
                                            device_id=device_id,
                                            )[0]

        sync_conf.save()

        return HttpResponse(status=201)
    except UnboundLocalError as error:
        raise error
    except ConnectionError as error:
        raise error

if __name__ == "__main__":
    print("Updating record")
    sync_config()
