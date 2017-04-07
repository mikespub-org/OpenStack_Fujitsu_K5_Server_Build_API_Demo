#!/usr/bin/python
usage = """Summary:
The following tutorial demonstrates how the native OpenStack APIs can be used to deploy a server, network, subnet and router
on the Fujitsu K5 IaaS Platform
Author: Joerg.schulz (AT )ts.fujitsu.com

calls K5 routines of Graham Land
Date: 24/03/17
Github: https://github.com/joergK5Schulz/OpenStack_Fujitsu_K5_Server_Build_API_Demo


this one: list flavors and manipulate flavor of a server.
"""

import config
import fjk5

import pprint

if config.testing :
    import pdb

"""
lists all servers for contract defined in config.
To search for a server, you would impose  a lambda on the servers[] array below.
"""
def listFlavors():
    token = fjk5.get_scoped_token()
    flavors = fjk5.list_flavors(token)
    for flavor in  flavors :
        # print ('name: %s id %s ram: %s vcpus %s'% (flavor['name'], flavor['id'], flavor['ram'], flavor['vcpus']))
        # as opposed to the doc, details are not specified here
        flavorDetail = fjk5.getFlavorDetail(token, flavor['id'])['flavor']
        print ('flavor: %s id %s  ram: %s vcpus %s' % (flavor['name'], flavor['id'], flavorDetail['ram'], flavorDetail['vcpus']))# pprint.pprint(flavor)
    if config.testing: pdb.set_trace()

def main():
    print (usage)
    listFlavors()
    
    
    
    # here we get the login token as key for all other info



if __name__ == "__main__":
    main()
