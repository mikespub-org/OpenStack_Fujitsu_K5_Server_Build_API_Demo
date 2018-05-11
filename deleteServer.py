#!/usr/bin/python
usage = """Summary:
The following tutorial demonstrates how the native OpenStack APIs can be used to deploy a server, network, subnet and router
on the Fujitsu K5 IaaS Platform
Author: Joerg.schulz (AT )ts.fujitsu.com

calls K5 routines of Graham Land
Date: 24/03/17
Github: https://github.com/joergK5Schulz/OpenStack_Fujitsu_K5_Server_Build_API_Demo


this one: deletes a server // name from config.py
"""

import config
import fjk5

import pprint

if config.testing :
    import pdb





def main():
    print (usage)
    k5token = fjk5.get_scoped_token()
    # delete ports first
    serverID = fjk5.lookForServer (k5token, config.serverInfo['name'])[0]['id']
    for port in fjk5.getServerPorts(k5token, serverID):
            pprint.pprint (port)
            fjk5.deletePort(k5token, port['port_id'])
    result = fjk5.deleteServer(k5token,  serverID )

    
    # if config.testing: pdb.set_trace()
    print (result)
    
    
    # here we get the login token as key for all other info



if __name__ == "__main__":
    main()
