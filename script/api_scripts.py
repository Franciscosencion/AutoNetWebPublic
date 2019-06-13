from netmiko import ConnectHandler
from netmiko.ssh_exception import (AuthenticationException,
                                    NetMikoTimeoutException)
from paramiko.ssh_exception import SSHException

class AuthenticationError(Exception):

    def __init__(self, msg):
        super().__init__(msg)

class CiscoIOSXE:
    """
    API calls in this class have been tested on Cisco IOS-XE version 16.11.01b
    Ensure software version has the same capabilities and modules for the
    calls perform in the different methods of this class.
    """
    #imports needed for class methods
    import xmltodict, os, urllib3, requests, json
    from requests.exceptions import ConnectionError
    #importing netmiko modules for nonrestful api calls

    # Setup base variable for request
    restconf_headers = {"Accept": "application/yang-data+json"}

    restconf_base = "https://{ip}:{port}/restconf/data"
    #disable self-signed certificates warning for demo
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


    def __init__(self, ip, username="developer", password="C1sco12345"):
        """initialization method"""

        self.ip = ip
        self.username = username
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
                            auth=(self.username, self.password),
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
                            auth=(self.username, self.password),
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
                        auth=(self.username, self.password),
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

    def change_port_vlan_assignment(self, interface_type, interface,
                                    data_vlan_id, voice_vlan_id):
        restconf_headers = {"Content-Type": "application/yang-data+json"}
        platform_info_url = self.restconf_base + "/Cisco-IOS-XE-native:native/interface/{interface_type}/"
        url = platform_info_url.format(ip=self.ip, port='443', interface_type=interface_type)

        data ={
            f"Cisco-IOS-XE-native:{interface_type}":
                {
                    "name": interface,
                    "switchport": {
                        "Cisco-IOS-XE-switch:access": {
                            "vlan": {
                                "vlan": data_vlan_id
                            }
                        },
                        "Cisco-IOS-XE-switch:mode": {
                            "access": {}
                        },
                        "Cisco-IOS-XE-switch:voice": {
                        "vlan": {
                            "vlan": voice_vlan_id
                        }
                        }
                    }
                }
            }

        try:
            r = self.requests.patch(url,
                            headers = restconf_headers,
                            json=data,
                            auth=(self.username, self.password),
                            verify=False)
            if r.status_code >= 200 and r.status_code <= 226:
                if r.status_code == 201:
                    return ("Created")
                elif r.status_code == 202:
                    return ("Accepted")
                elif r.status_code == 204:
                    return ("Request processed Successfully")
                else:
                    #process JSON data into Python Dictionary and use
                    return ("Request Status Code: {}".format(r.status_code))

        except AuthenticationError as error:
            raise error
        except self.requests.exceptions.RequestException as error:
            raise error




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
