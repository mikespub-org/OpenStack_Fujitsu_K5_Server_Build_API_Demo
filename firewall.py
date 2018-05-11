#!/usr/bin/python
usage = """Summary:
The following tutorial demonstrates how the native OpenStack APIs can be used to deploy a server, network, subnet and router
on the Fujitsu K5 IaaS Platform
Author: Joerg.schulz (AT )ts.fujitsu.com

calls K5 routines of Graham Land
Date: 24/03/17
Github: https://github.com/joergK5Schulz/OpenStack_Fujitsu_K5_Server_Build_API_Demo


this one: list and (later) possibly create a firewall.
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
def listFirewalls(k5token):
    
    firewalls = fjk5.listFirewalls(k5token)
    for firewall in  firewalls :
        #pdb.set_trace()
        pprint.pprint(firewall)
    policies = fjk5.listFirewallPolicies(k5token)
    pprint.pprint(policies)
    rules = fjk5.listFirewallRules(k5token)
    for rule in  rules :
        #pdb.set_trace()
        pprint.pprint(rule)
    # if config.testing: pdb.set_trace()



def main():
    print (usage)
    k5token = fjk5.get_scoped_token()
    listFirewalls(k5token)
    if config.testing: pdb.set_trace()
    ruleIDs = fjk5.createFirewallRules(k5token, config.firewallRules) # creates rules as defined in config
    
    
    # create firewall policy with all these rules
    policy = fjk5.createFirewallPolicy(k5token = k5token, rules = ruleIDs)
    if config.testing: pdb.set_trace()
    firewall = fjk5.createFirewall(k5token = k5token, policy = policy['id'])
    # create firewall for the router defined in config with all these rules
    if config.testing: pdb.set_trace()
    listFirewalls(k5token)
    # 
    
    
    



if __name__ == "__main__":
    main()
