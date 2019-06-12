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

    def get_running_config(self):

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

    def get_interfaces(self):

        running_config_url = self.restconf_base + "/Cisco-IOS-XE-native:native/interface"
        url = running_config_url.format(ip=self.ip, port='443')
        try:
            r = self.requests.get(url,
                        headers = self.restconf_headers,
                        auth=(self.user, self.password),
                        verify=False)
            if r.ok:
                #process JSON data into Python Dictionary and use
                #running = self.json.dumps(r.json(), indent=4)
                interface_list = dict()
                #interface_list =[f'{x}{x["name"]}' for x in r.json()['Cisco-IOS-XE-native:interface']]
                for x in r.json()['Cisco-IOS-XE-native:interface']:
                    interface_list[f'{x}'] = [f'{x}' + str(i['name']) for i in r.json()['Cisco-IOS-XE-native:interface'][x]]
                return interface_list
            elif r.status_code == 401:
                raise AuthenticationError("Invalid user name and password.")

        except self.ConnectionError as error:
            raise error
        except AuthenticationError:
            print("Authentication error yo")




class CiscoIOS:
    import re
    def __init__(self, ip, task=None, username='cisco', password='cisco'):
        self.ip = ip
        self.username = username
        self.password = password

    def main_session(self):
        """
        Method callable to establish the SSH session
        """
        cisco_ios_parameters = {"device_type": "cisco_ios",
                                "ip": self.ip,
            		            "username":self.username,
                                "password": self.password,
                                "secret": self.password}


        return ConnectHandler(**cisco_ios_parameters)

    def get_platform_detail(self):
        """
        Method used to pull device platform details such serial number and model
        """
        try:
            session = self.main_session()
            with session:
                session.enable()
                output = session.send_command('show inventory')
                pattern = self.re.compile(r'[PIDpid]+:\s+([A-Za-z0-9]+).*[SsNn:]+\s+([0-9A-Za-z]+).*')
                match = pattern.finditer(output)
                #print(match)
                for i in match:
                    model, serial = i.group(1, 2)
                    if model and serial:
                        break

            return {'model': model, 'serial_number': serial}
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

    def get_running_config(self):
        """
        This method is used to retrieve unstructured running configuration
        """
        try:
            session = self.main_session()

            with session:
                session.enable()
                running_config = session.send_command("show running-config")
            config = {"running_config": running_config}
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
