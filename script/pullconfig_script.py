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
from main_app.models import (DeviceDetail, Devices,
                            DeviceInterfaces, DeviceVlans,
                            )


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

class DataBaseActions:

    def __init__(self, device_id):

        self.device_id = device_id

    #def update_interfaces(self, all_interfaces):

    #    DeviceInterfaces.objects.filter(device_id=self.device_id).update(
    #                                    interfaces=all_interfaces)

    def sync_interfaces(self, interface_list):

        for interface_type, interface_numbers in interface_list.items():
            for interface_number in interface_numbers:
                interface_add = DeviceInterfaces.objects.get_or_create(
                                            interface_type=interface_type,
                                            interface_number=interface_number,
                                            device_id=self.device_id,
                                            )[0]
        interface_add.save()

    def update_configuration(self, configuration, user):

        DeviceDetail.objects.filter(device_id_id=self.device_id).update(
                                device_config=configuration[
                                'running_config'],
                                device_script="NA",
                                modified_by = user,
                                last_modify = timezone.now())

    def create_configuration(self, configuration, user):

        sync_conf = DeviceDetail.objects.get_or_create(
                                device_config=configuration[
                                'running_config'],
                                device_script="NA",
                                created_by = user,
                                modified_by = user,
                                device_id_id=self.device_id)[0]
        sync_conf.save()

    def sync_platform_attributes(self, device_details):

        Devices.objects.filter(id=self.device_id).update(
                                device_model=device_details["model"],
                                device_sn=device_details["serial_number"],
                                software_version=device_details["os_version"])

    def vlans_add_to_db(self, vlans_dict):
        for vlan_name, vlan_id in vlans_dict.items():
            vlans_add = DeviceVlans.objects.get_or_create(
                                    vlan_name =vlan_name,
                                    vlan_id=vlan_id,
                                    device_id=self.device_id)[0]

        vlans_add.save()

def sync_platform(device_ip, device_id):

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

        device_details = platform_detail.get_platform_detail()
        device_interfaces = platform_detail.get_interfaces()
        #instantiate the database action class
        action = DataBaseActions(device_id)
        #formatting interfaces into multiline string
        #interface_list = list()
        #for interface_type, interfaces in device_interfaces.items():
        #    for interface in interfaces:
        #        interface_list.append(interface)
        #all_interfaces = "\n".join(interface_list) # interfaces formmated

        #try:
            #if interface object exist will update it in the db
            #object = DeviceInterfaces.objects.get(device_id=device_id)
        action.sync_interfaces(device_interfaces)
        action.sync_platform_attributes(device_details)
        #except ObjectDoesNotExist:
            #will create object
        #    action.create_interfaces(all_interfaces)
        #    action.sync_platform_attributes(device_details)
        #
        #
        #
        # # update record if configuration record exist
        # DeviceDetail.objects.filter(device_id_id=device_id).update(
        #                         device_config=device_config[
        #                         'running_config'],
        #                         device_script="NA",
        #                         modified_by = user,
        #                         last_modify = timezone.now())
        #
        # Devices.objects.filter(id=device_id).update(
        #                         device_model=device_detail["model"],
        #                         device_sn=device_detail["serial_number"])
        # #last_modify=datetime.datetime.now()
    # except ObjectDoesNotExist:
    #     # New object will be created if ObjectDoesNotExist exception triggers
    #     sync_conf = DeviceDetail.objects.get_or_create(
    #                             device_config=device_config[
    #                             'running_config'],
    #                             device_script="NA",
    #                             created_by = user,
    #                             modified_by = user,
    #                             device_id_id=device_id)[0]
    #     sync_conf.save()
    #     Devices.objects.filter(id=device_id).update(
    #                             device_model=device_detail["model"],
    #                             device_sn=device_detail["serial_number"])
        return HttpResponse(status=201)
    except UnboundLocalError as error:
        raise error
    except ConnectionError as error:
        raise error

def sync_device_configuration(device_ip, device_id, user):

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

        device_config = platform_detail.get_running_config()
        #instantiate the database action class
        action = DataBaseActions(device_id)

        try:
            object = DeviceDetail.objects.get(device_id_id=device_id)
            action.update_configuration(device_config, user)


        except ObjectDoesNotExist:
            action.create_configuration(device_config, user)


        return HttpResponse(status=201)
    except UnboundLocalError as error:
        raise error
    except ConnectionError as error:
        raise error

def get_device_vlans(device_ip, device_id):

    try:
        device_object = Devices.objects.get(id=device_id)
        #find serial number & model
        if device_object.vendor == "C":
            if device_object.operating_system == '1':
                #operating system 1 is Cisco IOS
                from .api_scripts import (CiscoIOS)
                session = CiscoIOS(device_ip)
                pass
            elif device_object.operating_system == '2':
                #Cisco IOS-XE
                from .api_scripts import (CiscoIOSXE)
                session = CiscoIOSXE(device_ip)
            elif device_object.operating_system == '3':
                # Cisco IOS-XR
                pass
            elif device_object.operating_system == '4':
                # Cisco NX-OS
                pass

        vlans_dict = session.get_vlans()
        #
        action = DataBaseActions(device_id)
        try:
            #object = DeviceDetail.objects.get(device_id_id=device_id)
            action.vlans_add_to_db(vlans_dict)
            # use update_or_create type of method without verifying device id

        #except ObjectDoesNotExist:
        #    action.create_configuration(device_config, user)
        except Exception as error:
            raise error


        return HttpResponse(status=201)
    except UnboundLocalError as error:
        raise error
    except ConnectionError as error:
        raise error


def vlan_change(deviceip, interface_type, interfaces, data_vlan_id,
                    voice_vlan_id):

    """
    """

    try:
        device_object = Devices.objects.get(id=device_id)
        #find serial number & model
        if device_object.vendor == "C":
            if device_object.operating_system == '1':
                #operating system 1 is Cisco IOS
                from .api_scripts import (CiscoIOS)
                session = CiscoIOS(device_ip)
                pass
            elif device_object.operating_system == '2':
                #Cisco IOS-XE
                from .api_scripts import (CiscoIOSXE)
                session = CiscoIOSXE(device_ip)
            elif device_object.operating_system == '3':
                # Cisco IOS-XR
                pass
            elif device_object.operating_system == '4':
                # Cisco NX-OS
                pass

        action = session.change_port_vlan_assignment(interface_type,
                                                    interfaces, data_vlan_id,
                                                    voice_vlan_id)
        return action
    except Exception as error:
        raise error



if __name__ == "__main__":
    print("Updating record")
    sync_config()
