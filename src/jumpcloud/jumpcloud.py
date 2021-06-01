#!/usr/bin/env python3

__version__='1.1.0'

import sys
if sys.version_info[0] < 3:
    raise Exception("Python 3 please")

import time
import os
import json
import urllib3 #hmmm... requests still wasn't good enough for me then? eh, don't forget ignore ssl
urllib3.disable_warnings()

def usage():
    print("Usage: " + sys.argv[0] + " option")
    print("""
    options:

      list_systems [json|os|os_version|hostname|serial|insights|state|fde|agent|root_ssh]
      list_systems_id
      get_systems_json [system_id]
      get_systems_remoteIP [system_id]
      add_systems_remoteIP_awsSG [system_id] [awsSG_id]
      get_systems_os system_id
      get_systems_hostname [system_id]
      get_systems_users [system_id]
      get_systems_memberof [system_id]
      delete_system [system_id]

      list_users [json|suspended|locked|password_expired|not_activated|ldap_bind|mfa]
      list_usergroups [json]
      list_usergroups_members [group_id]
      list_usergroups_details [group_id]
      list_systemgroups [json]
      list_systemgroups_membership [group_id]
      get_systemgroups_name [group_id]
      get_user_email [user_id]

      set_systems_memberof system_id group_id
      set_users_memberof user_id system_id
      set_users_memberof_admin user_id system_id
      del_users_memberof user_id system_id

      list_systeminsights_hardware [json|csv]
      systeminsights_os_version [system_id]
      get_systeminsights_system_info [system_id]

      list_systeminsights_apps [system_id]
      list_systeminsights_programs [system_id]

      systeminsights_apps [system_id]
      systeminsights_programs [system_id]

      get_app [bundle_name]
      get_program [name]

      systeminsights_browser_plugins
      systeminsights_firefox_addons

      list_system_bindings [user_id]
      list_user_bindings [system_id]

      list_commands [json]
      get_command [command_id] [associations|systems|systemgroups]
      mod_command [command_id] [add|remove] [system_id]

      trigger [name]

      list_command_results [command_id]
      delete_command_results [command_id]

      update_system [system_id] [key] [value]

      events [startDate] [endDate] 
      Note: Dates must be formatted as RFC3339: "2020-01-15T16:20:01Z"

    """)
    print('Version: ' + str(__version__))
    sys.exit(0)

# Configure API key authorization: x-api-key
if os.environ.get('JUMPCLOUD_API_KEY') is None:
    print("JUMPCLOUD_API_KEY=None")
    sys.exit(1)

debug=False

content_type = 'application/json' # str |  (default application/json)
accept_type = 'application/json' # str |  (default application/json)
limit = 0 # int |  (optional) (default 10) (100 max)
skip = 0 # int | The offset into the records to return. (optional) (default 0)

def systeminsights_os_version(system_id=None):

    skip=0
    limit=100

    if system_id:
        system_id = ''.join(system_id)
        URL="https://console.jumpcloud.com/api/v2/systeminsights/" + str(system_id) + "/os_version"
    else:
        URL="https://console.jumpcloud.com/api/v2/systeminsights/os_version?limit=" + str(limit) + "&skip=" + str(skip)

    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})

    count = len(json.loads(response.data.decode('utf-8')))
    print(json.dumps(json.loads(response.data.decode('utf-8')), sort_keys=False, indent=4))
    print(str(count))

    #and after 100...
    #is also limited by systeminsights being enabled
    if debug: print('all done.')


def list_command_results(command_id=None):
    skip=0
    limit=100

    if command_id:
        command_id = ''.join(command_id)
        URL="https://console.jumpcloud.com/api/commandresults/" + str(command_id) 
    else:
        URL="https://console.jumpcloud.com/api/commandresults?limit=" + str(limit) + "&skip=" + str(skip)

    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})

    count = len(json.loads(response.data.decode('utf-8')))
    print(json.dumps(json.loads(response.data.decode('utf-8')), sort_keys=False, indent=4))
    print(str(count))
    #and then after 100... limit
    return True

def delete_command_results(command_id):
    command_id = ''.join(command_id)
    URL="https://console.jumpcloud.com/api/commandresults/" + str(command_id)
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('DELETE', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})

    count = len(json.loads(response.data.decode('utf-8')))
    print(json.dumps(json.loads(response.data.decode('utf-8')), sort_keys=False, indent=4))
    print(str(count))
    return True

def print_systems_users_json(system_id=None):
    if system_id:
        system_id = ''.join(system_id)
    jdata = get_systems_users_json(system_id)
    print(json.dumps(jdata, sort_keys=True, indent=4))
    if debug: print(system_id)

def get_systems_users_json(system_id=None):
    skip=0
    limit=100

    URL="https://console.jumpcloud.com/api/v2/systems/" + str(system_id) + "/users?limit=" + str(limit) + "&skip=" + str(skip)
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #if debug: print(str(len(response.data.decode('utf-8'))))
    #if debug: print(str(response.status))
    return json.loads(response.data.decode('utf-8'))

def get_systems_memberof_json(system_id=None):
    skip=0
    limit=100

    URL="https://console.jumpcloud.com/api/v2/systems/" + str(system_id) + "/memberof?limit=" + str(limit) + "&skip=" + str(skip)
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #if debug: print(str(len(response.data.decode('utf-8'))))
    #if debug: print(str(response.status))
    return json.loads(response.data.decode('utf-8'))

def set_systems_memberof(system_id, group_id, verbose=True):
    #https://docs.jumpcloud.com/2.0/system-group-members-and-membership/manage-the-members-of-a-system-group

    #print('system_id ' + str(system_id))
    #print('group_id ' + str(group_id))

    URL="https://console.jumpcloud.com/api/v2/systemgroups/" + str(group_id) + "/members"

    data = {'op': 'add', 'type': 'system', 'id': system_id}
    encoded_body = json.dumps(data).encode('utf-8')
    #print(encoded_body)
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('POST', URL,
                           headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                    'Content-Type': content_type,
                                    'Accept': accept_type},
                           body=encoded_body)

    #print(str(response.status))
    #print(response.data.decode('utf-8'))
    if verbose: print(str(response.status), str(response.data.decode('utf-8')))
    return str(response.status), str(response.data.decode('utf-8'))


def set_users_memberof(user_id, system_id, verbose=True):
    #https://docs.jumpcloud.com/2.0/systems/manage-associations-of-a-system

    #print('system_id ' + str(system_id))
    #print('user_id ' + str(user_id))

    URL="https://console.jumpcloud.com/api/v2/systems/" + str(system_id) + "/associations"

    data = {'op': 'add', 'type': 'user', 'id': user_id}
    encoded_body = json.dumps(data).encode('utf-8')
    #print(encoded_body)
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('POST', URL,
                           headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                    'Content-Type': content_type,
                                    'Accept': accept_type},
                           body=encoded_body)

    #print(str(response.status))
    #print(response.data.decode('utf-8'))
    if verbose: print(str(response.status), str(response.data.decode('utf-8')))
    return str(response.status), str(response.data.decode('utf-8'))

