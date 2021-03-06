#!/usr/bin/python
"""Summary:
The following tutorial demonstrates how the native OpenStack APIs can be used to deploy a server, network, subnet and router
on the Fujitsu K5 IaaS Platform

Author: Graham Land
Date: 27/01/17
Twitter: @allthingsclowd
Github: Github: https://github.com/joergK5Schulz/OpenStack_Fujitsu_K5_Server_Build_API_Demo
Blog: https://allthingscloud.eu

Modifications: Joerg.schulz@ts.fujitsu.com
- proxy

Import this file to use its functions.
main() below just displays a list of available flavors.
"""

# here your local data can be configured
import config

import requests
import sys
import json
import pprint
import base64

if config.testing :
    import pdb


"""
Endpoint: the URL to be called by subroutines
"""


def getEndpointDict(k5token) :
    endpoints = {}
    for ep in k5token.json()['token']['catalog']:
        for endpoint in ep['endpoints']:
            endpoints[endpoint['name']] = endpoint['url']
    return endpoints

def get_endpoint(k5token, endpoint_type):
    return getEndpointDict(k5token)[endpoint_type]



"""
This token is needed to call the API functions. Valid for some minutes, so get this for every significant step.
This one is unscoped - if your projectID is unknown, you have to retrieve it later
"""
def getUnscopedToken(adminUser = config.adminUser ,
                     adminPassword= config.adminPassword,
                     contract = config.contract,
                     region = config.region):
    identityURL = getAuthTokenUrl(region)
    try:
        response = requests.post(identityURL,
                                 headers = {'Content-Type': 'application/json', 
                                           'Accept': 'application/json'},
                                 proxies=config.htmlProxies,
                                 json={"auth":
                                         {"identity":
                                          {"methods": ["password"], "password":
                                           {"user":
                                           {"domain":
                                               {"name": contract},
                                            "name": adminUser,
                                            "password": adminPassword
                                            }}},
                                          }})
        return response
    except:
        return 'Token Scoping Failure'

"""
returns the projectID (tenant_id) 
"""
def getProjectID(name) :
    k5UnscopedToken = getUnscopedToken()
    configuredProject =  filter(lambda project: project['name'] == name, listProjectsForUser(k5UnscopedToken)['projects'])[0]
    return configuredProject['id']


"""
This token is needed to call the API functions. Valid for some minutes, so get this for every significant step.
"""
def get_scoped_token(adminUser = config.adminUser ,
                     adminPassword= config.adminPassword,
                     contract = config.contract,region = config.region):
    identityURL = 'https://identity.' + region + \
        '.cloud.global.fujitsu.com/v3/auth/tokens'
    # we need to find the projectID, therefore we need an unscoped token:
    projectID = getProjectID(config.projectName) 
    try:
        response = requests.post(identityURL,
                                 headers = {'Content-Type': 'application/json', 
                                           'Accept': 'application/json'},
                                 proxies=config.htmlProxies,
                                 json={"auth":
                                         {"identity":
                                          {"methods": ["password"], "password":
                                           {"user":
                                           {"domain":
                                               {"name": contract},
                                            "name": adminUser,
                                            "password": adminPassword
                                            }}},
                                          "scope":
                                          {"project":
                                           {"id": projectID
                                            }}}})
        return response
    except:
        return 'Regional Project Token Scoping Failure'

    

"""
creates a new network
"""
def create_network(k5token, name = config.zoneInfo[config.availabilityZone]['networkName'] , availability_zone = config.availabilityZone):
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/networks')
    print networkURL
    
    try:
        response = requests.post(networkURL,
                                 headers=getStandardHeader(k5token),
                                 proxies=config.htmlProxies,
                                 json={
                                            "network":
                                            {
                                              "name": name,
                                              "admin_state_up": True,
                                              "availability_zone": availability_zone
                                             }
                                        })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

