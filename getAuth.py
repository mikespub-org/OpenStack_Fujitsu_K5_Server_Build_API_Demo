#!/usr/bin/python
usage = """Summary:
The following tutorial demonstrates how the native OpenStack APIs can be used to deploy a server, network, subnet and router
on the Fujitsu K5 IaaS Platform
Author: Joerg.schulz (AT )ts.fujitsu.com

calls K5 routines of Graham Land
Date: 24/03/17
Github: https://github.com/joergK5Schulz/OpenStack_Fujitsu_K5_Server_Build_API_Demo


this one: list authentication stuff.
"""

import config
import fjk5

import pprint

if config.testing :
    import pdb

"""
prints some auth and project info
"""
def printAuthInfo():
    
    k5UnscopedToken = fjk5.getUnscopedToken()
    # list available endpoints / URLs
    pprint.pprint(fjk5.getEndpointDict(k5UnscopedToken))
    projectsForUser = fjk5.listProjectsForUser(k5UnscopedToken)
    pprint.pprint(projectsForUser)
    if config.testing: pdb.set_trace()
    configuredProject =  filter(lambda project: project['name'] == config.projectName, projectsForUser['projects'])[0]
    pprint.pprint(configuredProject)
    
    


    
    if config.testing:
        # pprint.pprint(k5UnscopedToken.json())
        pdb.set_trace()
        pprint.pprint(fjk5.get_scoped_token().json())

def main():
    print (usage)
    printAuthInfo()
    

    
    # 
    
    
    



if __name__ == "__main__":
    main()