def set_users_memberof_admin(user_id, system_id, verbose=True):
    #https://docs.jumpcloud.com/2.0/systems/manage-associations-of-a-system

    #print('system_id ' + str(system_id))
    #print('user_id ' + str(user_id))

    URL="https://console.jumpcloud.com/api/v2/systems/" + str(system_id) + "/associations"

    data = {'op': 'add', 'type': 'user', 'id': user_id, 'attributes': {'sudo':{'enabled':True, 'withoutPassword': False}}}
    encoded_body = json.dumps(data).encode('utf-8')
    #print(encoded_body)
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('POST', URL,
                           headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                    'Content-Type': content_type,
                                    'Accept': accept_type},
                           body=encoded_body)

    #print(str(response.status))
    #print(response.data.decode('utf-8'))
    if verbose: print(str(response.status), str(response.data.decode('utf-8')))
    return str(response.status), str(response.data.decode('utf-8'))



def del_users_memberof(user_id, system_id, verbose=True):
    #https://docs.jumpcloud.com/2.0/systems/manage-associations-of-a-system

    #print('system_id ' + str(system_id))
    #print('user_id ' + str(user_id))

    URL="https://console.jumpcloud.com/api/v2/systems/" + str(system_id) + "/associations"

    data = {'op': 'remove', 'type': 'user', 'id': user_id}
    encoded_body = json.dumps(data).encode('utf-8')
    #print(encoded_body)
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('POST', URL,
                           headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                    'Content-Type': content_type,
                                    'Accept': accept_type},
                           body=encoded_body)

    #print(str(response.status))
    #print(response.data.decode('utf-8'))
    if verbose: print(str(response.status), str(response.data.decode('utf-8')))
    return str(response.status), str(response.data.decode('utf-8'))

   
def print_systems_memberof(system_id=None):
    if system_id:
        system_id = ''.join(system_id)
    jdata = get_systems_memberof_json(system_id)
    #print(json.dumps(jdata, sort_keys=True, indent=4))
    #if debug: print(system_id)
    #for line in jdata:
    #    #print(str(line))
    #    group_id = str(line['id'])
    #    group_name = get_systemgroups_name(group_id)
    #    print(str(group_id) + ' "' + str(group_name) + '"')
    if jdata:
        groups = []
        for line in jdata:
            group_id = str(line['id'])
            group_name = get_systemgroups_name(group_id)
            groups.append(str(group_name))
        print(str(system_id) + ' ' + str(groups))
    else:
        print(str(system_id) + ' []')



def get_systems_users(system_id=None):
    if system_id:
        system_id = ''.join(system_id)
    jdata = get_systems_users_json(system_id)

    if len(jdata) == 1:
        #return print(jdata)
        print(jdata)
        return

    for line in jdata:
        print(line['id'])

#https://docs.jumpcloud.com/2.0/user-groups/list-all-users-groups
#https://github.com/TheJumpCloud/jcapi-python/tree/master/jcapiv2
#List all User Groups
#GET /usergroups
def list_usergroups_json():
    jdata = get_usergroups_json(group_id=None)
    print(json.dumps(jdata, sort_keys=False, indent=4))
    
def list_usergroups():
    jdata = get_usergroups_json(group_id=None)
    for line in jdata:
        print(str(line['id']) + ' "' + str(line['name']) + '"' )

def get_usergroups_json(group_id=None):

    if group_id:
        group_id = ''.join(group_id)
    else:
        group_id = ''

    URL="https://console.jumpcloud.com/api/v2/usergroups/" + str(group_id) + "?limit=" + str(limit) + "&skip=" + str(skip)

    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    return json.loads(response.data.decode('utf-8'))


def get_systemgroups_json(group_id=None):
    if group_id:
        group_id = ''.join(group_id)
        URL="https://console.jumpcloud.com/api/v2/systemgroups/" + str(group_id) + "?limit=100&skip=0"
    else:
        group_id = ''
        URL="https://console.jumpcloud.com/api/v2/systemgroups?limit=100&skip=0"

    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    return json.loads(response.data.decode('utf-8'))

def list_systemgroups_json(group_id=None):
    jdata = get_systemgroups_json(group_id)
    print(json.dumps(jdata, sort_keys=True, indent=4))

def list_systemgroups():
    jdata = get_systemgroups_json(group_id=None)
    for line in jdata:
        print(line['id'] + ' "' + line['name'] + '"')


def systeminsights_browser_plugins():
    URL="https://console.jumpcloud.com/api/v2/systeminsights/browser_plugins"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    print(json.dumps(json.loads(response.data.decode('utf-8')), sort_keys=False, indent=4))

def systeminsights_firefox_addons():
    URL="https://console.jumpcloud.com/api/v2/systeminsights/firefox_addons?limit=100"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    print(json.dumps(json.loads(response.data.decode('utf-8')), sort_keys=False, indent=4))



def systeminsights_apps(system_id=None): #GET /systeminsights/{system_id}/apps

    if system_id:
        system_id = ''.join(system_id)

    count=0
    skip=0
    limit=100

    response = get_systeminsights_list_apps_json(system_id, skip, limit)
    print(json.dumps(response, sort_keys=False, indent=4))

    if len(response) == 1:
        if debug: print('I have spoken.') #Kuiil
        #sys.exit(0)
        return

    #responseList = response
    #if debug: print(len(responseList))
    count += len(response)

    while len(response) > 0:
        skip += 100
        response = get_systeminsights_list_apps_json(system_id, skip, limit)
        #responseList = responseList + response
        count += len(response)
        #if debug: print(str(len(responseList)) + ' ' + str(len(response)))
        print(json.dumps(response, sort_keys=False, indent=4))
        if system_id is None:
            print('Count: ' + str(count))
        
    #print(str(len(responseList)))
    print('Count: ' + str(count))


def get_systeminsights_list_apps_json(system_id=None, skip=0, limit=100): #GET /systeminsights/{system_id}/apps

    if system_id:
        URL="https://console.jumpcloud.com/api/v2/systeminsights/" + str(system_id) + "/apps?limit=" + str(limit) + "&skip=" + str(skip)
    else:
        URL="https://console.jumpcloud.com/api/v2/systeminsights/apps?limit=" + str(limit) + "&skip=" + str(skip)

    if debug: print(str(URL))

    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    return json.loads(response.data.decode('utf-8'))


