import os, datetime, re
from multiprocessing import Pool
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NetAutoMgmt.settings')
import django
django.setup()
from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from netmiko import ConnectHandler
from netmiko.ssh_exception import (AuthenticationException,
                                    NetMikoTimeoutException)
from paramiko.ssh_exception import SSHException
#custom modules
from main_app.models import DeviceDetail, Devices


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
    # devicedict = {"device_type": "cisco_ios", "ip": device_ip,
	# 	          "username":"cisco", "password": "cisco", "secret": "cisco"}
    # try:
    #
    #     session = ConnectHandler(device_type=devicedict["device_type"],
    # 							 ip=devicedict["ip"],
    #                              username=devicedict["username"],
    # 							 password=devicedict["password"],
    # 							 secret=devicedict["secret"],
    # 							 )
    #     with session:
    #         session.enable()
    #         config = session.send_command("show running-config")
    #         #device model
    try:
        device_object = Devices.objects.get(id=device_id)
        #find serial number & model
        if device_object.vendor == "C":
            # serial number goes here
            from .api_scripts import CiscoIOSXE
            platform_detail = CiscoIOSXE(device_ip)
            platform_defail = platform_detail.get_platform_detail()
            running_config = platform_detail.get_running_config()
            # inventory = session.send_command("show inventory")
            # serial_number_match = PatternFinder(r'SN.\s{0,}(9V.+)', inventory)
            # serial_number_match = serial_number_match.find_match()
            # model goes here
            #inventory = session.send_command("show inventory")
            #serial_number_match = PatternFinder(r'SN.\s{0,}(FOC.+)', inventory)
            #serial_number_match = serial_number_match.find_match()


    except Exception as error:
        return None

    try:
        object = DeviceDetail.objects.get(device_id_id=device_id)
        # update record if configuration record exist
        DeviceDetail.objects.filter(device_id_id=device_id).update(
                                device_config=running_config['running_config'],
                                device_script="NA",
                                modified_by = user,
                                #last_modify = timezone.now(),
                                device_model = platform_defail["model"],
                                device_sn = platform_defail["serial_number"])
        #last_modify=datetime.datetime.now()
        return HttpResponse(status=202)
    except ObjectDoesNotExist:
        # New object will be created if ObjectDoesNotExist exception triggers
        sync_conf = DeviceDetail.objects.get_or_create(
                                device_config=running_config['running_config'],
                                device_script="NA",
                                created_by = user,
                                modified_by = user,
                                last_modify = timezone.now(),
                                device_id_id=device_id,
                                device_model = platform_defail["model"],
                                device_sn = platform_defail["serial_number"])[0]
        sync_conf.save()

        return HttpResponse(status=201)
    except Exception as error:
        return HttpResponse(status=500)

if __name__ == "__main__":
    print("Updating record")
    sync_config()