"""
create the subnet to use within your servers. Additional parameters for routing, DHCP!
"""
def create_subnet(k5token,
                  netid,
                  name = config.subnetName,
                  cidr=config.subnetAddress,
                  allocationPoolStart = config.allocationPoolStart,
                  allocationPoolEnd = config.allocationPoolEnd,
                  defaultRoute = config.defaultRoute,
                  availability_zone = config.availabilityZone, ns1 = config.zoneInfo[config.availabilityZone]['nameserver1']  , ns2 = config.zoneInfo[config.availabilityZone]['nameserver2']):
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/subnets')
    try:
        response = requests.post(networkURL,
                                headers=getStandardHeader(k5token),
                                proxies=config.htmlProxies,
                                json={
                                             "subnet": {
                                                 "name": name,
                                                 "network_id": netid,
                                                  "dns_nameservers": [ ns1,ns2 ],
                                                 "host_routes":[ {  "destination":"0.0.0.0/0",  "nexthop": defaultRoute }],
                                                 "ip_version": 4,
                                                  "allocation_pools": [ { "start": allocationPoolStart,
                                                                          "end": allocationPoolEnd }        ], 
                                                 "cidr": cidr,
                                                 "availability_zone": availability_zone
                                             }
                                            })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())




"""
Virtual router. 
"""
def create_router(k5token, name = config.zoneInfo[config.availabilityZone]['routerName'], availability_zone = config.availabilityZone ):
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/routers')
    print networkURL
    try:
        response = requests.post(networkURL,
                                headers=getStandardHeader(k5token),
                                proxies=config.htmlProxies,
                                json={
                                          "router": {
                                               "name": name,
                                               "admin_state_up": True,
                                               "availability_zone": availability_zone,
                                               
                                          }})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

"""
this one connecty your router with the correct external network. 
"""
def update_router_gateway(k5token, router_id, network_id):
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/routers/') + router_id
    print networkURL
    try:
        response = requests.put(networkURL,
                                headers=getStandardHeader(k5token),
                                proxies=config.htmlProxies,
                                json={"router": {
                                    "external_gateway_info": {
                                        "network_id": network_id
                                        }
                                    }})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def add_interface_to_router(k5token, router_id, subnet_id):
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/routers/') + router_id + '/add_router_interface'
    try:
        response = requests.put(networkURL, headers=getStandardHeader(k5token),
                                proxies=config.htmlProxies,
                                json={
                                    "subnet_id": subnet_id})
        return response
    except:
        print('error adding interface to router')
        if config.testing: pdb.set_trace()
        return ("\nUnexpected error:", sys.exc_info())


"""
creates a security group, not yet demoed here
"""
def create_security_group(k5token, name, description):
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/security-groups')
    try:
        response = requests.post(networkURL, headers=getStandardHeader(k5token),
                                 proxies=config.htmlProxies,
                                 json={
                                        "security_group": {
                                            "name": name,
                                            "description": description
                                            }
                                        })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

"""
get a json object for a security group by name
"""
def getSecurityGroup(token, name):
    securityGroups, result = list_securityGroups(token)
    # if config.testing: pdb.set_trace()
    if result < 400:
        # don't ask me why the lambda doesn't accept the parameter above
        return eval ("filter(lambda name: name['name'] == '" + name + "', securityGroups.json()['security_groups'])")[0]
        # return filter(lambda name: name['name'] == name, securityGroups.json()['security_groups'])[0]
    else: return False

"""
add a rule for the security group. Not yet demoed here.
"""
def create_security_group_rule(k5token, security_group_id, direction, portmin, portmax, protocol):
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/security-group-rules')
    try:
        response = requests.post(networkURL, headers=getStandardHeader(k5token),
                                 proxies=config.htmlProxies,
                                 json={
                                        "security_group_rule": {
                                            "direction": direction,
                                            "port_range_min": portmin,
                                            "ethertype": "IPv4",
                                            "port_range_max": portmax,
                                            "protocol": protocol,
                                            "security_group_id": security_group_id
                                            }
                                        })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())



