from netmiko import ConnectHandler
from netmiko.ssh_exception import (AuthenticationException,
                                    NetMikoTimeoutException)
from paramiko.ssh_exception import SSHException

class AuthenticationError(Exception):

    def __init__(self, msg):
        super().__init__(msg)

class CiscoIOSXE:

    #imports needed for class methods
    import xmltodict, os, urllib3, requests, json
    from requests.exceptions import ConnectionError
    #importing netmiko modules for nonrestful api calls

    # Setup base variable for request
    restconf_headers = {"Accept": "application/yang-data+json"}
    restconf_base = "https://{ip}:{port}/restconf/data"
    #disable self-signed certificates warning for demo
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


    def __init__(self, ip, user="cisco", password="cisco"):
        """initialization method"""

        self.ip = ip
        self.user = user
        self.password = password

    def get_platform_detail(self):
        """This method will pull both the platform model as well as
        platform serial number and return them in a dictionary
        """
        platform_info_url = self.restconf_base + "/Cisco-IOS-XE-native:native/license/udi"
        url = platform_info_url.format(ip=self.ip, port='443')
        try:
            r = self.requests.get(url,
                            headers = self.restconf_headers,
                            auth=(self.user, self.password),
                            verify=False)
            if r.ok:
                #process JSON data into Python Dictionary and use
                return {'model': r.json()["Cisco-IOS-XE-native:udi"]['pid'],
                    'serial_number':r.json()["Cisco-IOS-XE-native:udi"]['sn']}

            elif r.status_code == 401:
                raise AuthenticationError("Invalid user name and password.")
        except self.ConnectionError as error:
            raise error
        except AuthenticationError as error:
            raise error

    def get_running_config_structured(self):

        running_config_url = self.restconf_base + "/Cisco-IOS-XE-native:native"
        url = running_config_url.format(ip=self.ip, port='443')
        try:
            r = self.requests.get(url,
                            headers = self.restconf_headers,
                            auth=(self.user, self.password),
                            verify=False)
            if r.ok:
                #process JSON data into Python Dictionary and use
                running = self.json.dumps(r.json(), indent=True)
                #print(running)
                return {'running_config': running}
            elif r.status_code == 401:
                raise AuthenticationError("Invalid user name and password.")
        except self.ConnectionError as error:
            raise error
        except AuthenticationError as error:
            raise error

    def get_running_config_unstructured(self):
        """
        This method is used to retrieve unstructured running configuration
        """

        try:
            cisco_ios_parameters = {"device_type": "cisco_ios",
                                    "ip": self.ip,
                		            "username":self.user,
                                    "password": self.password,
                                    "secret": self.password}

            session = ConnectHandler(**cisco_ios_parameters)

            with session:
                session.enable()
                running_config = session.send_command("show running-config")
            config = {"unconstructed_config": running_config}
            return config
        except AuthenticationException as error:
            #this will raise authentication error when wrong credentials are
            #provided
            raise error
        except NetMikoTimeoutException as error:
            #this will raise a connection timeout exception when device is
            #unreachable
            raise error
        except SSHException as error:
            #this will raise an  SSH service exception when unable to establish
            #an SSH session
            raise error