def systeminsights_programs(system_id=None): #GET /systeminsights/{system_id}/programs

    if debug: print('system_id type: ' + str(type(system_id)))
    if debug: print('system_id len: ' + str(len(system_id)))

    if len(system_id) != 0:
        system_id = ''.join(system_id)
        if debug: print('Using system_id (' + system_id + ')')
    else:
        system_id = None

    count=0
    skip=0
    limit=100

    response = get_systeminsights_list_programs_json(system_id, skip, limit)
    print(json.dumps(response, sort_keys=False, indent=4))

    if len(response) == 1:
        if debug: print('I have spoken.') #Kuiil
        #sys.exit(0)
        return

    count += len(response)

    while len(response) > 0:
        skip += 100
        response = get_systeminsights_list_programs_json(system_id, skip, limit)
        count += len(response)
        print(json.dumps(response, sort_keys=False, indent=4))
        if system_id is None:
            print('Count: ' + str(count))

    print('Count: ' + str(count))

def get_systeminsights_list_programs_json(system_id=None, skip=0, limit=100): #GET /systeminsights/{system_id}/programs

    if debug: print('get_systeminsights_list_programs_json')

    if system_id is None:
        URL="https://console.jumpcloud.com/api/v2/systeminsights/programs?limit=" + str(limit) + "&skip=" + str(skip)
    else:
        URL="https://console.jumpcloud.com/api/v2/systeminsights/" + str(system_id) + "/programs?limit=" + str(limit) + "&skip=" + str(skip)

    if debug: print(str(URL))

    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    return json.loads(response.data.decode('utf-8'))

#api.v1
def get_commands_json(command_id=None): #GET/api/commands/{id}
    if command_id:
        command_id = ''.join(command_id)
    else:
        command_id = ''
    URL="https://console.jumpcloud.com/api/commands/" + str(command_id)
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    return json.loads(response.data.decode('utf-8'))
 
def list_commands_json():
    jdata = get_commands_json()
    print(json.dumps(jdata, sort_keys=True, indent=4))
    
def list_commands():
    jdata = get_commands_json()
    for data in jdata['results']:
        _line = data.get('id') + ' ' + data.get('name') + ' (' + data.get('commandType') + ') '
        _line += '["' + data.get('launchType') + '"] '
        print(_line)

#api.v2
def get_commands_api2_json(command_id=None, segment=None): #GET/api/v2/commands/{id}/[associations?,systems,systemgroups]
    if command_id:
        command_id = ''.join(command_id)

    segments = ['associations','systems','systemgroups']
   
    if not segment in segments:
        print("Unknown option: " + str(segment))
        return

    if segment == 'associations':
        param = "&targets=system"
    else:
        param = ""
        

    limit = 100
    skip  = 0

    URL="https://console.jumpcloud.com/api/v2/commands/" + str(command_id) + "/" + str(segment) + "?limit=" + str(limit) + "&skip=" + str(skip) + str(param)
    #print(URL)
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    return json.loads(response.data.decode('utf-8'))

def list_commands_api2(command_id=None, segment=None):
    if command_id:
        command_id = ''.join(command_id)

    if segment:
        segment = ''.join(segment)

    jdata = get_commands_api2_json(command_id, segment)
    print(json.dumps(jdata, sort_keys=True, indent=4))

def mod_command(command_id=None, op=None, system_id=None): #POST/api/v2/commands/{id}/associations
    if command_id:
        command_id = ''.join(command_id)

    ops = ['add','remove']
  
    if not op in ops:
        print("Unknown option: " + str(op))
        return

    if system_id:
        system_id = ''.join(system_id)


    URL="https://console.jumpcloud.com/api/v2/commands/" + str(command_id) + "/associations"

    #encoded_body = json.dumps('{"op":"' + str(op) + '","type":"system","id":"' + str(system_id) + '"}')
    #encoded_body = json.dumps('{"op":"' + str(op) + '","type":"system","id":"' + str(system_id) + '"}').encode('utf-8')
    data = {'op': op, 'type': 'system', 'id': system_id}
    encoded_body = json.dumps(data).encode('utf-8')
    print(encoded_body)
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('POST', URL,
                           headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                    'Content-Type': content_type,
                                    'Accept': accept_type},
                           body=encoded_body)

    #return json.loads(response.data.decode('utf-8'))
    #print(json.loads(response.data.decode('utf-8')))
    print(str(response.status))
    print(response.data.decode('utf-8'))





#https://docs.jumpcloud.com/2.0/traits/filter
#https://console.jumpcloud.com/api/v2/systeminsights/5df3efcdf2d66c6f6a287136/apps?limit=100&filter=bundle_name:eq:ControlStrip
def list_systeminsights_apps(system_id=None): #GET /systeminsights/{system_id}/apps

    system_id = ''.join(system_id)

    count=0
    skip=0
    limit=100

    response = get_systeminsights_apps_json(system_id, skip, limit)
    responseList = response

    #print(len(responseList))

    while len(response) > 0:
        skip += 100
        response = get_systeminsights_apps_json(system_id, skip, limit)
        responseList = responseList + response
        #print(str(len(responseList)) + ' ' + str(len(response)))

    for line in responseList:
        count += 1
        print(str(count) + ' ' + line['name'] + ' (' + line['bundle_name'] + ') Version: ' + line['bundle_short_version'])


def get_systeminsights_apps_json(system_id=None, skip=0, limit=100): #GET /systeminsights/{system_id}/apps

    system_id = ''.join(system_id)
    #print(system_id)
    URL="https://console.jumpcloud.com/api/v2/systeminsights/" + str(system_id) + "/apps?limit=" + str(limit) + "&skip=" + str(skip)
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    return json.loads(response.data.decode('utf-8'))



def list_systeminsights_programs(system_id=None): #GET /systeminsights/{system_id}/programs

    system_id = ''.join(system_id)

    count=0
    skip=0
    limit=100

    response = get_systeminsights_programs_json(system_id, skip, limit)
    responseList = response
    #print(len(responseList))

    while len(response) > 0:
        skip += 100
        response = get_systeminsights_programs_json(system_id, skip, limit)
        responseList = responseList + response
        #print(str(len(responseList)) + ' ' + str(len(response)))

    #print(str(len(responseList)))

    for line in responseList:
        count += 1
        print(str(count) + ' ' + line['name'] + ' (' + line['publisher'] + ') Version: ' + line['version'])
        #print(str(count) + ' ' + str(line))

def get_systeminsights_programs_json(system_id=None, skip=0, limit=100): #GET /systeminsights/{system_id}/programs

    system_id = ''.join(system_id)
    #print(system_id)
    URL="https://console.jumpcloud.com/api/v2/systeminsights/" + str(system_id) + "/programs?limit=" + str(limit) + "&skip=" + str(skip)
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    return json.loads(response.data.decode('utf-8'))