def create_port(k5token, network_id,  availability_zone = config.availabilityZone , name = config.networkPortName, fixedIP = False):
    """
    create a port for your new server.
    """
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/ports')
    # security groups should contain default, else some things will fail during setup (like login credentials). YOu can remove it later if you wish.
    # we look for the one configured in config. shouldn't break when emtpy. 
    configuredSecurityGroups = listSecurityGroups(k5token, filterName = config.securityGroup)
    securityGroups = [configuredSecurityGroups[0]['id']] if len(configuredSecurityGroups) > 0 else  []
    defaultSecurityGroup = getSecurityGroup(k5token, 'default')
    # default1aGroup = getSecurityGroup(k5token, 'secgroup-1a')
    securityGroups.append(defaultSecurityGroup['id'])
    ### securityGroups.append( getSecurityGroup(k5token, 'secgroup-1a')['id'])
    portInfo = {"network_id": network_id,
                "name": name,
                "availability_zone": availability_zone,
                "security_groups": securityGroups }
    if fixedIP: # look for a subnet and assign IP there
        # subnet = getSubnets(k5token, network_id)[0]
        # portInfo['fixed_ips'] = {  "subnet_id": subnet, "ip_address": fixedIP}
        portInfo['fixed_ips'] = [ {   "ip_address": fixedIP }  ]
    try:
        response = requests.post(networkURL, headers=getStandardHeader(k5token),
                                 proxies=config.htmlProxies,
                                 json={"port": portInfo})
        if config.testing: pdb.set_trace()
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


"""
this PRINTS the new keypair. Don't forget to save it - you'll need it for login.
"""
def create_keypair(k5token, keypair_name = config.key, availability_zone = config.availabilityZone):
    computeURL = unicode(get_endpoint(k5token, "compute")) + unicode('/os-keypairs')
    try:
        response = requests.post(computeURL,headers=getStandardHeader(k5token),
                                proxies=config.htmlProxies,
                                json={
                                    "keypair": {
                                        "name": keypair_name,
                                        "availability_zone": availability_zone
                                        }})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


"""
create a server with DHCP from data in config.
You'll need a PORT. We couldn't get it working by just specifying the network.
For lazy people: instead of deriving the ps from the .pem (where I failed yet), you can provide a password.
This is transferred and stored in clear text, so please change it.
"""
def create_server(k5token,
                port,
                serverInfo ):
    computeURL = getComputeURL(k5token)
    # one could generate this more dynamically, i.e., when parameters are not given: not add them to the dictionary.
    serverDefinition = { "server": {  "name": serverInfo['name'],
                                      "imageRef":  serverInfo['imageRef'],
                                      "flavorRef": serverInfo['flavorid'],
                                      "key_name": serverInfo['sshkey_name'],
                                      "networks": [{"port": port}],
                                      "security_groups": [{ "name":   serverInfo['security_group_name']} ,
                                                          {"name" : "default"},
                                                          {"name" : "secgroup-1a"}],
                                      "availability_zone" : serverInfo['availabilityZone'], 
                                      "block_device_mapping_v2": [{"device_name": "/dev/vda",
                                                                   "source_type": "image",
                                                                   "destination_type": "volume",
                                                                   "volume_size": serverInfo['volumesize'],
                                                                   "boot_index": "0",
                                                                   "uuid": serverInfo['imageRef'], 
                                                                   "delete_on_termination": "True"   },  ] } }
    if serverInfo['initialPassword']: # this is the workaround for windows login instead of the complicated way deriving the password from the key generated above. Stored in clear Text, change it!
        serverDefinition['server']['metadata'] =  {"admin_pass": serverInfo['initialPassword']}
    if serverInfo['initialScript']: # this will configure your server for your needs
        serverDefinition['server']['user_data'] = base64.b64encode(serverInfo['initialScript'])
    try:
        response = requests.post(computeURL, headers=getStandardHeader(k5token),
                                proxies=config.htmlProxies,
                                json=serverDefinition)

        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

