#!/usr/bin/python
usage = """Summary:
The following tutorial demonstrates how the native OpenStack APIs can be used to deploy a server, network, subnet and router
on the Fujitsu K5 IaaS Platform

Author: Jörg Schulz
based on work of Graham Land
Date: 27/01/17

Github: Github: https://github.com/joergK5Schulz/OpenStack_Fujitsu_K5_Server_Build_API_Demo

Modifications: Joerg.schulz (AT ) ts.fujitsu.com

creates a Server using spec in config.py.


"""

import config
import fjk5

if config.testing :
    import pdb
import listServers
import pprint

def main():
    print (usage)
    # here we get the login token as key for all other info
    k5token = fjk5.get_scoped_token()
    
    # before we start we need info about the network
    networks, status = fjk5.list_networks(k5token)
    securityGroup = fjk5.getSecurityGroup(k5token, config.securityGroup )
    
    if status < 400 :
        network = filter(lambda name: name['name'] == config.zoneInfo[config.availabilityZone]['networkName'], networks.json()['networks'])
        networkID = network[0]['id']
        print ('network %s: ' % networkID)
        # create a port
        portInfo = fjk5.create_port(k5token, networkID, fixedIP = config.serverInfo['fixedIP'])
        
        port = portInfo.json()['port'].get('id')
        # this one creates the server
        serverInfo = fjk5.create_server(k5token, port = port, serverInfo = config.serverInfo)
        print (serverInfo)
        print (serverInfo.content)
    else :
        print ("error %s: " % response.status_code)
    # next we add a public IP to that port
    extNetwork = filter(lambda name: name['name'] == config.zoneInfo[config.availabilityZone]['externalNet'], networks.json()['networks'])
    publicNetwork = fjk5.create_global_ip(k5token, extNetwork[0]['id'], port)
    
    # dispay the most important infos here: IP, vnc
    listServers.listServers(k5token)
    initPassword = fjk5.get_Serverpassword(k5token, serverInfo.json()['server']['id'])
    print (publicNetwork.json()['floatingip']['floating_ip_address'])
    pprint.pprint(initPassword)
    

    
    
    

    


if __name__ == "__main__":
    main()