# api/v2/systeminsights/apps?limit=100&skip=0&filter=bundle_name:eq:Maps
def get_app(name=None): #GET /systeminsights/apps

    #name = ''.join(name)
    #print(str(name) + ' my name is')

    #count=0
    skip=0
    limit=100

    response = get_systeminsights_app_json(name, skip, limit)
    responseList = response

    #print(len(responseList))

    while len(response) > 0:
        skip += 100
        response = get_systeminsights_app_json(name, skip, limit)
        responseList = responseList + response
        #print(str(len(responseList)) + ' ' + str(len(response)))

    #for line in responseList:
    #    count += 1
    #    print(line['system_id']  + ' ' + line['name'] + ' (' + line['bundle_name'] + ') Version: ' + line['bundle_short_version'])
    #    #print(str(count) + str(line))
    return responseList

def print_get_app(name=None):
    name = ''.join(name)
    responseList = get_app(name)
    count=0
    for line in responseList:
        count += 1
        print(line['system_id']  + ' ' + line['name'] + ' (' + line['bundle_name'] + ') Version: ' + line['bundle_short_version'])



# api/v2/systeminsights/apps?limit=100&skip=0&filter=bundle_name:eq:Maps
def get_systeminsights_app_json(name=None, skip=0, limit=100): #GET /systeminsights/apps

    #name = ''.join(name)
    #print('Name is ' + str(name))
    URL="https://console.jumpcloud.com/api/v2/systeminsights/apps?limit=" + str(limit) + "&skip=" + str(skip) + "&filter=bundle_name:eq:" + str(name)
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    return json.loads(response.data.decode('utf-8'))


# api/v2/systeminsights/programs?limit=100&skip=0&filter=name:eq:Microsoft Teams
def get_program(name=None): #GET /systeminsights/programs

    name = ''.join(name)
    #print(str(name) + ' my name is')

    count=0
    skip=0
    limit=100

    response = get_systeminsights_program_json(name, skip, limit)
    responseList = response

    #print(len(responseList))

    while len(response) > 0:
        skip += 100
        response = get_systeminsights_program_json(name, skip, limit)
        responseList = responseList + response
        #print(str(len(responseList)) + ' ' + str(len(response)))

    #print(str(len(responseList)))

    for line in responseList:
        count += 1
        print(line['system_id']  + ' ' + line['name'] + ' (' + line['publisher'] + ') Version: ' + line['version'])
        #print(str(count) + str(line))



# api/v2/systeminsights/programs?limit=100&skip=0&filter=name:eq:Microsoft Teams
def get_systeminsights_program_json(name=None, skip=0, limit=100): #GET /systeminsights/programs

    #name = ''.join(name)
    #print('Name is ' + str(name))
    URL="https://console.jumpcloud.com/api/v2/systeminsights/programs?limit=" + str(limit) + "&skip=" + str(skip) + "&filter=name:eq:" + str(name)
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    return json.loads(response.data.decode('utf-8'))


def run_trigger(trigger=None):

    #print("trigger is " + str(trigger))
    trigger = ''.join(trigger)

    URL="https://console.jumpcloud.com/api/command/trigger/" + str(trigger)
    #print(URL)
    encoded_body = json.dumps({}) 
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('POST', URL,
                           headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                    'Content-Type': content_type},
                           body=encoded_body)
    #print(response.read())
    print(response.data.decode('utf-8'))


def update_system(system_id=None, key=None, value=None):

    system_id = ''.join(system_id)
    print(system_id)

    key    = ''.join(key)
    print(key)

    value    = ''.join(value)
    print(value)

    encoded_body = json.dumps({ key : value })

    print(encoded_body)

    URL="https://console.jumpcloud.com/api/systems/" + str(system_id)
    #print(URL)

    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('PUT', URL,
                           headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                    'Content-Type': content_type,
                                    'Accept': accept_type},
                           body=encoded_body)
    #print(response.read())
    print(json.loads(response.data.decode('utf-8')))
#https://docs.jumpcloud.com/1.0/authentication-and-authorization/system-context
#https://docs.jumpcloud.com/1.0/systems/list-an-individual-system
#https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/instance-shutdown-initd

def get_system_bindings_json(user_id=None):
    #user_id = ''.join(user_id)
    URL="https://console.jumpcloud.com/api/v2/users/" + str(user_id) + "/systems"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    return json.loads(response.data.decode('utf-8'))

def list_system_bindings_json(user_id=None):
    user_id = ''.join(user_id)
    jdata = get_system_bindings_json(user_id)
    print(json.dumps(jdata, sort_keys=True, indent=4))

def list_system_bindings(user_id=None):
    user_id = ''.join(user_id)
    jdata = get_system_bindings_json(user_id)
    #print(jdata)
    for line in jdata:
        #print(line)
        hostname = get_systems_hostname(line['id'])
        print(line['id'] + ' ' + str(hostname))

#https://docs.jumpcloud.com/2.0/systems/list-the-users-bound-to-a-system
#List the Users bound to a System
#GET/systems/{system_id}/users
def get_user_bindings_json(system_id=None):
    #system_id = ''.join(system_id)
    URL="https://console.jumpcloud.com/api/v2/systems/" + str(system_id) + "/users?limit=100"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    return json.loads(response.data.decode('utf-8'))

def list_user_bindings_json(system_id=None):
    system_id = ''.join(system_id)
    jdata = get_user_bindings_json(system_id)
    print(json.dumps(jdata, sort_keys=True, indent=4))

def list_user_bindings(system_id=None):
    system_id = ''.join(system_id)
    jdata = get_user_bindings_json(system_id)

    for line in jdata:
        user_email = get_user_email(line['id'])
        print(line['id'] + ' ' + str(user_email))



    #print(jdata)
    #for line in jdata:
        #print(line)
    #    user_email = get_user_email(line['id'])
    #    print(line['id'] + ' ' + str(user_email))
    #print(json.dumps(jdata, indent=2))
    #List=[]
    #for line in jdata:
    #    #print(line)
    #    List.append(line['id'])
    #print(List)

    #List = json_extract(jdata, 'id')
    #dList=[]

    #print(List)
    #dList = list(dict.fromkeys(List))
    #print(dList)
    #for i in dList:

    #for i in List:
    #    if i not in dList:
    #        dList.append(i)

    #for i in dList:
    #    try:
    #        user_email = get_user_email(i)
    #    except KeyError as e:
    #        error = e
    #        user_email = None
    #    print(str(i) + ' ' + str(user_email))




def get_systems_hostname(system_id=None):
    system_id = ''.join(system_id)
    jdata = get_systems_json_single(system_id)
    return jdata['hostname']

def print_systems_hostname(system_id=None):
    system_id = ''.join(system_id)
    jdata = get_systems_json_single(system_id)
    print(jdata['hostname'])