"""
get the URL for networking operations
"""
def get_networkURL (k5token):
    return unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/networks')


def getNetworkDetailURL (k5token, networkID):
    """
    get the URL for network details for 1 network
    """
    return unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/networks/') + networkID
    

"""
get the URL for networking operations
"""
def get_routerURL (k5token):
    return unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/routers')

"""
get the URL for security groups
"""
def get_securityUrl (k5token):
    return unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/security-groups')

   
"""
return a json list of all security groups
"""
def list_securityGroups(token) :
    url = get_securityUrl(token)
    return list_something(token, url)

"""
return a json list of all routers
"""
def list_routers(token):
    routerURL = get_routerURL(token)
    return list_something(token, routerURL)


"""
fed up of repeating the same code? use this stub
"""
def getStandardHeader(k5token) :
    return { 'X-Auth-Token': k5token.headers['X-Subject-Token'],
             'Content-Type': 'application/json',
             'Accept': 'application/json'}

# helper functions for the list_functions
def getAuthTokenUrl(region) :
    return u'https://identity.' + region + u'.cloud.global.fujitsu.com/v3/auth/tokens'

def getComputeURL(token):
    return unicode(get_endpoint(token, "compute")) + unicode('/servers')

def getServerDetailURL(token, serverID):
    return unicode(get_endpoint(token, "compute")) + unicode('/servers/') + serverID

def getServerActionURL(token, serverID):
    return unicode(get_endpoint(token, "compute")) + unicode('/servers/') + serverID+ u'/action'

def getServerPortURL(token, serverID):
    return unicode(get_endpoint(token, "compute")) + unicode('/servers/') + serverID + u'/os-interface'

def getFlavorsUrl(token):
    return unicode(get_endpoint(token, u"compute")) +u'/flavors'

def get_flavorDetailURL(token, flavor):
    return unicode(get_endpoint(token, u"compute")) +u'/flavors/' + flavor

def getImagesUrl(token):
    return unicode(get_endpoint(token, u"compute")) +u'/images/detail'

def getServerPasswordURL(token, serverID):
    return unicode(get_endpoint(token, "compute")) + unicode('/servers/') + serverID + u'/os-server-password'

def get_globalIPURL (k5token):
    return unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/floatingips')

def getFirewallURL(k5token):
    return unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/fw')

def getFirewallsURL(k5token):
    return getFirewallURL(k5token) + u'/firewalls'

def getFirewallRulesURL(k5token):
    return getFirewallURL(k5token) + u'/firewall_rules'

def getFirewallRuleDetailsURL(k5token, ruleID):
    return getFirewallURL(k5token) + u'/firewall_rules/' + ruleID

def getFirewallPoliciesURL(k5token):
    return getFirewallURL(k5token) + u'/firewall_policies'

def getFirewallPoliciesUpdateURL(k5token, policyID):
    return getFirewallURL(k5token) + u'/firewall_policies/' + policyID

def getSecurityGroupsURL(k5token) :
    return unicode(get_endpoint(k5token, "networking")) + u'/v2.0/security-groups'

def getProjectsForUserURL(k5token):
    return get_endpoint(k5token, 'identityv3') + u'/users/' + k5token.json()['token']['user']['id'] + u'/projects'

def getStorageURL(k5token, projectName = config.projectName) :
     return get_endpoint(k5token, "blockstoragev2" ) + "/snapshots"#+  "/v2/" +  getProjectID(projectName)

def getStorageActionURL (k5token, projectName, snapshotID ) :
    return getStorageURL(k5token, projectName) + u'/' + snapshotID + u'/action'

def getPortDetailURL(k5token, projectName = config.projectName, portID = False) :
     return unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/ports/') + portID

"""
return info on a generic subject
works with networks, routers, ...
"""
def list_something(k5token, url):
    # if config.testing: print (url)
    try:
        response = requests.get(url,
                                headers=getStandardHeader(k5token),
                                proxies=config.htmlProxies)
        return response, response.status_code
    except:
        return ("\nUnexpected error:", sys.exc_info()), -1
    return false
 

