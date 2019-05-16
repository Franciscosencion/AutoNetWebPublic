import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NetAutoMgmt.settings')
import django
django.setup()
from netmiko import ConnectHandler
from netmiko.ssh_exception import AuthenticationException, NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from multiprocessing import Pool


from main_app.models import DeviceConfig

_config = """
This is a test config run using an automated script
"""
def sync_config(device_ip, device_id):

    devicedict = {"device_type": "cisco_ios", "ip": device_ip,
		          "username":"cisco", "password": "cisco", "secret": "cisco"}
    session = ConnectHandler(device_type=devicedict["device_type"],
							 ip=devicedict["ip"], username=devicedict["username"],
							 password=devicedict["password"],
							 secret=devicedict["secret"],
							 )
    with session:
        session.enable()
        config = session.send_command("show running-config")
        sync_conf = DeviceConfig.objects.get_or_create(device_config=config,
                                                            device_script="NA",
                                                            device_id_id=device_id)[0]
        sync_conf.save()


if __name__ == "__main__":
    print("Updating record")
    sync_config()
