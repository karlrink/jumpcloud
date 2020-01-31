#!/usr/bin/env python3

__version__ = '0001'

import sys, os, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import jumpcloud

import config

#app = 'Slack'
#jdata = jumpcloud.get_app(app)
#for line in jdata:
#    print(line['system_id'])

app_offenses = {}
for app in config.blacklistsoftware:
    #print(app)
    jdata = jumpcloud.get_app(app)
    for line in jdata:
        #print(line['system_id'] + ' ' + line['name'])
        system_id = str(line['system_id'])
        app_name  = str(line['name'])
        app_offenses[system_id] = app_name

print(str(app_offenses))