"""
return a json list of all servers
"""
def list_servers(k5token):
    url = getComputeURL(k5token)
    return list_something(k5token, url)[0].json()
    
"""
returns some of the server Details
"""
def getServerDetail(k5token, serverID) :
    url = getServerDetailURL(k5token, serverID)
    return list_something(k5token, url)[0].json()

"""
lists snapshots for current project
"""
def getSnapshots(k5token, projectName) :
    url = getStorageURL (k5token, projectName )
    return list_something(k5token, url)[0].json()


"""
restores snapshot for current project
"""
def restoreSnapshot(k5token, projectName, snapshotID) :
    url = getStorageActionURL (k5token, projectName, snapshotID )
    response = requests.post(url, headers = getStandardHeader(k5token),
                             proxies=config.htmlProxies,
                             json = {  "fcx-restore": {}  }   )
    return response

"""
sends a server to deactivated. Action: [shelve|unshelve]
"""
def shelveUnshelveServer(k5token, serverID, action) :
    url = getServerActionURL(k5token, serverID)
    response = requests.post(url, headers = getStandardHeader(k5token),
                             proxies=config.htmlProxies,
                             json = { action : False }   )
    return response
                             

"""
returns information about the server Ports
"""
def getServerPorts(token, serverID):
    return list_something(token, getServerPortURL(token, serverID))[0].json()['interfaceAttachments']
     
def get_Serverpassword(token, serverID):
    return list_something(token, getServerPasswordURL(token, serverID))[0].json()['password']    
    
"""
list all our known networks
"""
def list_networks(token):
    return list_something(token, get_networkURL(token))


def getSubnets(token, networkID) : 
    """
    list all subnets for the given network
    """
    networkInfo = list_something(token, getNetworkDetailURL(token, networkID))
    subnets = networkInfo[0].json()['network']['subnets']
    return subnets

"""
list all our own global IPs
"""
def list_globalIPs(token):
    return list_something(token, get_globalIPURL(token))[0].json()['floatingips']

"""
list all our own unused IPs
"""
def list_unusedIPs(token):
    addresses = list_globalIPs(token)
    # if config.testing:pdb.set_trace()
    unused = filter(lambda address: address['port_id'] == None, addresses)
    return unused

"""
Just try a resize. No sanity checking, no result checking yet.
"""
def resizeServer(k5token, serverID, flavor) :
    resizeURL = getServerActionURL(k5token, serverID)
    response = requests.post(resizeURL,headers=getStandardHeader(k5token),
                                proxies=config.htmlProxies,
                                json={  "resize": {  "flavorRef": flavor } } )
    print ("response is %s - verifying ...." % response.status_code)
    
    serverStatus = getServerDetail(k5token, serverID)['server']['status']
    verify = (serverStatus == u'VERIFY_RESIZE')
    if verify:
        response = requests.post(resizeURL,headers=getStandardHeader(k5token),
                                proxies=config.htmlProxies,
                                json= { "confirmResize": 0 } )
    return response

"""
housekeeping: Delete a server. Without asking.
"""
def deleteServer(k5token, serverID) :
    deleteURL = getServerDetailURL (k5token, serverID)
    response = requests.delete(deleteURL,headers=getStandardHeader(k5token),
                                proxies=config.htmlProxies )
    return response


"""
lists available details for the flavorID
"""
def getFlavorDetail(token, flavor):
    return list_something(token, get_flavorDetailURL(token, flavor))[0].json()

"""
dynamic global IP for server
"""
def create_global_ip(k5token, ext_network_id, port_id, availability_zone = config.availabilityZone ):
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/floatingips')
    print (networkURL)
    # token = 
    try:
        response = requests.post(networkURL, headers=getStandardHeader(k5token),
                                proxies=config.htmlProxies,
                                json={
                                             "floatingip": {
                                                     "floating_network_id": ext_network_id,
                                                     "port_id": port_id,
                                                     "availability_zone": availability_zone
                                                     },
                                            })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())