def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values


#######################################################################

#def get_systems_remoteIP(system_id=None, verbose=True) -> None:
def get_systems_remoteIP(system_id=None, verbose=True):
    system_id = ''.join(system_id)
    jdata = get_systems_json_single(system_id)
    if verbose: print(str(jdata['remoteIP']))
    return jdata['remoteIP']


def add_systems_remoteIP_awsSG(system_id, awsSG_id):

    remote_ip = get_systems_remoteIP(system_id, verbose=False)
    print(remote_ip)
    print(awsSG_id)

    #import subprocess
    from subprocess import Popen, PIPE, STDOUT

    cmd = 'aws ec2 authorize-security-group-ingress --group-id '+str(awsSG_id)+' --protocol tcp --port 3389 --cidr '+str(remote_ip)+'/32'

    proc = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
    out = proc.stdout.readlines()
    err = proc.stderr.readlines()

    for o in out:
        print('out: '+str(o.decode('utf-8')))

    for e in err:
        print('err: '+str(e.decode('utf-8')))

    return True




#####################################################################################################################################################
#
#api.v1
#https://docs.jumpcloud.com/1.0/systems/list-all-systems
#List All Systems GET /systems
#def get_systems_json(system_id=None):
#    if system_id:
#        system_id = ''.join(system_id)
#        URL="https://console.jumpcloud.com/api/systems/" + str(system_id)
#    else:
#        system_id = ''
#        URL="https://console.jumpcloud.com/api/systems"
#
#
#    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
#    response = http.request('GET', URL,
#                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
#                                     'Content-Type': content_type,
#                                     'Accept': accept_type})
#    #if debug: print(str(response.status))
#    #if debug: print(str(len(response.data.decode('utf-8'))))
#
#    return response.data.decode('utf-8')
# more than 100 results... URL="https://console.jumpcloud.com/api/systems?skip=0&limit=100"

def get_systems_json_single(system_id=None):
    if system_id:
        URL="https://console.jumpcloud.com/api/systems/" + str(system_id)
    else:
         URL="https://console.jumpcloud.com/api/systems"

    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    return json.loads(response.data.decode('utf-8'))


def get_systems_json_multi(skip, limit):
    URL="https://console.jumpcloud.com/api/systems?skip=" + str(skip) + '&limit=' + str(limit)
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    return json.loads(response.data.decode('utf-8'))

def get_systems_json():
    skip=0
    data = get_systems_json_multi(skip, limit=100)
    totalCount = data['totalCount']
    #print(len(data['results']))
    resultList = data['results']

    while len(data['results']) > 0:
        skip += 100
        data = get_systems_json_multi(skip, limit=100)
        #print(len(data['results']))
        resultList.extend(data['results'])

    dictdata = { 'totalCount': totalCount, 'results': resultList }
    jdata = json.dumps(dictdata)
    return json.loads(jdata)

def get_user_email(user_id=None):
    if user_id:
        user_id = ''.join(user_id)
    jdata = get_systemusers_json(user_id)
    return str(jdata['email'])

def print_user_email(user_id=None):
    if user_id:
        user_id = ''.join(user_id)
        jdata = get_systemusers_json(user_id)
        #print(jdata)
        print(jdata['email'])
    else:
        print('None')


def get_systemgroups_name(group_id=None):
    if group_id:
        group_id = ''.join(group_id)
    jdata = get_systemgroups_json(group_id)
    return str(jdata['name'])

def print_systemgroups_name(group_id=None):
    if group_id:
        group_id = ''.join(group_id)
        jdata = get_systemgroups_json(group_id)
        print(jdata['name'])
    else:
        print('None')


#https://docs.jumpcloud.com/2.0/system-group-members-and-membership/list-system-groups-group-membership
#def list_systemgroups_membership(group_id=None):
#    pass

#def get_systemgroups_membership(group_id=None, skip=0, limit=100):
def list_systemgroups_membership(group_id=None, skip=0, limit=100):

    group_id = ''.join(group_id)

    #default is limit 10
    #URL="https://console.jumpcloud.com/api/v2/systemgroups/" + str(group_id) + "/membership"
    #https://docs.jumpcloud.com/2.0/system-group-members-and-membership/list-the-system-group-s-membership

    URL="https://console.jumpcloud.com/api/v2/systemgroups/" + str(group_id) + "/membership?limit=" + str(limit) + "&skip=" + str(skip)

    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    if debug: print(str(response.status))
    if debug: print(str(len(response.data.decode('utf-8'))))

    if response.status == 200:
        jdata = json.loads(response.data.decode('utf-8'))
    else:
        #return print(str(response.data.decode('utf-8')))
        print(str(response.data.decode('utf-8')))
        return

    for data in jdata:
        print(data['id'] + ' ' + get_systems_hostname(data.get('id')))


#def get_usergroups_members(group_id=None, skip=0, limit=100):
def list_usergroups_members(group_id=None, skip=0, limit=100):

    group_id = ''.join(group_id)

    URL="https://console.jumpcloud.com/api/v2/usergroups/" + str(group_id) + "/members?limit=" + str(limit) + "&skip=" + str(skip)

    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #print(str(len(response.data.decode('utf-8'))))
    #print(str(response.status))
    #print(response.data.decode('utf-8'))
    if response.status == 200:
        jdata = json.loads(response.data.decode('utf-8'))
    else:
        jdata = response.data.decode('utf-8')
        print(str(jdata))
        return

    users = []
    for user in jdata:
        users.append(user.get('to').get('id'))

    #print(users)
    for user_id in users:
        user_email = get_user_email(user_id)
        print(str(user_id) + ' ' + str(user_email))

def list_usergroups_details(group_id=None):

    group_id = ''.join(group_id)

    URL="https://console.jumpcloud.com/api/v2/usergroups/" + str(group_id)

    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #print(str(len(response.data.decode('utf-8'))))
    #print(str(response.status))
    #print(response.data.decode('utf-8'))
    if response.status == 200:
        jdata = json.loads(response.data.decode('utf-8'))
    else:
        jdata = response.data.decode('utf-8')
        print(str(jdata))
        return

    print(str(json.dumps(jdata, sort_keys=True, indent=4)))


def get_systemusers_json(user_id=None):
    #WARNING: this method prone to skip,limit 100
    if user_id:
        user_id = ''.join(user_id)
    else:
        user_id = ''
    URL="https://console.jumpcloud.com/api/systemusers/" + str(user_id)
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type})
    if response.status == 200:
        if len(response.data.decode('utf-8')) == 0:
            return json.loads('{}')
        return json.loads(response.data.decode('utf-8'))
    else:
        jdata = response.data.decode('utf-8')
        print(str(jdata))
        return

