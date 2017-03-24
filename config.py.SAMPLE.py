# -*- coding: iso8859-15 -*-
"""
config.py
configuration file for k5 api. Caveat: don't upload to github without cleaning

you'll need your credentials; all other values come from your config needs
"""

from string import Template
encoding = 'iso-8859-1' # for xml and other purposes


import base64


testing=True

htmlProxies = {'http' : 'http://YourUserID:yourProxyPassword@YourFtsProxy:82', 'https' : 'http://yourUserID:YourProxxyPassword@mchproxya.mch.fsc.net:82'}
#htmlProxies = {}
adminUser='YourK5UserID'
adminPassword='YourK5Password'
contract='YourK5ContractNum'
region='uk-1' # or any other region
projectid='YourK5ProjectID' # might be obsolete
securityGroup = 'YourSecGroupMust Exist'
# securityGroupID = '11113222222333333'
networkName = 'yourDesiredNetworkName'
subnetName='yourDesiredSubnetName'
subnetAddress='10.10.0.0/16' # pick it along your design
allocationPoolStart= '10.10.10.1' # pick it along your design
allocationPoolEnd='10.10.100.255' # pick it along your design
routerName = 'YourRouterName'
defaultRoute='10.10.0.1'    # pick it along your design, see net config above

externalNet = 'inf_az1_ext-net01'   # recommended one for uk-1
nameserver1 = '62.60.39.9'  # recommended one for uk-1, see documentation
# nameserver2 = '62.60.39.10'
nameserver2 = '8.8.8.8' # Google, just to have a safe bet



key='NameOfecretKeyPair'

# server parameters; 
if testing:
    serverName='yourServerName'
    imageRef="6e1610db-1115-4260-8dc2-bcdd526a54be" # grab it from the sample output of fjk5.py. This one is a Ubuntu*14*LTS
    flavor='1302'   # pretty small footprint. Refer to docs.
    volumesize = '90' # take what you need, must be bigger than minsize for selected image.
    availabilityZone = 'uk-1a'  # if you chose a different one, you have to chose a different external net above
    networkPortName = 'SomePortName'
    initialPassword = 'WindowsPassword' # CHANGE THIS ONE AS SOON AS YOU HAVE ACCESS TO THE SERVER. Only for Windows.




