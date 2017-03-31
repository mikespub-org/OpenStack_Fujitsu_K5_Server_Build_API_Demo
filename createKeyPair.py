#!/usr/bin/python
usage = """Summary:
The following tutorial demonstrates how the native OpenStack APIs can be used to deploy a server, network, subnet and router
on the Fujitsu K5 IaaS Platform

Author: Jörg Schulz
based on work of Graham Land
Date: 27/01/17

Github: Github: https://github.com/joergK5Schulz/OpenStack_Fujitsu_K5_Server_Build_API_Demo

Modifications: Joerg.schulz (AT ) ts.fujitsu.com
creates a new key pair - if it exists already, we return an error


"""

import config
import fjk5

if config.testing :
    import pdb





# creates a new key pair


def main():
    token = fjk5.get_scoped_token()
    key = fjk5.create_keypair(token)
    print ("status %s " % key.status_code)
    if key.status_code > 200:
        print (key.content)
    else:
        print (key.json()['keypair']['private_key'])




   


if __name__ == "__main__":
    main()