def list_users():
    jdata = get_systemusers_json()
    if len(jdata) == 0:
        print('Zero (0) response')

    #print('totalCount: ' + str(jdata['totalCount']))
    for data in jdata['results']:
        middlename = data.get('middlename')
        if middlename == "" or middlename is None:
            #if debug: print('blank middlename')
            middlename = ' '
        else:
            #if debug: print(str(data.get('middlename')))
            middlename = ' ' + str(data.get('middlename')) + ' '

        _line = str(data.get('_id')) + ' ' + str(data.get('username')) + ' (' + str(data.get('displayname')) + ') '
        _line += '["' + str(data.get('firstname')) + str(middlename) + str(data.get('lastname')) + '"] '
        _line += str(data.get('email'))
        print(_line)

def list_users_suspended(_print=True):
    thisDict = {}
    jdata = get_systemusers_json()
    if len(jdata) == 0:
        print('Zero (0) response')
    #print('totalCount: ' + str(jdata['totalCount']))
    for data in jdata['results']:
        suspended = data.get('suspended')
        if str(suspended) == 'True':
            _line = data.get('_id') + ' ' + data.get('username') + ' ' + data.get('email') + ' '
            _line += 'suspended:' + str(suspended)
            if _print: print(_line)
            thisDict[data.get('_id')] = data.get('email')
    return thisDict

def list_users_locked(_print=True):
    thisDict = {}
    jdata = get_systemusers_json()
    if len(jdata) == 0:
        print('Zero (0) response')
    #print('totalCount: ' + str(jdata['totalCount']))
    for data in jdata['results']:
        account_locked = data.get('account_locked')
        if str(account_locked) != 'False':
            _line = data.get('_id') + ' ' + data.get('username') + ' ' + data.get('email') + ' '
            _line += 'account_locked:' + str(account_locked)
            if _print: print(_line)
            thisDict[data.get('_id')] = data.get('email')
    return thisDict

def list_users_password_expired(_print=True):
    thisDict = {}
    jdata = get_systemusers_json()
    if len(jdata) == 0:
        print('Zero (0) response')
    #print('totalCount: ' + str(jdata['totalCount']))
    for data in jdata['results']:
        password_expired = data.get('password_expired')
        if str(password_expired) != 'False':
            _line = data.get('_id') + ' ' + data.get('username') + ' ' + data.get('email') + ' '
            _line += 'password_expired:' + str(password_expired)
            if _print: print(_line)
            thisDict[data.get('_id')] = data.get('email')
    return thisDict

def list_users_not_activated(_print=True):
    thisDict = {}
    jdata = get_systemusers_json()
    if len(jdata) == 0:
        print('Zero (0) response')
    #print('totalCount: ' + str(jdata['totalCount']))
    for data in jdata['results']:
        activated = data.get('activated')
        if str(activated) != 'True':
            _line = data.get('_id') + ' ' + data.get('username') + ' ' + data.get('email') + ' '
            _line += 'activated:' + str(activated)
            if _print: print(_line)
            thisDict[data.get('_id')] = data.get('email')
    return thisDict

def list_users_ldap_bind(_print=True):
    thisDict = {}
    jdata = get_systemusers_json()
    if len(jdata) == 0:
        print('Zero (0) response')
    #print('totalCount: ' + str(jdata['totalCount']))
    for data in jdata['results']:
        ldap_binding_user = data.get('ldap_binding_user')
        if str(ldap_binding_user) == 'True':
            _line = data.get('_id') + ' ' + data.get('username') + ' ' + data.get('email') + ' '
            _line += 'ldap_binding_user:' + str(ldap_binding_user)
            if _print: print(_line)
            thisDict[data.get('_id')] = data.get('email')
    return thisDict

def list_users_mfa():
    jdata = get_systemusers_json()
    if len(jdata) == 0:
        print('Zero (0) response')
    #print('totalCount: ' + str(jdata['totalCount']))
    for data in jdata['results']:
        mfa_json = json.dumps(data.get('mfa'), sort_keys=True)
        _output = data.get('_id') + ' "' + data.get('email') + ' ' + str(mfa_json)
        print(_output)

def list_users_json():
        response = get_systemusers_json()
        if len(response) == 0:
            print('Zero (0) response')
        print(json.dumps(response, sort_keys=True, indent=4))


def list_systems_json(system_id=None):
    if system_id:
        system_id = ''.join(system_id)
        jdata = get_systems_json_single(system_id)
    else:
        jdata = get_systems_json_single()
    print(json.dumps(jdata, sort_keys=True, indent=4))


#def list_systems_id(operatingsystem=None):
#
#    if operatingsystem:
#        operatingsystem = ''.join(operatingsystem)
#    else:
#        if debug: print('no os!')
#
#    URL="https://console.jumpcloud.com/api/systems"
#    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
#    response = http.request('GET', URL,
#                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
#                                     'Content-Type': content_type,
#                                     'Accept': accept_type})
#    jdata = json.loads(response.data.decode('utf-8'))
#    for data in jdata['results']:
#        if operatingsystem:
#            #print('checking... ' + str(operatingsystem))
#            if str(data.get('os')) == str(operatingsystem):
#                #print('Match OS' + str(data.get('os')))
#                if debug: print(data.get('_id') + ' ' + str(data.get('os')))
#                print(data.get('_id'))
#        else:
#            #print(data.get('_id') + ' ' + data.get('os'))
#            print(data.get('_id'))
#    #print('totalCount: ' + str(jdata['totalCount']))

def list_systems_id(operatingsystem=None):
    skip=0
    jdata = get_systems_id_json(skip, limit=100)
    for data in jdata['results']:
        print(data.get('_id'))

    while len(jdata['results']) > 0:
        skip += 100
        jdata = get_systems_id_json(skip, limit=100)
        for data in jdata['results']:
            print(data.get('_id'))
    


def get_systems_id_json(skip, limit):
    URL="https://console.jumpcloud.com/api/systems?skip=" + str(skip) + '&limit=' + str(limit)
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    return json.loads(response.data.decode('utf-8'))

def get_systems_id():
    idList = []
    skip=0
    jdata = get_systems_id_json(skip, limit=100)
    for data in jdata['results']:
        idList.append(data.get('_id'))

    while len(jdata['results']) > 0:
        skip += 100
        jdata = get_systems_id_json(skip, limit=100)
        for data in jdata['results']:
            idList.append(data.get('_id'))

    return idList