def deleteGlobalIP(k5token, globalIpId):
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/floatingips/') + globalIpId
    if config.testing: print (networkURL)
    
    try:
        response = requests.delete(networkURL,headers=getStandardHeader(k5token),
                                    proxies=config.htmlProxies)
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())
        
    
    

"""
delete unused global IPs
"""
def deleteUnusedGlobalIPs(k5token):
    for address in list_unusedIPs(k5token) :
        response = deleteGlobalIP(k5token, address['id'])
        if response.status_code == 204: print ('deleted IP %s ' % (address['floating_ip_address']) )


def deletePort(k5token, portID):
    """
    delete specified port.
    """
    portURL = getPortDetailURL(k5token, portID = portID)
    
    try:
        response = requests.delete(portURL,headers=getStandardHeader(k5token),
                                    proxies=config.htmlProxies)
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())
        
 



"""
projects for user by userID
"""
def listProjectsForUser(k5token):
    url = getProjectsForUserURL(k5token)
    return list_something(k5token, url)[0].json()

"""
display a list of available ACTIVE images. Secondly, a demo on how to filter/search this list.
"""
def list_images(token, filterName = False) :
    url = getImagesUrl(token)
    images = list_something(token, url)[0].json()['images']
    activeImages = filter(lambda image: image['status'] == 'ACTIVE', images)
    if filterName :
        activeImages = filter(lambda image: image['name'] == filterName, activeImages)
    return activeImages

"""
display a list of available flavors.
"""
def list_flavors(token, filterName = False) :
    url = getFlavorsUrl(token)
    flavors = list_something(token, url)[0].json()['flavors']
    if filterName :
        flavors = filter(lambda image: image['name'] == filterName, activeFlavors)
    return flavors


"""
looks for a specific server by name
"""
def lookForServer (token, name):
    servers = list_servers(token)
    myServer = eval ("filter(lambda server: server['name'] == '" +  name + "', servers['servers'])")
    return myServer

"""
security groupss
"""
def listSecurityGroups(k5token, filterName = False) :
    url = getSecurityGroupsURL(k5token)
    securityGroups = list_something(k5token, url)[0].json()['security_groups']
    if filterName:
        securityGroups = filter(lambda sg: sg['name'] == filterName, securityGroups)
    return securityGroups

"""
Firewall stubs
"""
def listFirewalls(k5token, filterName = False) :
    url = getFirewallsURL(k5token)
    firewalls = list_something(k5token, url)[0].json()['firewalls']
    if filterName:
        firewalls = filter(lambda fw: fw['name'] == filterName, firewalls)
    return firewalls

"""
returns array of firewall policies
"""
def listFirewallPolicies(k5token, filterName = False):
    url = getFirewallPoliciesURL(k5token)
    policies = list_something(k5token, url)[0].json()['firewall_policies']
    if filterName:
        policies = filter(lambda rule: rule['name'] == filterName, policies)
    return policies 

"""
lists FirewallRules. If name is given, only rules with given name.
"""
def listFirewallRules(k5token, filterName = False) :
    url = getFirewallRulesURL(k5token)
    rules = list_something(k5token, url)[0].json()['firewall_rules']
    # if config.testing: pdb.set_trace()
    if filterName:
        rules = filter(lambda rule: rule['name'] == filterName, rules)
    return rules #

