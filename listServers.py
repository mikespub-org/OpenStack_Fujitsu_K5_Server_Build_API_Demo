#!/usr/bin/python
usage = """Summary:
The following tutorial demonstrates how the native OpenStack APIs can be used to deploy a server, network, subnet and router
on the Fujitsu K5 IaaS Platform
Author: Joerg.schulz (AT )ts.fujitsu.com

calls K5 routines of Graham Land
Date: 24/03/17
Github: https://github.com/joergK5Schulz/OpenStack_Fujitsu_K5_Server_Build_API_Demo


this one: listServers and search a server.
list Security Groups and print details on the one configured in config.py
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
def listServers():
    token = fjk5.get_scoped_token()
    # pdb.set_trace()
    servers = fjk5.list_servers(token)
    for server in  servers['servers']:
        print ('name: %s id %s' % (server['name'], server['id']))
        serverDetail = fjk5.getServerDetail(token, server['id'])
        pprint.pprint(serverDetail)
        for addresses in serverDetail['server']['addresses'].keys():
            for address in serverDetail['server']['addresses'][addresses] :
                print ('port %s,  IP %s'  % (addresses, address['addr']))
        for port in fjk5.getServerPorts(token, server['id']):
            pprint.pprint (port)
    
    myServer = fjk5.lookForServer (token, config.serverInfo['name'])
    # if config.testing : pdb.set_trace()
    if len ( myServer ) > 0 :
        print ('Queried Server %s has the ID %s' % (config.serverInfo['name'], myServer[0]['id']))
    else :
        print ("Server %s does not exist" % config.serverInfo['name'])

def listSecurityGroups() :
    token = fjk5.get_scoped_token()
    # pdb.set_trace()
    securityGroups = fjk5.listSecurityGroups(token, filterName = config.securityGroup)
    pprint.pprint(securityGroups)

def main():
    print (usage)
    listServers()
    listSecurityGroups()
    
    
    
    # here we get the login token as key for all other info



if __name__ == "__main__":
    main()
