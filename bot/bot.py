#!/usr/bin/env python3

__version__ = '0003.1'

import sys, os, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import jumpcloud
import config
debug = True

def usage():
    print("""Usage: {0} [option]

    options:
        check app_offenses

    """.format(sys.argv[0]))


def check_app_offenses():

    #app = 'Slack'
    #jdata = jumpcloud.get_app(app)
    #for line in jdata:
    #    print(line['system_id'])

    #app_offenses = {}
    app_offenses = []
    for app in config.blacklistsoftware:
        if debug: print(app)
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
        
    if debug: print(str(systems_users_dict))
    #{'5cf93ad2bd31ec75de452bcd': '5cdc8042aedcce77afcdb670', '5d9e267e546c544ad994f8cb': '5cdc7fad683a41781ec39845', '5e30c0b9890a7a4766268b59': '5de99ca25045a9513ca0dafa', '5d9e204c22874c28abece3a1': '5cdc8042d72cb377b72c5b36', '5ddda45d484f9c5b7ff5721c': 'Empty', '5ddda49b0c35306c77d09072': 'Empty', '5ddf112c2e34784cb7e24c41': '5cdc80416e59bc2c5bbe63ef', '5de97e3a82fdd020a161042b': 'Empty', '5de99b62fe8d195bababe9a3': 'Empty', '5df3efcdf2d66c6f6a287136': 'Empty'}

    systems_users_email_dict = {}
    for system_id, user_id in systems_users_dict.items():
        if debug: print(system_id, '->', user_id)
        if user_id == 'Empty':
            if debug: print(str(system_id) + ' is Empty')
            systems_users_email_dict[system_id] = 'Empty'
        else:
            #get_user_email 5cdc8042d72cb377b72c5b36
            user_email = jumpcloud.get_user_email(user_id)
            if debug: print(user_email)
            systems_users_email_dict[system_id] = user_email

    return systems_users_email_dict
        

    #5ddf112c2e34784cb7e24c41 Skype
    #systems_users_jdata [{'id': '5cdc80416e59bc2c5bbe63ef', 'type': 'user', 'compiledAttributes': {'sudo': {'withoutPassword': False, 'enabled': True}}, 'paths': [[{'attributes': {'sudo': {'withoutPassword': False, 'enabled': True}}, 'to': {'attributes': None, 'id': '5cdc80416e59bc2c5bbe63ef', 'type': 'user'}}]]}]
    #----------------------------------------------------
    #5de97e3a82fdd020a161042b Skype
    #systems_users_jdata []
    #----------------------------------------------------

if __name__ == "__main__":
    if sys.argv[1:]:
        if sys.argv[1] == "check" and sys.argv[2] == "app_offenses":
            offenders = check_app_offenses()
            print(str(offenders))
        else:
            print('Unknown option')
    else:
        usage()




