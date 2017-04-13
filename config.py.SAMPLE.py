# -*- coding: iso8859-15 -*-
"""
config.py
configuration file for k5 api. Caveat: don't upload to github without cleaning

you'll need your credentials; all other values come from your config needs
"""

import base64

testing=True

htmlProxies = {'http' : 'http://YourUserID:yourProxyPassword@YourFtsProxy:82', 'https' : 'http://yourUserID:YourProxxyPassword@mchproxya.mch.fsc.net:82'}
#htmlProxies = {}
adminUser='YourK5UserID'
adminPassword='YourK5Password'
contract='YourK5ContractNum'
region='uk-1' # or any other region
projectid='YourK5ProjectID' # might be obsolete
securityGroup = 'YourSecGroupMust Exist'
# securityGroupID = '11113222222333333'


subnetName='yourDesiredSubnetName'
subnetAddress='10.10.0.0/16' # pick it along your design
allocationPoolStart= '10.10.10.1' # pick it along your design
allocationPoolEnd='10.10.100.255' # pick it along your design
"""
basics for the availability zones
"""
availabilityZone = 'uk-1a'
# availabilityZone = 'uk-1b'
zoneInfo = { 'uk-1a' : {'externalNet'   : 'inf_az1_ext-net01',
                        'nameserver1'   : '62.60.42.9' ,
                        'nameserver2'   : '8.8.8.8',
                        'networkName'   : 'oceania-1a',
                        'routerName'    : 'oceania01-a'},
             'uk-1b' : {'externalNet'   : 'inf_az2_ext-net01',
                        'nameserver1'   : '62.60.39.9' ,
                        'nameserver2'   : '8.8.8.8',
                        'networkName'   : 'oceania-1b',
                        'routerName'    : 'oceania01-b'}
             }


key='NameOfSecretKeyPair'

firewallRules =  [  {
    "action": "allow",
    "description": "SSH",
    "destination_ip_address": "10.10.0.0/16",
    "destination_port": "22",
    "enabled": True,
    "ip_version": 4,
    "name": "ALLOW_SSH_IN",
    "protocol": "tcp",
    "source_ip_address": "0.0.0.0/0",
    "availability_zone": availabilityZone        }  , {
    "action": "allow",
    "description": "HTTPS all around",
    "destination_ip_address": "0.0.0.0/0",
    "destination_port": "443",
    "enabled": True,
    "ip_version": 4,
    "name": "ALLOW_HTTPS",
    "protocol": "tcp",
    "source_ip_address": "0.0.0.0/0",
    "availability_zone": availabilityZone        }  , {
    "action": "allow",
    "description": "DNS ",
    "destination_ip_address": "0.0.0.0/0",
    "destination_port": "53",
    "enabled": True,
    "ip_version": 4,
    "name": "ALLOW_DNS_outbound",
    "protocol": "tcp",
    "source_ip_address": "10.10.0.0/16",
    "availability_zone": availabilityZone        } , {
    "action": "allow",
    "description": "DNS UDP outbound",
    "destination_ip_address": "0.0.0.0/0",
    "destination_port": "53",
    "enabled": True,
    "ip_version": 4,
    "name": "ALLOW_DNS_UDP_out",
    "protocol": "udp",
    "source_ip_address": "10.10.0.0/16",
    "availability_zone": availabilityZone        }
                    ]

firewallPolicyName = 'Oceania01'    # not for K5, but for our context this should be unique
firewallPolicyDescription = """This is a basic firewall Policy for our demonstration purposes"""
firewallName = 'Oceania01'    # not for K5, but for our context this should be unique
firewallDescription = """This is a basic firewall for our demonstration purposes"""


# this didn't work yet. Would immediately update Ubuntu14 to 16.
initialLxUpgrade="""#!/bin/bash
sudo apt-get -y update
sudo apt-get -y upgrade
sudo do-release-upgrade -f DistUpgradeViewNonInteractive
"""

# server parameters; 
ubuntuServerInfo = {
    'name' : 'Oceania02LX',
    'imageRef' : '45895e58-e416-4b96-9576-1df6cba6e264',
    'flavorid' : '1902',
    'volumesize' : '20',
    'availabilityZone' : availabilityZone,
    'networkPortName' : networkPortName,
    'security_group_name' : securityGroup,
    'sshkey_name' : key,
    'initialPassword' : False,
    'initialScript' : initialLxUpgrade
}


serverInfo = ubuntuServerInfo
    #     serverInfo = windowsServerInfo
    