def list_systeminsights_hardware():

    idList = get_systems_id()

    for system_id in idList:
        #print(system_id)
        response = get_systeminsights_system_info_json(system_id, skip=0, limit=100)
        if len(response) == 0:
            print(str(system_id))
        for line in response:
            memGB = round(int(line['physical_memory']) / 1024 / 1024 / 1024)
            #print(line)
            _line =  str(system_id) + ' ' + line['computer_name'] + ' (' + line['hostname'] + ') '
            _line += line['hardware_model'] + ' (' + line['hardware_vendor'] + ') '
            _line += line['cpu_type'] + ' (' + str(line['cpu_physical_cores']) + ') '
            _line += line['cpu_brand'] + ' ' + str(line['physical_memory']) + ' Bytes (' + str(memGB) + ' GB) ["'
            _line += str(line['hardware_serial']) + '"] '
            print(_line)

def list_systeminsights_hardware_csv():

    idList = get_systems_id()

    for system_id in idList:
        #print(system_id)
        response = get_systeminsights_system_info_json(system_id, skip=0, limit=100)
        if len(response) == 0:
            print(str(system_id))
        for line in response:
            memGB = round(int(line['physical_memory']) / 1024 / 1024 / 1024)
            #print(line)
            _line =  str(system_id) + ',' + line['computer_name'] + ',(' + line['hostname'] + '),'
            _line += str(line['hardware_model']).replace(",", " ") + ',(' + line['hardware_vendor'] + '),'
            _line += line['cpu_type'] + ',(' + str(line['cpu_physical_cores']) + '),'
            _line += line['cpu_brand'] + ',' + str(line['physical_memory']) + ' Bytes,(' + str(memGB) + ' GB),["'
            _line += str(line['hardware_serial']) + '"] '
            print(_line)



def list_systeminsights_hardware_json():

    count=0
    skip=0
    limit=100

    idList = get_systems_id()

    for system_id in idList:
        response = get_systeminsights_system_info_json(system_id, skip, limit)
        if len(response) == 0:
            response = {  'system_id' : system_id  }   
        print(json.dumps(response, sort_keys=False, indent=4))


def get_systeminsights_system_info(system_id=None):
    system_id = ''.join(system_id)
    jdata = get_systeminsights_system_info_json(system_id, skip=0, limit=100)
    print(json.dumps(jdata, sort_keys=False, indent=4))


#List System Insights System Info
#GET /systeminsights/system_info
#Valid filter fields are system_id and cpu_subtype.
#https://docs.jumpcloud.com/2.0/system-insights/list-system-insights-system-info
def get_systeminsights_system_info_json(system_id=None, limit=None, skip=None):

    skip=0
    limit=100

    system_id = ''.join(system_id)
    URL="https://console.jumpcloud.com/api/v2/systeminsights/system_info?limit=" + str(limit) + "&skip=" + str(skip) + "&filter=system_id:eq:" + str(system_id)

    if debug: print(str(URL))
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})

    count = len(json.loads(response.data.decode('utf-8')))
    #jdata = json.loads(response.data.decode('utf-8'))
    return json.loads(response.data.decode('utf-8'))

def list_systems():
    jdata = get_systems_json()
    for data in jdata['results']:
        #print(data.get('_id') + ' "' + data.get('displayName') + '" (' + data.get('hostname')  + ') ' + data.get('os') + ' ' + data.get('version') + ' ' + data.get('arch'))
        print(str(data.get('_id')) + ' "' 
              + str(data.get('displayName')) + '" (' 
              + str(data.get('hostname'))  + ') ' 
              + str(data.get('os')) + ' ' 
              + str(data.get('version')) + ' ' 
              + str(data.get('arch')))
    #print('totalCount: ' + str(jdata['totalCount']))

def list_systems_hostname():
    jdata = get_systems_json()
    for data in jdata['results']:
        print(data.get('_id') + ' ' + data.get('hostname'))

def list_systems_os(_print=True):
    thisDict = {}
    jdata = get_systems_json()
    for data in jdata['results']:
        if _print: print(data.get('_id') + ' ' + data.get('os'))
        thisDict[data.get('_id')] = data.get('os')
    return thisDict

def get_systems_os(system_id, _print=True):
    system_id = ''.join(system_id)
    jdata = get_systems_json_single(system_id)
    if _print: print(jdata['os'])
    return jdata['os']

def list_systems_serial():
    jdata = get_systems_json()
    for data in jdata['results']:
        print(data.get('_id') + ' ("' + data.get('serialNumber') + '") ')

def list_systems_agent():
    jdata = get_systems_json()
    for data in jdata['results']:
        print(data.get('_id') + ' ' + data.get('hostname') + ' ("' + data.get('agentVersion') + '") ')

def list_systems_os_version():
    jdata = get_systems_json()
    for data in jdata['results']:
        print(data.get('_id') + ' ' + data.get('os') + ' ' + data.get('version') + ' ' + data.get('arch'))

def list_systems_insights():
    jdata = get_systems_json()
    for data in jdata['results']:
        #print(data.get('_id') + ' ' + data.get('os') + ' ' + data.get('version') + ' ' + data.get('arch') + ' ' + json.dumps(data.get('systemInsights')))
        _line = data.get('_id') + ' "' + data.get('displayName') + '" (' + data.get('hostname')  + ') ' + data.get('os') + ' ' + data.get('version') + ' ' + data.get('arch')
        _line += ' ' + json.dumps(data.get('systemInsights'))
        print(_line)

def list_systems_state():
    jdata = get_systems_json()
    for data in jdata['results']:
        _line = data.get('_id') + ' "' + data.get('displayName') + '" (' + data.get('hostname')  + ') '
        _line += str(data.get('lastContact')) + ' active: ' + str(json.dumps(data.get('active')))
        print(_line)

def list_systems_fde():
    jdata = get_systems_json()
    if len(jdata) == 0:
        print('Zero (0) response')
    if len(jdata) == 1:
        print(str(jdata))
        if debug: print('I have spoken.') #Kuiil
        #sys.exit(0)
        return

    for data in jdata['results']:
        fde_json = json.dumps(data.get('fde'), sort_keys=True)
        _line = data.get('_id') + ' "' + data.get('displayName') + '" (' + data.get('hostname')  + ') ' + data.get('os') + ' ' + data.get('version') + ' ' + data.get('arch')
        _line += ' ' + str(data.get('fileSystem')) + ' [' + str(fde_json) + ']'
        print(_line)

def list_systems_root_ssh():
    jdata = get_systems_json()
    for data in jdata['results']:
        root_ssh = json.dumps(data.get('allowSshRootLogin'), sort_keys=True)
        _line = data.get('_id') + ' "' + data.get('displayName') + '" (' + data.get('hostname')  + ') ' + data.get('os')
        _line += ' allowSshRootLogin ' + ' [' + str(root_ssh) + ']'
        print(_line)
        #print('root_ssh')