def createFirewallRules(k5token, rules) :
    
    ruleIDs = []
    for rule in rules:
        try:
            # only add rule if no such rule by name
            existingRules = listFirewallRules(k5token, rule['name'])
            if len(existingRules) == 0:
                response = requests.post(getFirewallRulesURL(k5token),
                                         headers=getStandardHeader(k5token),
                                         proxies=config.htmlProxies,
                                         json={"firewall_rule": rule} )
                ruleIDs.append(response.json()['firewall_rule']['id'])
                if config.testing:
                    print ('creating rule %s' % rule['name'])
            else: # update rule
                if config.testing:
                    print ('modifying rule %s' % rule['name'])
                    # pdb.set_trace()
                del(rule['availability_zone']) ## these members must not be changed.
                del(rule['ip_version'])
                url = getFirewallRuleDetailsURL(k5token, existingRules[0]['id'])
                response = requests.put(url, headers = getStandardHeader(k5token), proxies = config.htmlProxies, json = {"firewall_rule": rule}  )
                
                ruleIDs.append(existingRules[0]['id'])
                
                    
            if config.testing:
                    pprint.pprint(response.content)
        except:
            print(response.content)
            if config.testing:pdb.set_trace()
            return ("\nUnexpected error:", sys.exc_info())
    
    return ruleIDs 




"""
this one creates a firewall policy along definition in config.
It returns the json information on this policy.
If there already is a policy with 'name', it will be updated.
"""
def createFirewallPolicy (k5token, rules = [],
                          name = config.firewallPolicyName,
                          description = config.firewallPolicyDescription, 
                          availabilityZone = config.availabilityZone ) :
    json = {"firewall_policy": { "firewall_rules": rules,
                                 "name": name,
                                 "description" : description } }
    try :
        existingPolicies = listFirewallPolicies(k5token, name)
        if len (existingPolicies) > 0 : # don't create duplicates, but update the policy
            url = getFirewallPoliciesUpdateURL(k5token, existingPolicies[0]['id'])
            if config.testing: pdb.set_trace()
            policy = requests.put(url, headers = getStandardHeader(k5token), proxies = config.htmlProxies, json = json  )
            
        else:
            json['firewall_policy']['availability_zone'] =  availabilityZone
            url = getFirewallPoliciesURL(k5token)
            policy = requests.post(url, headers = getStandardHeader(k5token), proxies = config.htmlProxies, json = json  )
        
        
    except:
        return ("\nUnexpected error:", sys.exc_info())
    if policy.status_code < 400 :
        return policy.json()['firewall_policy']
    else :
        print (policy.content)
        return ("\nUnexpected error:", policy.content)
        
    
    
"""
creates a firewall and attaches it to all routers (no router parameter given)
"""
def createFirewall (k5token, policy ,
                          name = config.firewallName,
                          description = config.firewallDescription, 
                          availabilityZone = config.availabilityZone ) :
    if config.testing:
            pdb.set_trace()
    url = getFirewallsURL(k5token)
    try :
        
        existingFirewalls = listFirewalls(k5token, name)
        if len (existingFirewalls) > 0 : # don't create duplicates
            return existingFirewalls[0]
        fw = requests.post(url,headers=getStandardHeader(k5token),
                           proxies=config.htmlProxies,
                           json={"firewall": { "firewall_policy_id": policy,
                                 "name": name,
                                 "description" : description, 
                                 "availability_zone" : availabilityZone} } )
        if config.testing: pdb.set_trace()
    except:
        return ("\nUnexpected error:", sys.exc_info())
    if fw.status_code < 400 :
        return fw.json()['firewall']
    else :
        print (fw.content)
        return ("\nUnexpected error:", fw.content)
        



usage = """
demoes some of the main functions.
please peak into this code for doc, or use the accompanying snippets
"""

def main():
    print (usage)
    ## these are only for testing..
    token = get_scoped_token()
    print ("Images available: ")
    activeImages = list_images(token)
    for image in activeImages:
        print('Image "%s" : ID: "%s" : MinDisk %s' %(image['name'], image['id'], image['minDisk']))
    image = list_images(token, u'Windows Server 2012 R2 SE 64bit + SQL Server 2014 SE SP2 (English) 01')[0]
    print('WindowsImage "%s" : ID: "%s" : MinDisk %s' %(image['name'], image['id'], image['minDisk']))

    # get global IP info
    if config.testing: pdb.set_trace()
    
    
        
        


    


if __name__ == "__main__":
    main()
