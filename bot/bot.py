#!/usr/bin/env python3

__version__ = '0002'

import sys, os, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import jumpcloud

import config

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

for i in range(0, len(app_offenses), 2):
    system_id = app_offenses[i]
    app_name  = app_offenses[i + 1]
    print(str(system_id) + ' ' + str(app_name))

    #get_systems_users 5d9e267e546c544ad994f8cb




