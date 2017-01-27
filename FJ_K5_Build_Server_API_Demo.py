#!/usr/bin/python
"""Summary:
The following tutorial demonstrates how the native OpenStack APIs can be used to deploy a server, network, subnet and router
on the Fujitsu K5 IaaS Platform

Author: Graham Land
Date: 27/01/17
Twitter: @allthingsclowd
Github: https://github.com/allthingscloud
Blog: https://allthingscloud.eu


"""

import requests
import sys
import json
import pprint

def get_endpoint(k5token, endpoint_type):
    # list the endpoints
    for ep in k5token.json()['token']['catalog']:
        if len(ep['endpoints'])>0:
            # if this is the endpoint that  I'm looking for return the url
            if endpoint_type == ep['endpoints'][0].get('name'):
                #pprint.pprint(ep)
                return ep['endpoints'][0].get('url')


def get_scoped_token(adminUser, adminPassword, contract, projectid, region):

    identityURL = 'https://identity.' + region + \
        '.cloud.global.fujitsu.com/v3/auth/tokens'

    try:
        response = requests.post(identityURL,
                                 headers={'Content-Type': 'application/json',
                                          'Accept': 'application/json'},
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


def create_network(k5token, name, availability_zone):


    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/networks')
    print networkURL
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.post(networkURL,
                                 headers={'X-Auth-Token': token,
                                         'Content-Type': 'application/json'},
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


def create_subnet(k5token, name, netid, cidr, availability_zone):

    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/subnets')
    print networkURL
    token = k5token.headers['X-Subject-Token']
    try:

        response = requests.post(networkURL,
                                headers={'X-Auth-Token': token,
                                         'Content-Type': 'application/json'},
                                json={
                                             "subnet": {
                                                 "name": name,
                                                 "network_id": netid,
                                                 "ip_version": 4,
                                                 "cidr": cidr,
                                                 "availability_zone": availability_zone
                                             }
                                            })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def create_router(k5token, name, availability_zone):

    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/routers')
    print networkURL
    token = k5token.headers['X-Subject-Token']

    try:
        response = requests.post(networkURL,
                                headers={'X-Auth-Token': token,
                                         'Content-Type': 'application/json'},
                                json={
                                          "router": {
                                               "name": name,
                                               "admin_state_up": True,
                                               "availability_zone": availability_zone
                                          }})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def update_router_gateway(k5token, router_id, network_id):

    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/routers/') + router_id
    print networkURL
    token = k5token.headers['X-Subject-Token']

    try:
        response = requests.put(networkURL,
                                headers={'X-Auth-Token': token,
                                         'Content-Type': 'application/json'},
                                json={
                                         "router": {
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
                                json={
                                    "subnet_id": subnet_id})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def create_security_group(k5token, name, description):

    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/security-groups')
    print networkURL
    token = k5token.headers['X-Subject-Token']

    try:
        response = requests.post(networkURL,
                                headers={'X-Auth-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                json={
                                        "security_group": {
                                            "name": name,
                                            "description": description
                                            }
                                        })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def create_security_group_rule(k5token, security_group_id, direction, portmin, portmax, protocol):

    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/security-group-rules')
    print networkURL
    token = k5token.headers['X-Subject-Token']

    try:
        response = requests.post(networkURL,
                                headers={'X-Auth-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
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

def create_port(k5token, name, network_id, security_group_id, availability_zone):

    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/ports')
    print networkURL
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.post(networkURL,
                                 headers={
                                     'X-Auth-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                 json={"port":
                                       {"network_id": network_id,
                                        "name": name,
                                        "admin_state_up": True,
                                        "availability_zone": availability_zone,
                                        "security_groups":
                                        [security_group_id]}})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def create_keypair(k5token, keypair_name, availability_zone):

    computeURL = unicode(get_endpoint(k5token, "compute")) + unicode('/os-keypairs')
    print computeURL
    token = k5token.headers['X-Subject-Token']

    try:
        response = requests.post(computeURL,
                                headers={
                                     'X-Auth-Token': token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'},
                                json={
                                    "keypair": {
                                        "name": keypair_name,
                                        "availability_zone": availability_zone
                                        }})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def create_server_with_port(k5token, name, imageid, flavorid, sshkey_name, security_group_name, availability_zone, volsize,  port_id):

    computeURL = unicode(get_endpoint(k5token, "compute")) + unicode('/servers')
    print computeURL
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.post(computeURL,
                                headers={'X-Auth-Token':token,'Content-Type': 'application/json','Accept':'application/json'},
                                json={"server": {

                                                 "name": name,
                                                 "security_groups":[{"name": security_group_name }],
                                                 "availability_zone":availability_zone,
                                                 "imageRef": imageid,
                                                 "flavorRef": flavorid,
                                                 "key_name": sshkey_name,
                                                 "block_device_mapping_v2": [{
                                                                               "uuid": imageid,
                                                                               "boot_index": "0",
                                                                               "device_name": "/dev/vda",
                                                                               "source_type": "image",
                                                                               "volume_size": volsize,
                                                                               "destination_type": "volume",
                                                                               "delete_on_termination": True
                                                                            }],
                                                 "networks": [{"port": port_id}],
                                                 "metadata": {"Example Custom Tag": "Finance Department"}
                                                }})

        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def create_global_ip(k5token, ext_network_id, port_id, availability_zone):

    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/floatingips')
    print networkURL
    token = k5token.headers['X-Subject-Token']

    try:
        response = requests.post(networkURL,
                                headers={
                                     'X-Auth-Token': token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'},
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

def main():

    # Initialise environment parameters
    adminUser = 'username goes here' # k5/openstack user login name
    adminPassword = 'password goes here' # k5/openstack user password
    contract = 'contract name goes here' # k5 contract name or openstack domain name
    defaultProject = 'default project name goes here' # default project id - on k5 it's the project name that starts with contract name and ends with -prj
    extaz2 = 'd730db50-0e0c-4790-9972-1f6e2b8c4915' # K5 availability zone b external network id
    demoProjectA = 'target project goes here' # k5/openstack demo target project name
    demoProjectAid = 'demo project id' # k5/openstack demo target project id
    region = 'uk-1' # target region

    # Get a project scoped token
    k5token = get_scoped_token(adminUser, adminPassword, contract, demoProjectAid, region)

    # Create a layer 2 virtual network
    network = create_network(k5token, "demonet", "uk-1b")

    print network

    print network.json()

    network_id = network.json()['network'].get('id')

    print network_id

    # Create a layer 3 subnet
    subnet = create_subnet(k5token, "demosubnet", network_id, "192.168.10.0/24", "uk-1b")

    print subnet

    print subnet.json()

    subnet_id = subnet.json()['subnet'].get('id')

    print subnet_id

    # Create a layer 3 virtual router
    router = create_router(k5token, "demorouter", "uk-1b")

    print router

    print router.json()

    router_id = router.json()['router'].get('id')

    print router_id

    # Add external gateway to router (extaz2 is the external network id for the external network in availability zone b)
    router_gateway = update_router_gateway(k5token, router_id, extaz2)

    print router_gateway

    print router_gateway.json()

    # Plug new network subnet into the router
    router_interface = add_interface_to_router(k5token, router_id, subnet_id)

    print router_interface

    print router_interface.json()

    # Create a new security group
    security_group = create_security_group(k5token, "demosecuritygroup", "Demo Security Group Allows RDP, SSH and ICMP")

    print security_group

    print security_group.json()

    security_group_id = security_group.json()['security_group'].get('id')

    print security_group_id

    security_group_name = security_group.json()['security_group'].get('name')

    # Create security group rules
    # allow rdp
    rdp_rule = create_security_group_rule(k5token, security_group_id, "ingress", "3389", "3389", "tcp")

    print rdp_rule

    print rdp_rule.json()

    # allow ssh # allow rdp
    ssh_rule = create_security_group_rule(k5token, security_group_id, "ingress", "22", "22", "tcp")

    print ssh_rule

    print ssh_rule.json()

     # allow icmp
    icmp_rule = create_security_group_rule(k5token, security_group_id, "ingress", "0", "0", "icmp")

    print icmp_rule

    print icmp_rule.json()

    # Create a new port for the server
    server_port = create_port(k5token, "demoserverport", network_id, security_group_id, "uk-1b")

    print server_port

    print server_port.json()

    server_port_id = server_port.json()['port'].get('id')

    print server_port_id

    # Create ssh key pair that can be injected into the server
    server_key = create_keypair(k5token, "demokeypair", "uk-1b")

    print server_key

    print server_key.json()

    server_key_id = server_key.json()['keypair'].get('id')

    print server_key_id

    server_key_private = server_key.json()['keypair'].get('private_key')

    print server_key_private

    server_key_public = server_key.json()['keypair'].get('public_key')

    print server_key_public

    server_key_name = server_key.json()['keypair'].get('name')

    # K5 predefined parameters for images and flavors

    # this is the id of the K5 ubuntu image
    image_id = "ffa17298-537d-40b2-a848-0a4d22b49df5"

    # the is the id of a small flavor size (T-1 or P1...need to verify)
    flavor_id = "1901"

    # Create the virtual machine
    new_server = create_server_with_port(k5token, "demoserver", image_id, flavor_id, server_key_name, security_group_name, "uk-1b", 3,  server_port_id)

    print new_server

    print new_server.json()

    # Assign a global/public ip address
    public_ip = create_global_ip(k5token, extaz2, server_port_id, "uk-1b")

    print public_ip

    print public_ip.json()

    print public_ip.json()['floatingip'].get('floating_ip_address')





if __name__ == "__main__":
    main()
