#!/usr/bin/python
usage = """Summary:
The following tutorial demonstrates how the native OpenStack APIs can be used to deploy a server, network, subnet and router
on the Fujitsu K5 IaaS Platform
Author: Joerg.schulz (AT )ts.fujitsu.com

calls K5 routines of Graham Land
Date: 24/03/17
Github: https://github.com/joergK5Schulz/OpenStack_Fujitsu_K5_Server_Build_API_Demo


this one: UNshelves a server.

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
def shelveServer():
    k5token = fjk5.get_scoped_token()
    myServer = fjk5.lookForServer (k5token, config.serverInfo['name'])
    if len ( myServer ) > 0 :
        print ('Queried Server %s has the ID %s' % (config.serverInfo['name'], myServer[0]['id']))
    else :
        print ("Server %s does not exist" % config.serverInfo['name'])
    result = fjk5.shelveUnshelveServer(k5token, myServer[0]['id'], 'unshelve')



def main():
    print (usage)
    shelveServer()
    
    
    
    # here we get the login token as key for all other info



if __name__ == "__main__":
    main()
