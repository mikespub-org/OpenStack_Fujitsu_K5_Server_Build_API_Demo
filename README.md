# OpenStack_Fujitsu_K5_Server_Build_API_Demo
Another demo of how a virtual server can be instantiated though the OpenStack APIs on Fujitsu K5's IaaS Platform

This example requires a Fujitsu K5 or OpenStack Project to target.

It creates everything necessary to have a public login to a server.

The basics are documented on https://allthingscloud.eu

For details, refer to the example scripts and config.py.
There is also a .doc 


modifications in this repo: allow usage behind proxy. Some additional features / see sample files
Use at your own risk.
fjk5.py contains the functions needed by the demo files.
you'll need valid credentials - merge them into your local copy of config.py

Refer to the demo Files to see the scope 

Script	|Description
---|---
fjk5.py|	Main script. Contains all subroutines. If called directly,  should present a list of available operating system images.
listServers.py|	displays all server details for your contract including the clear text windows password and IP information
createKeyPair.py|	Generates a Key Pair / copy the output on to safe place (again: read API documentation)
getGlobalIP.py|	should be renamed: it lists all your global IPS and deletes the unallocated ones.
createNetwork.py|	Creates a network along the configuration in config.py
Flavors.py|	Lists all available flavors. Resizes a virtual machine. Look into fjk5 / 3 steps necessary / reboot involved
createserver.py|	Creates a new server along the configuration in config.py
Deleteserver.py|	Shows how you can delete a server by ‘name’
config.py|	Contains all your security and server parameter information. One day, credentials will be moved  out. Another day, maybe HEAT templates might get called. Didn’t research into this one yet.
firewall.py|	Creates firewall rules, a firewall policy and attaches that to all routers. Lists firewall rules. Updates existing rules from rules descripbed in config file.
Shelve/unshelve.py|	Sends a server to the shelve 



## Things to come (help wanted):
- streamline fjk5 / pythonize it and add object oriented features
- security group rules
- management of VPNs
- better handling of firewall rules:
  - Add, delete single rules
  - search for rules by properties
  - multiple firewall policies
- autoscale
- manage images and snapshots
  
=======
- firewall rule definition improved


