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
Restore system from first snapshot visible under listSnapshots..
"""


def restoreSnapshot(k5token):
    snapshots = fjk5.getSnapshots(k5token, config.projectName)
    pprint.pprint(snapshots)
    print ('beware - restoreSnapshot will destroy your server, currently)
    if config.testing:
        pdb.set_trace()
    result = fjk5.restoreSnapshot(k5token, config.projectName, snapshots['snapshots'][0]['id'])
    
    

    print result.content
    
    

def main():
    print (usage)
    k5token =  fjk5.get_scoped_token()

    restoreSnapshot(k5token)
    
    
    
    # here we get the login token as key for all other info



if __name__ == "__main__":
    main()
