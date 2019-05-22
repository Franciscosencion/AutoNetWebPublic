import os, datetime, re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NetAutoMgmt.settings')
import django
django.setup()
from django.http import HttpResponse
from netmiko import ConnectHandler
from netmiko.ssh_exception import (AuthenticationException,
                                    NetMikoTimeoutException)
from paramiko.ssh_exception import SSHException
from multiprocessing import Pool


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


def sync_config(device_ip, device_id):

    """
    sync_config will utilize netmiko API to connect to remote device and
    pull the configuration, after that using the values received ip and device
    id configuration will be either updated or created if it does not exist
    """
    devicedict = {"device_type": "cisco_ios", "ip": device_ip,
		          "username":"cisco", "password": "cisco", "secret": "cisco"}
    try:

        session = ConnectHandler(device_type=devicedict["device_type"],
    							 ip=devicedict["ip"],
                                 username=devicedict["username"],
    							 password=devicedict["password"],
    							 secret=devicedict["secret"],
    							 )
        with session:
            session.enable()
            config = session.send_command("show running-config")
            #device model
            device_object = Devices.objects.get(id=device_id)
            #find serial number & model
            if device_object.vendor == "C":
                # serial number goes here
                inventory = session.send_command("show inventory")
                serial_number_match = PatternFinder(r'SN.\s{0,}(9V.+)', inventory)
                serial_number_match = serial_number_match.find_match()
                # model goes here
                #inventory = session.send_command("show inventory")
                #serial_number_match = PatternFinder(r'SN.\s{0,}(FOC.+)', inventory)
                #serial_number_match = serial_number_match.find_match()


    except Exception as error:
        return None
    # except NetMikoTimeoutException as error:
    #     return HttpResponse("<h3>Connection timed out</h3>")
    # except AuthenticationException as error:
    #     return "Authentication failed. Try again."
    # except SSHException as error:
    #     return "Unable to connect via SSH. SSH enabled?"
    record_exist = None
    try:
        record_exist = DeviceDetail.objects.get(device_id_id=device_id)
    except:
        # if record does not exist variable record_exist will remain as None
        # This will result in following statement returning False and new record
        # being created.
        pass

    if record_exist:
        # update record if configuration record exist
        sync_conf = DeviceDetail.objects.filter(device_id_id=device_id).update(
                                device_config=config,
                                device_script="NA",
                                device_sn = serial_number_match[0],
                                last_modify=datetime.datetime.now())
    else:
        # create new configuration record
        sync_conf = DeviceDetail.objects.get_or_create(
                                device_config=config,
                                device_script="NA",
                                device_id_id=device_id,
                                device_sn = serial_number_match[0],
                                last_modify=datetime.datetime.now())[0]
        sync_conf.save()
    return HttpResponse(status=201)

if __name__ == "__main__":
    print("Updating record")
    sync_config()
