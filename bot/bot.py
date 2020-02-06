#!/usr/bin/env python3

__version__ = '0003'

import sys, os, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import jumpcloud

import config

debug = False


#app = 'Slack'
#jdata = jumpcloud.get_app(app)
#for line in jdata:
#    print(line['system_id'])

#app_offenses = {}
app_offenses = []
for app in config.blacklistsoftware:
    #print(app)
    jdata = jumpcloud.get_app(app)
    for line in jdata:
        #print(line['system_id'] + ' ' + line['name'])
        system_id = str(line['system_id'])
        app_offenses.extend([system_id, app])

#print(app_offenses)
systems_users_dict = {}

for i in range(0, len(app_offenses), 2):
    system_id = app_offenses[i]
    app_name  = app_offenses[i + 1]
    if debug: print(str(system_id) + ' ' + str(app_name))

    
    #get_systems_users 5d9e267e546c544ad994f8cb
    systems_users_jdata  = jumpcloud.get_systems_users_json(system_id)
    if debug: print('----------------------------------------------------')
    if debug: print('systems_users_jdata ' + str(systems_users_jdata))
    if debug: print(str(type(systems_users_jdata)))
    if not systems_users_jdata:
        if debug: print('Empty ' + str(systems_users_jdata))
        systems_users_dict[system_id] = 'Empty'
    else:
        for line in systems_users_jdata:
            if debug: print('systems_users are... ' + str(line['id']))
            systems_users_dict[system_id] = str(line['id'])
    
    #for line in systems_users_jdata:
    #    print('systems_users ' + str(line['id']))
    #for line in systems_users_jdata:
    #    print('systems_users ' + str(line['id']))
    
print(str(systems_users_dict))



#5ddf112c2e34784cb7e24c41 Skype
#systems_users_jdata [{'id': '5cdc80416e59bc2c5bbe63ef', 'type': 'user', 'compiledAttributes': {'sudo': {'withoutPassword': False, 'enabled': True}}, 'paths': [[{'attributes': {'sudo': {'withoutPassword': False, 'enabled': True}}, 'to': {'attributes': None, 'id': '5cdc80416e59bc2c5bbe63ef', 'type': 'user'}}]]}]
#----------------------------------------------------
#5de97e3a82fdd020a161042b Skype
#systems_users_jdata []
#----------------------------------------------------


