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
def get_endpoint(k5token, endpoint_type):
    # list the endpoints
    for ep in k5token.json()['token']['catalog']:
        if len(ep['endpoints'])>0:
            # if this is the endpoint that  I'm looking for return the url
            if endpoint_type == ep['endpoints'][0].get('name'):
                #pprint.pprint(ep)
                return ep['endpoints'][0].get('url')

"""
This token is needed to call the APIN functions. Valid for some minutes, so get this for every significant step.
"""
def get_scoped_token(adminUser = config.adminUser ,
                     adminPassword= config.adminPassword,
                     contract = config.contract,
                     projectid = config.projectid,
                     region = config.region):
    identityURL = 'https://identity.' + region + \
        '.cloud.global.fujitsu.com/v3/auth/tokens'
    try:
        response = requests.post(identityURL,
                                 headers={'Content-Type': 'application/json',
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
                                           {"id": projectid
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
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.post(networkURL,
                                 headers={'X-Auth-Token': token,
                                         'Content-Type': 'application/json'},
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
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.post(networkURL,
                                headers={'X-Auth-Token': token,
                                         'Content-Type': 'application/json'},
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
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.post(networkURL,
                                headers={'X-Auth-Token': token,
                                         'Content-Type': 'application/json'},
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
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.put(networkURL,
                                headers={'X-Auth-Token': token,
                                         'Content-Type': 'application/json'},
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
    print networkURL
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.put(networkURL,
                                headers={'X-Auth-Token': token,
                                         'Content-Type': 'application/json'},
                                proxies=config.htmlProxies,
                                json={
                                    "subnet_id": subnet_id})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


"""
creates a security group, not yet demoed here
"""
def create_security_group(k5token, name, description):
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/security-groups')
    print networkURL
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.post(networkURL,
                                 headers={'X-Auth-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
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
    print networkURL
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.post(networkURL,
                                 headers={'X-Auth-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
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


"""
create a port for your new server.
"""
def create_port(k5token, network_id, security_group_id = config.securityGroupID , availability_zone = config.availabilityZone , name = config.networkPortName):
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/ports')
    print networkURL
    token = k5token.headers['X-Subject-Token']
    # security groups should contain default, else some things will fail during setup (like login credentials). YOu can remove it later if you wish.
    securityGroups = [security_group_id] if security_group_id else []
    defaultSecurityGroup = getSecurityGroup(k5token, 'default')
    # default1aGroup = getSecurityGroup(k5token, 'secgroup-1a')
    securityGroups.append(defaultSecurityGroup['id'])
    ### securityGroups.append( getSecurityGroup(k5token, 'secgroup-1a')['id'])
    try:
        response = requests.post(networkURL,
                                 headers={
                                     'X-Auth-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                 proxies=config.htmlProxies,
                                 json={"port":
                                       {"network_id": network_id,
                                        "name": name,
                                        "admin_state_up": True,
                                        "availability_zone": availability_zone,
                                        "security_groups": securityGroups }})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


"""
this PRINTS the new keypair. Don't forget to save it - you'll need it for login.
"""
def create_keypair(k5token, keypair_name = config.key, availability_zone = config.availabilityZone):
    computeURL = unicode(get_endpoint(k5token, "compute")) + unicode('/os-keypairs')
    print computeURL
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.post(computeURL,
                                headers={
                                     'X-Auth-Token': token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'},
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
    token = k5token.headers['X-Subject-Token']
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
        response = requests.post(computeURL,
                                headers={'X-Auth-Token':token,
                                         'Content-Type': 'application/json',
                                         'Accept':'application/json'},
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
return info on a generic subject
works with networks, routers, ...
"""
def list_something(token, url):
    # if config.testing: print (url)
    try:
        headers={'X-Auth-Token': token.headers['X-Subject-Token'],
                 'Content-Type': 'application/json',
                 'Accept': 'application/json'}
        #if config.testing: pdb.set_trace()
        response = requests.get(url,
                                headers = headers,
                                proxies=config.htmlProxies)
        return response, response.status_code
    except:
        return ("\nUnexpected error:", sys.exc_info()), -1
    
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
    
# helper functions for the list_functions
def getComputeURL(token):
    return unicode(get_endpoint(token, "compute")) + unicode('/servers')

def getServerDetailURL(token, serverID):
    return unicode(get_endpoint(token, "compute")) + unicode('/servers/') + serverID

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

"""
return a json list of all servers
"""
def list_servers(token):
    url = getComputeURL(token)
    return list_something(token, url)[0].json()
    
"""
returns some of the server Details
"""
def getServerDetail(token, serverID) :
    url = getServerDetailURL(token, serverID)
    return list_something(token, url)[0].json()

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
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.post(networkURL,
                                headers={
                                     'X-Auth-Token': token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'},
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
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.delete(networkURL,
                                    headers={
                                         'X-Auth-Token': token,
                                         'Content-Type': 'application/json',
                                         'Accept': 'application/json'},
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
