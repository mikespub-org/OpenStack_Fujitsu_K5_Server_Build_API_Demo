# OpenStack_Fujitsu_K5_Server_Build_API_Demo
Another demo of how a virtual server can be instantiated though the OpenStack APIs on Fujitsu K5's IaaS Platform

This example requires a Fujitsu K5 or OpenStack Project to target.


It creates everything necessary to have a public login to a server.

It's fully documented on https://allthingscloud.eu
modifications in this repo: allow usage behind proxy. Some additional features / see sample files
Use at your own risk.
fjk5.py contains the functions needed by createNetwork, createKeyPair, createserver, listServers.
you'll need valid credentials - merge them into your local copy of config.py
