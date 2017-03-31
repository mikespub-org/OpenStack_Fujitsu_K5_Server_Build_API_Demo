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

Refer to the demo Files to see the scope (create server, list servers, list Global IPs and remove the unused ones).

Things to come (help wanted):
- resize of machines
- security group rules
- firewall rules 
