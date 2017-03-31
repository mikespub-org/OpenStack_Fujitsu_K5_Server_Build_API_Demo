#!/usr/bin/python
usage = """Summary:
The following tutorial demonstrates how the native OpenStack APIs can be used to deploy a server, network, subnet and router
on the Fujitsu K5 IaaS Platform

Author: Jörg Schulz
based on work of Graham Land
Date: 27/01/17

Github: Github: https://github.com/joergK5Schulz/OpenStack_Fujitsu_K5_Server_Build_API_Demo

Modifications: Joerg.schulz (AT ) ts.fujitsu.com
this one: list all global IPs
"""

import config
import fjk5

import pprint

def listGlobalIPs() :
    token = fjk5.get_scoped_token()
    print ("IPs defined: ")
    globalIPs = fjk5.list_globalIPs(token)
    # if config.testing: pdb.set_trace()
    for address in globalIPs :
        print('IP %s : bound to: %s ' % (address['floating_ip_address'], address['port_id']))
    # unused:
    print ("IPs available: ")
    for address in fjk5.list_unusedIPs(token) :
        print('IP %s : ID: %s  ' % (address['floating_ip_address'], address['id']))
    # we are friendly and clean up the unused ones
    fjk5.deleteUnusedGlobalIPs(token)
        


def main():
    print (usage)
    listGlobalIPs()

    
if __name__ == "__main__":
    main()