def delete_system(system_id=None):
    if system_id:
        system_id = ''.join(system_id)
    else:
        #return print('system_id required')
        print('system_id required')
        return

    URL="https://console.jumpcloud.com/api/systems/" + str(system_id)

    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('DELETE', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    print(json.loads(response.data.decode('utf-8')))
    return

    
#https://support.jumpcloud.com/support/s/article/jumpcloud-events-api1
def get_events_json(startDate=None, endDate=None):
    startDate = ''.join(startDate)
    endDate =   ''.join(endDate)
    URL="https://events.jumpcloud.com/events?startDate=" + str(startDate) + '&endDate=' + str(endDate)
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    return json.loads(response.data.decode('utf-8'))

def events(start=None, end=None):
    jdata = get_events_json(start, end)
    print(json.dumps(jdata, sort_keys=False, indent=4))

#hmmm...  these options are looking ugly... is this a case for python 3.10 new switch case statements? double pun intended. 
#https://www.python.org/dev/peps/pep-3103/

options = {
  'list_systems'                    : list_systems,
  'list_systems_id'                 : list_systems_id,
  'list_systems_hostname'           : list_systems_hostname,
  'list_systems_serial'             : list_systems_serial,
  'list_systems_json'               : list_systems_json,
  'get_systems_json'                : list_systems_json,
  'get_systems_remoteIP'            : get_systems_remoteIP,
  'add_systems_remoteIP_awsSG'      : add_systems_remoteIP_awsSG,
  'list_systems_os'                 : list_systems_os,
  'list_systems_agent'              : list_systems_agent,
  'list_systems_os_version'         : list_systems_os_version,
  'list_systeminsights_hardware'    : list_systeminsights_hardware,
  'list_systeminsights_hardware_json' : list_systeminsights_hardware_json,
  'list_systeminsights_hardware_csv'  : list_systeminsights_hardware_csv,
  'list_systems_insights'           : list_systems_insights,
  'list_systems_state'              : list_systems_state,
  'list_systems_fde'                : list_systems_fde,
  'list_systems_root_ssh'           : list_systems_root_ssh,
  'delete_system'                   : delete_system,
  'systeminsights_os_version'       : systeminsights_os_version,
  'list_usergroups'                 : list_usergroups,
  'list_usergroups_json'            : list_usergroups_json,
  'list_usergroups_members'         : list_usergroups_members,
  'list_usergroups_details'         : list_usergroups_details,
  'list_systemgroups'               : list_systemgroups,
  'list_systemgroups_json'          : list_systemgroups_json,
  'list_systemgroups_membership'    : list_systemgroups_membership,
  'list_users'                      : list_users,
  'list_users_json'                 : list_users_json,
  'list_users_mfa'                  : list_users_mfa,
  'list_users_suspended'            : list_users_suspended,
  'list_users_locked'               : list_users_locked,
  'list_users_password_expired'     : list_users_password_expired,
  'list_users_not_activated'        : list_users_not_activated,
  'list_users_ldap_bind'            : list_users_ldap_bind,
  'list_commands'                   : list_commands,
  'list_commands_json'              : list_commands_json,
  'get_command'                     : list_commands_api2,
  'mod_command'                     : mod_command,
  'systeminsights_apps'             : systeminsights_apps,
  'systeminsights_programs'         : systeminsights_programs,
  'systeminsights_browser_plugins'  : systeminsights_browser_plugins,
  'systeminsights_firefox_addons'   : systeminsights_firefox_addons,
  'list_system_bindings'            : list_system_bindings,
  'list_system_bindings_json'       : list_system_bindings_json,
  'list_user_bindings'              : list_user_bindings,
  'list_user_bindings_json'         : list_user_bindings_json,
  'get_systems_users'               : get_systems_users,
  'get_systems_os'                  : get_systems_os,
  'get_systems_memberof'            : print_systems_memberof,
  'set_systems_memberof'            : set_systems_memberof,
  'set_users_memberof'              : set_users_memberof,
  'set_users_memberof_admin'        : set_users_memberof_admin,
  'del_users_memberof'              : del_users_memberof,
  'get_systems_users_json'          : print_systems_users_json,
  'get_systems_hostname'            : print_systems_hostname,
  'get_user_email'                  : print_user_email,
  'get_systemgroups_name'           : print_systemgroups_name,
  'update_system'                   : update_system,
  'list_systeminsights_apps'        : list_systeminsights_apps,
  'list_systeminsights_programs'    : list_systeminsights_programs,
  'get_app'                         : print_get_app,
  'get_program'                     : get_program,
  'get_systeminsights_system_info'  : get_systeminsights_system_info,
  'list_command_results'            : list_command_results,
  'delete_command_results'          : delete_command_results,
  'events'                          : events,
  'trigger'                         : run_trigger,
}

args1 = ['list_systems','list_users','list_commands','list_systeminsights_hardware',
         'list_systemgroups']

args2 = ['trigger','systeminsights_os_version','systeminsights_apps',
         'systeminsights_programs','get_systems_json','get_systems_users',
         'get_systems_hostname','get_user_email','get_systems_remoteIP',
         'list_systems_id','list_usergroups_members','list_usergroups_details',
         'list_systemgroups_membership','list_systeminsights_apps','list_systeminsights_programs',
         'get_systeminsights_system_info','get_app','get_program','list_system_bindings',
         'list_user_bindings','list_user_bindings_json','list_system_bindings_json',
         'get_systems_users_json','delete_system','get_systems_memberof','get_systemgroups_name',
         'list_command_results','delete_command_results','get_systems_os']

def main():
    try:
        if sys.argv[1:]:
            if sys.argv[1] == "--help":
                usage()
            elif sys.argv[1] == "events" or sys.argv[1] == "get_command":
                options[sys.argv[1]](sys.argv[2],sys.argv[3])
            elif sys.argv[1] == "add_systems_remoteIP_awsSG":
                options[sys.argv[1]](sys.argv[2],sys.argv[3])
            elif sys.argv[1] == "update_system" or sys.argv[1] == "mod_command":
                options[sys.argv[1]](sys.argv[2],sys.argv[3], sys.argv[4])
            elif sys.argv[1] == "set_systems_memberof" or sys.argv[1] == "set_users_memberof" \
                    or sys.argv[1] == "set_users_memberof_admin":
                options[sys.argv[1]](sys.argv[2],sys.argv[3])
            elif sys.argv[1] == "del_users_memberof":
                options[sys.argv[1]](sys.argv[2],sys.argv[3])
            elif len(sys.argv) > 2 and sys.argv[1] in args1:
                options[str(sys.argv[1] + '_' + sys.argv[2])]()
            elif sys.argv[1] in args2:
                options[sys.argv[1]](sys.argv[2:])
            else:
                options[sys.argv[1]]()
        else:
            usage()

    except KeyError as e:
        print("KeyError: " + str(e))
        sys.exit(1)

if __name__ == '__main__':
    sys.exit(main())


#EOF
