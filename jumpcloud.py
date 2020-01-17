#!/usr/bin/env python

__version__='0.1.9.5'

import sys
if sys.version_info[0] < 3:
    raise Exception("Please use Python 3 ")

import time
import os
import json
import urllib3
urllib3.disable_warnings()

def usage():
    print("Usage: " + sys.argv[0] + " option")
    print("""
    options:

      list_systems [json, os, os_version, hostname, serial, insights_state, fde, agent]
      list_systems_id [systems_os]
      list_systeminsights_hardware [json]
      get_systems_json [system_id]
      get_systems_hostname [system_id]
      get_systems_users [system_id]
      get_systems_state [system_id]

      list_users [json, suspended, locked, password_expired, not_activated, ldap_bind]
      list_usergroups [json]
      list_usergroups_members [group_id]
      list_usergroups_details [group_id]
      list_systemgroups [json]
      list_systemgroups_membership [group_id]
      get_user_email [user_id]

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

      list_commands [json]

      update_system [system_id] [key] [value]

      #Note: Dates must be formatted as RFC3339: "2020-01-15T16:20:01Z"
      events [startDate] [endDate] 

      trigger [name]
    """)
    print('Version: ' + str(__version__))
    sys.exit(0)

# Configure API key authorization: x-api-key
if os.environ.get('JUMPCLOUD_API_KEY') is None:
    print("JUMPCLOUD_API_KEY=None")
    sys.exit(1)

debug=False

content_type = 'application/json' # str |  (default to application/json)
accept_type  = 'application/json' # str |  (default to application/json)
limit = 0 # int |  (optional) (default 10) (100 max)
skip = 0 # int | The offset into the records to return. (optional) (default to 0)
filter = ['[]'] # list[str] | Supported operators are: eq (optional) (default to [])
x_org_id = '' # str |  (optional) (default to )
fields = '' # str | Use a space seperated string of field parameters to include the data in the response. If omitted, the default list of fields will be returned.  (optional) (default to )
sort = '' # str | Use space separated sort parameters to sort the collection. Default sort is ascending. Prefix with `-` to sort descending.  (optional) (default to )

#import ssl
#if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
#    getattr(ssl, '_create_unverified_context', None)): 
#    ssl._create_default_https_context = ssl._create_unverified_context

def systeminsights_os_version(system_id=None):

    skip=0
    limit=100

    if debug: print('system_id is ' + str(system_id))
    if debug: print('system_id type ' + str(type(system_id)))

    #if system_id is None:
    if not system_id:
        URL="https://console.jumpcloud.com/api/v2/systeminsights/os_version?limit=" + str(limit) + "&skip=" + str(skip)
    else:
        system_id = ''.join(system_id)
        URL="https://console.jumpcloud.com/api/v2/systeminsights/" + str(system_id) + "/os_version"

    if debug: print(str(URL))
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

def get_systems_users_json(system_id=None):

    skip=0
    limit=100

    if debug: print('system_id is ' + str(system_id))
    if debug: print('system_id type ' + str(type(system_id)))

    system_id = ''.join(system_id)
    URL="https://console.jumpcloud.com/api/v2/systems/" + str(system_id) + "/users?limit=" + str(limit) + "&skip=" + str(skip)

    if debug: print(str(URL))
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

def get_systems_users(system_id=None):

    skip=0
    limit=100

    system_id = ''.join(system_id)
    URL="https://console.jumpcloud.com/api/v2/systems/" + str(system_id) + "/users?limit=" + str(limit) + "&skip=" + str(skip)

    if debug: print(str(URL))
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})

    count = len(json.loads(response.data.decode('utf-8')))
    jdata = json.loads(response.data.decode('utf-8'))

    #print(json.dumps(json.loads(response.data.decode('utf-8')), sort_keys=False, indent=4))

    c=0
    for line in jdata:
        c+=1
        #print(str(c) + ' ' + str(line))
        #print(str(c) + ' ' + str(line['id']) + ' ' + str(line['type']))
        user_id = str(line['id'])
        user_email = get_user_email(user_id)

        #print(str(user_id) + ' ' + get_user_email(user_id))
        print(str(user_id) + ' ' + str(user_email))

    if debug: print(str(count))
    #and after 100...
    #is also limited by systeminsights being enabled
    if debug: print('all done.')


#mark.remove
#def list_user_groups():
#    configuration = jcapiv2.Configuration()
#    configuration.api_key['x-api-key'] = os.environ.get('JUMPCLOUD_API_KEY')
#    try:
#        api_instance = jcapiv2.UserGroupsApi(jcapiv2.ApiClient(configuration))
#        user_groups = api_instance.groups_user_list(content_type, accept_type, limit=100)
#        #pprint(user_groups)
#        print(user_groups)
#    except ApiException2 as e:
#        print("Exception when calling UserGroupsApi->groups_user_list: %s\n" % e)


#https://docs.jumpcloud.com/2.0/user-groups/list-all-users-groups
#https://github.com/TheJumpCloud/jcapi-python/tree/master/jcapiv2
#List all User Groups
#GET /usergroups
def list_usergroups_json():
    jdata = get_usergroups_json(group_id=None)
    print(json.dumps(jdata, sort_keys=False, indent=4))
    
def list_usergroups():
    jdata = get_usergroups_json(group_id=None)
    #print(json.dumps(jdata, sort_keys=False, indent=4))
    c=0
    for line in jdata:
        c+=1
        #print(str(c) + ' ' + str(line))
        print(str(line['id']) + ' "' + str(line['name']) + '"' )

def get_usergroups_json(group_id=None):

    if group_id:
        group_id = ''.join(group_id)
    else:
        group_id = ''

    URL="https://console.jumpcloud.com/api/v2/usergroups/" + str(group_id) 

    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #print(str(response.status))
    if response.status == 200:
        return json.loads(response.data.decode('utf-8'))
    else:
        return json.loads('{"error" : "' + str(response.data.decode('utf-8')) + '"}')


def get_systemgroups_json():
    URL="https://console.jumpcloud.com/api/v2/systemgroups?limit=100"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #pprint(response.data.decode('utf-8'))
    #print(json.dumps(json.loads(response.data.decode('utf-8')), sort_keys=False, indent=4))
    return json.loads(response.data.decode('utf-8'))

def list_systemgroups_json():
    jdata = get_systemgroups_json()
    print(json.dumps(jdata, sort_keys=True, indent=4))

def list_systemgroups():
    jdata = get_systemgroups_json()
    for line in jdata:
        print(line['id'] + ' "' + line['name'] + '"')


def systeminsights_browser_plugins():
    URL="https://console.jumpcloud.com/api/v2/systeminsights/browser_plugins"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #pprint(response.data.decode('utf-8'))
    print(json.dumps(json.loads(response.data.decode('utf-8')), sort_keys=False, indent=4))

def systeminsights_firefox_addons():
    URL="https://console.jumpcloud.com/api/v2/systeminsights/firefox_addons?limit=100"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #pprint(response.data.decode('utf-8'))
    print(json.dumps(json.loads(response.data.decode('utf-8')), sort_keys=False, indent=4))



def systeminsights_apps(system_id=None): #GET /systeminsights/{system_id}/apps

    if debug: print('system_id type: ' + str(type(system_id)))
    if debug: print('system_id len: ' + str(len(system_id)))

    if len(system_id) != 0:
        system_id = ''.join(system_id)
        if debug: print('Using system_id (' + system_id + ')')
    else:
        #print('0 out.here')
        #sys.exit(99)
        system_id = None

    count=0
    skip=0
    limit=100

    response = get_systeminsights_list_apps_json(system_id, skip, limit)
    print(json.dumps(response, sort_keys=False, indent=4))

#{
#    "message": "Bad Request: invalid object id \"5df3efcdf2d66c6f6a287\""
#}

    if len(response) == 1:
        if debug: print('I have spoken. 1')
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

    if debug: print('get_systeminsights_list_apps_json')

    #system_id = ''.join(system_id)

    if system_id is None:
        #system_id = ''
        #if debug: print('Now Using system_id (' + str(system_id) + ')')
        URL="https://console.jumpcloud.com/api/v2/systeminsights/apps?limit=" + str(limit) + "&skip=" + str(skip)
    else:
        URL="https://console.jumpcloud.com/api/v2/systeminsights/" + str(system_id) + "/apps?limit=" + str(limit) + "&skip=" + str(skip)

    #print('get.system_id type: ' + str(type(system_id)))
    #print('get.system_id len: ' + str(len(system_id)))
    #print('get.system_id ' + str(system_id))

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
        if debug: print('I have spoken. 1')
        sys.exit(0)

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


def get_commands_json(command_id=None): #GET/commands/{id}

    if command_id:
        command_id = ''.join(command_id)
    else:
        command_id = ''

    URL="https://console.jumpcloud.com/api/commands/" + str(command_id)
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type})
    if response.status == 200:
        return json.loads(response.data.decode('utf-8'))
    else:
        return response.data.decode('utf-8')
 
def list_commands_json():
    jdata = get_commands_json()
    print(json.dumps(jdata, sort_keys=True, indent=4))
    #print(' 1 ' + str(jdata))
    
def list_commands():
    jdata = get_commands_json()
    #print('totalCount: ' + str(jdata['totalCount']))
    for data in jdata['results']:

        _line = data.get('id') + ' ' + data.get('name') + ' (' + data.get('commandType') + ') '
        _line += '["' + data.get('launchType') + '"] '
        #_line += '["' + data.get('launchType') + ' ' + data.get('command') + '"] '
        print(_line)

#https://docs.jumpcloud.com/2.0/traits/filter
#https://console.jumpcloud.com/api/v2/systeminsights/5df3efcdf2d66c6f6a287136/apps?limit=100&filter=bundle_name:eq:ControlStrip
def systeminsights_list_system_apps(system_id=None): #GET /systeminsights/{system_id}/apps

    system_id = ''.join(system_id)
    #print(system_id)
    URL="https://console.jumpcloud.com/api/v2/systeminsights/" + str(system_id) + "/apps?limit=100"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    print(json.dumps(json.loads(response.data.decode('utf-8')), sort_keys=False, indent=4))


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
    #print(system_id)

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

    name = ''.join(name)
    #print(str(name) + ' my name is')

    count=0
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

    for line in responseList:
        count += 1
        print(line['system_id']  + ' ' + line['name'] + ' (' + line['bundle_name'] + ') Version: ' + line['bundle_short_version'])
        #print(str(count) + str(line))


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
    print(response.data.decode('utf-8'))
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



def get_systems_hostname(system_id=None):
    system_id = ''.join(system_id)
    jdata = get_systems_json(system_id)
    return jdata['hostname']

def print_systems_hostname(system_id=None):
    system_id = ''.join(system_id)
    jdata = get_systems_json(system_id)
    print(jdata['hostname'])

#api.v1
#https://docs.jumpcloud.com/1.0/systems/list-all-systems
#List All Systems GET /systems
def get_systems_json(system_id=None):
    if system_id:
        system_id = ''.join(system_id)
    else:
        system_id = ''

    URL="https://console.jumpcloud.com/api/systems/" + str(system_id)

    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    if debug: print(str(response.status))
    if debug: print(str(len(response.data.decode('utf-8'))))

    if len(response.data.decode('utf-8')) == 0:
        return json.loads('{ "json":"0" }')

    if response.status == 200:
        return json.loads(response.data.decode('utf-8'))
    else:
        return response.data.decode('utf-8')


#def print_systems_json(system_id=None):
#    system_id = ''.join(system_id)
#    jdata = get_systems_json(system_id)
#    print(json.dumps(jdata, indent=4, sort_keys=True))

def get_systems_state(system_id=None):

    system_id = ''.join(system_id)

    URL="https://console.jumpcloud.com/api/systems/" + str(system_id)

    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    jdata = json.loads(response.data.decode('utf-8'))
    jsize = len(jdata)

    #print(json.dumps(jdata, indent=4, sort_keys=True))
    #print(str(jsize))
    print(jdata.get('_id') + ' ' + jdata.get('displayName') + ' (' + jdata.get('hostname')  + ') active:' + str(jdata.get('active')) + ' lastContact:' + jdata.get('lastContact') )


#def get_user_email(user_id=None):
#    user_id = ''.join(user_id)
#    URL="https://console.jumpcloud.com/api/systemusers/" + str(user_id)
#
#    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
#    response = http.request('GET', URL,
#                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
#                                     'Content-Type': content_type,
#                                     'Accept': accept_type})
#    #print(response.data.decode('utf-8'))
#    jdata = json.loads(response.data.decode('utf-8'))
#    #print(jdata['email'])
#    return str(jdata['email'])

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


#https://docs.jumpcloud.com/2.0/system-group-members-and-membership/list-system-groups-group-membership
def list_systemgroups_membership(group_id=None):

    #print("group_id is " + str(group_id))
    group_id = ''.join(group_id)

    URL="https://console.jumpcloud.com/api/v2/systemgroups/" + str(group_id) + "/membership"

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
        return print(str(response.data.decode('utf-8')))

    for data in jdata:
        print(data['id'] + ' ' + get_systems_hostname(data.get('id')))


def list_usergroups_members(group_id=None):

    #print("group_id is " + str(group_id))
    group_id = ''.join(group_id)

    URL="https://console.jumpcloud.com/api/v2/usergroups/" + str(group_id) + "/members"

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
        #print(user)
        #print(user.get('to').get('id'))
        users.append(user.get('to').get('id'))

    #print(users)
    for user_id in users:
        #get_systems_hostname(sys)
        #print(user_id)
        #get_user_email(user_id)
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

        _line = data.get('_id') + ' ' + data.get('username') + ' (' + data.get('displayname') + ') '
        _line += '["' + data.get('firstname') + str(middlename) + data.get('lastname') + '"] '
        _line += data.get('email')
        print(_line)

def list_users_suspended():
    jdata = get_systemusers_json()
    if len(jdata) == 0:
        print('Zero (0) response')
    #print('totalCount: ' + str(jdata['totalCount']))
    for data in jdata['results']:
        suspended = data.get('suspended')
        if str(suspended) != 'False':
            _line = data.get('_id') + ' ' + data.get('username') + ' ' + data.get('email') + ' '
            _line += 'suspended:' + str(suspended)
            print(_line)

def list_users_locked():
    jdata = get_systemusers_json()
    if len(jdata) == 0:
        print('Zero (0) response')
    #print('totalCount: ' + str(jdata['totalCount']))
    for data in jdata['results']:
        account_locked = data.get('account_locked')
        if str(account_locked) != 'False':
            _line = data.get('_id') + ' ' + data.get('username') + ' ' + data.get('email') + ' '
            _line += 'account_locked:' + str(account_locked)
            print(_line)

def list_users_password_expired():
    jdata = get_systemusers_json()
    if len(jdata) == 0:
        print('Zero (0) response')
    #print('totalCount: ' + str(jdata['totalCount']))
    for data in jdata['results']:
        password_expired = data.get('password_expired')
        if str(password_expired) != 'False':
            _line = data.get('_id') + ' ' + data.get('username') + ' ' + data.get('email') + ' '
            _line += 'password_expired:' + str(password_expired)
            print(_line)

def list_users_not_activated():
    jdata = get_systemusers_json()
    if len(jdata) == 0:
        print('Zero (0) response')
    #print('totalCount: ' + str(jdata['totalCount']))
    for data in jdata['results']:
        activated = data.get('activated')
        if str(activated) != 'True':
            _line = data.get('_id') + ' ' + data.get('username') + ' ' + data.get('email') + ' '
            _line += 'activated:' + str(activated)
            print(_line)

def list_users_ldap_bind():
    jdata = get_systemusers_json()
    if len(jdata) == 0:
        print('Zero (0) response')
    #print('totalCount: ' + str(jdata['totalCount']))
    for data in jdata['results']:
        ldap_binding_user = data.get('ldap_binding_user')
        if str(ldap_binding_user) == 'True':
            _line = data.get('_id') + ' ' + data.get('username') + ' ' + data.get('email') + ' '
            _line += 'ldap_binding_user:' + str(ldap_binding_user)
            print(_line)

def list_users_json():
        response = get_systemusers_json()
        if len(response) == 0:
            print('Zero (0) response')
        print(json.dumps(response, sort_keys=True, indent=4))


def list_systems_json(system_id=None):
    if system_id:
        system_id = ''.join(system_id)
        jdata = get_systems_json(system_id)
    else:
        jdata = get_systems_json()
    print(json.dumps(jdata, sort_keys=True, indent=4))


def list_systems_id(operatingsystem=None):

    if not operatingsystem:
        if debug: print('no os!')
        #sys.exit(1)
    else:
        operatingsystem = ''.join(operatingsystem)

    URL="https://console.jumpcloud.com/api/systems"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #pprint(response.data.decode('utf-8'))
    jdata = json.loads(response.data.decode('utf-8'))
    #print('totalCount: ' + str(jdata['totalCount']))
    #for data in jdata['results']:
    #    print(data.get('_id') + ' ' + data.get('hostname'))
    #print(str(jdata))

    for data in jdata['results']:
        if operatingsystem:
            #print('checking... ' + str(operatingsystem))
            if str(data.get('os')) == str(operatingsystem):
                #print('Match OS' + str(data.get('os')))
                if debug: print(data.get('_id') + ' ' + str(data.get('os')))
                print(data.get('_id'))
        else:
            #print(data.get('_id') + ' ' + data.get('os'))
            print(data.get('_id'))
    #print('totalCount: ' + str(jdata['totalCount']))


def print_get_systems_id(operatingsystem=None):

    if not operatingsystem:
        if debug: print('no os!')
        #sys.exit(1)
    else:
        operatingsystem = ''.join(operatingsystem)

    URL="https://console.jumpcloud.com/api/systems"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #pprint(response.data.decode('utf-8'))
    jdata = json.loads(response.data.decode('utf-8'))
    #print('totalCount: ' + str(jdata['totalCount']))
    #for data in jdata['results']:
    #    print(data.get('_id') + ' ' + data.get('hostname'))
    #print(str(jdata))

    for data in jdata['results']:
        if operatingsystem:
            #print('checking... ' + str(operatingsystem))
            if str(data.get('os')) == str(operatingsystem):
                #print('Match OS' + str(data.get('os')))
                if debug: print(data.get('_id') + ' ' + str(data.get('os')))
                print(data.get('_id'))
        else:
            #print(data.get('_id') + ' ' + data.get('os'))
            print(data.get('_id'))
    #print('totalCount: ' + str(jdata['totalCount']))

def get_systems_id_json():
    URL="https://console.jumpcloud.com/api/systems"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    return json.loads(response.data.decode('utf-8'))

def get_systems_id():
    idList = []
    jdata = get_systems_id_json()
    #print(json.dumps(jdata, sort_keys=False, indent=4))
    for data in jdata['results']:
        #print(data.get('_id') + ' ' + data.get('hostname'))
        idList.append(data.get('_id'))
    #print('totalCount: ' + str(jdata['totalCount']))
    return idList

def list_systems_hostname():
    URL="https://console.jumpcloud.com/api/systems"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #pprint(response.data.decode('utf-8'))
    jdata = json.loads(response.data.decode('utf-8'))
    #print('totalCount: ' + str(jdata['totalCount']))
    #for data in jdata['results']:
    #    print(data.get('_id') + ' ' + data.get('hostname'))
    #print(str(jdata))

    for data in jdata['results']:
        print(data.get('_id') + ' ' + data.get('hostname'))
    #print('totalCount: ' + str(jdata['totalCount']))


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

    if debug: print('list_systeminsights_hardware.end')



def list_systeminsights_hardware_json():
    if debug: print('run.1')
    #system_id = '5dbb61c83cccc8147faa4189'

    count=0
    skip=0
    limit=100

    #idList = list_systems_id()
    idList = get_systems_id()
    #print(str(idList))

    for system_id in idList:
        #print(system_id)
        response = get_systeminsights_system_info_json(system_id, skip, limit)
        #print(len(response))
        if len(response) == 0:
            response = {  'system_id' : system_id  }   
        print(json.dumps(response, sort_keys=False, indent=4))


    #print(str(jdata))
    #print(jdata['hostname'])
    if debug: print('run.1.end')



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


def list_systems_os():
    URL="https://console.jumpcloud.com/api/systems"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #pprint(response.data.decode('utf-8'))
    jdata = json.loads(response.data.decode('utf-8'))
    #print('totalCount: ' + str(jdata['totalCount']))
    #for data in jdata['results']:
    #    print(data.get('_id') + ' ' + data.get('hostname'))
    #print(str(jdata))

    for data in jdata['results']:
        #print(data.get('_id') + ' ' + data.get('os') + ' ' + data.get('version') + ' ' + data.get('arch'))
        print(data.get('_id') + ' ' + data.get('os'))
    #print('totalCount: ' + str(jdata['totalCount']))



def list_systems_serial():
    URL="https://console.jumpcloud.com/api/systems"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #pprint(response.data.decode('utf-8'))
    jdata = json.loads(response.data.decode('utf-8'))
    #print('totalCount: ' + str(jdata['totalCount']))
    #for data in jdata['results']:
    #    print(data.get('_id') + ' ' + data.get('hostname'))
    #print(str(jdata))

    for data in jdata['results']:
        print(data.get('_id') + ' ' + data.get('hostname') + ' ("' + data.get('serialNumber') + '") ')
    #print('totalCount: ' + str(jdata['totalCount']))

def list_systems_agent():
    jdata = get_systems_json()
    for data in jdata['results']:
        print(data.get('_id') + ' ' + data.get('hostname') + ' ("' + data.get('agentVersion') + '") ')

def list_systems_list():
    URL="https://console.jumpcloud.com/api/systems"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #pprint(response.data.decode('utf-8'))
    jdata = json.loads(response.data.decode('utf-8'))
    #print('totalCount: ' + str(jdata['totalCount']))
    #for data in jdata['results']:
    #    print(data.get('_id') + ' ' + data.get('hostname'))
    #print(str(jdata))

    for data in jdata['results']:
        print(data.get('_id') + ' "' + data.get('displayName') + '" (' + data.get('hostname')  + ') ' + data.get('os') + ' ' + data.get('version') + ' ' + data.get('arch'))
    #print('totalCount: ' + str(jdata['totalCount']))


def list_systems_os_version():
    URL="https://console.jumpcloud.com/api/systems"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #pprint(response.data.decode('utf-8'))
    jdata = json.loads(response.data.decode('utf-8'))
    #print('totalCount: ' + str(jdata['totalCount']))
    #for data in jdata['results']:
    #    print(data.get('_id') + ' ' + data.get('hostname'))
    #print(str(jdata))

    for data in jdata['results']:
        print(data.get('_id') + ' ' + data.get('os') + ' ' + data.get('version') + ' ' + data.get('arch'))
    #print('totalCount: ' + str(jdata['totalCount']))


def list_systems_insights_state():
    URL="https://console.jumpcloud.com/api/systems"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    jdata = json.loads(response.data.decode('utf-8'))
    #print('totalCount: ' + str(jdata['totalCount']))
    #for data in jdata['results']:
    #    print(data.get('_id') + ' ' + data.get('hostname'))
    #print(str(jdata))

    for data in jdata['results']:
        #print(data.get('_id') + ' ' + data.get('os') + ' ' + data.get('version') + ' ' + data.get('arch') + ' ' + json.dumps(data.get('systemInsights')))
        _line = data.get('_id') + ' "' + data.get('displayName') + '" (' + data.get('hostname')  + ') ' + data.get('os') + ' ' + data.get('version') + ' ' + data.get('arch')
        _line += ' ' + json.dumps(data.get('systemInsights'))
        print(_line)
    #print('totalCount: ' + str(jdata['totalCount']))

def list_systems_fde():
    jdata = get_systems_json()
    if len(jdata) == 0:
        print('Zero (0) response')
    if len(jdata) == 1:
        print(str(jdata))
        if debug: print('I have spoken')
        #sys.exit(1)
        return

    #print(str(jdata))
    #print('totalCount: ' + str(jdata['totalCount']))
    for data in jdata['results']:
        fde_json = json.dumps(data.get('fde'), sort_keys=True)
        _line = data.get('_id') + ' "' + data.get('displayName') + '" (' + data.get('hostname')  + ') ' + data.get('os') + ' ' + data.get('version') + ' ' + data.get('arch')
        _line += ' ' + str(data.get('fileSystem')) + ' [' + str(fde_json) + ']'
        print(_line)
    #print('totalCount: ' + str(jdata['totalCount']))

    
#def get_user_ids():
#    URL="https://console.jumpcloud.com/api/systemusers"
#    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
#    response = http.request('GET', URL,
#                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
#                                     'Content-Type': content_type,
#                                     'Accept': accept_type})
#    #pprint(response.data.decode('utf-8'))
#    jdata = json.loads(response.data.decode('utf-8'))
#    #print('totalCount: ' + str(jdata['totalCount']))
#    for data in jdata['results']:
#        print(data.get('_id') + ' ' + data.get('email'))

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
    if response.status != 200:
        print(str(response.data.decode('utf-8')))
        #return json.loads("{ 'status':'" + str(response.data.decode('utf-8')) + "'}")
        #jdata = '{"message":"' + response.data.decode('utf-8') + '"}'
        jdata = '{"' + str(response.status) + '":"' + str(response.data.decode('utf-8')) + '"}'
        #jdata = '{"status":"' + str(response.status) + '"},{"error":"' + str(response.data.decode('utf-8')) + '"}'
        #jdata = '{"status":"' + str(response.status) + '"},{"error":"' + str(response.data.decode('utf-8')) + '"}'
        return json.loads(jdata)
    else:
        #print(json.dumps(json.loads(response.data.decode('utf-8')), sort_keys=False, indent=4))
        return json.loads(response.data.decode('utf-8'))

    #print(str(response.status))
    #print(str(len(response.data.decode('utf-8'))))
    #print(str(response.data.decode('utf-8')))
    #jdata = json.loads(response.data.decode('utf-8'))
    #print(json.dumps(jdata))

def events(start=None, end=None):
    jdata = get_events_json(start, end)
    print(json.dumps(jdata, sort_keys=False, indent=4))

options = {
  'list_systems'                    : list_systems_list,
  'list_systems_id'                 : list_systems_id,
  'list_systems_hostname'           : list_systems_hostname,
  'list_systems_serial'             : list_systems_serial,
  'list_systems_json'               : list_systems_json,
  'get_systems_json'                : list_systems_json,
  'list_systems_os'                 : list_systems_os,
  'list_systems_agent'              : list_systems_agent,
  'list_systems_os_version'         : list_systems_os_version,
  'list_systeminsights_hardware'    : list_systeminsights_hardware,
  'list_systeminsights_hardware_json' : list_systeminsights_hardware_json,
  'list_systems_insights_state'     : list_systems_insights_state,
  'list_systems_fde'                : list_systems_fde,
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
  'list_users_suspended'            : list_users_suspended,
  'list_users_locked'               : list_users_locked,
  'list_users_password_expired'     : list_users_password_expired,
  'list_users_not_activated'        : list_users_not_activated,
  'list_users_ldap_bind'            : list_users_ldap_bind,
  'list_commands'                   : list_commands,
  'list_commands_json'              : list_commands_json,
  'systeminsights_apps'             : systeminsights_apps,
  'systeminsights_programs'         : systeminsights_programs,
  'systeminsights_browser_plugins'  : systeminsights_browser_plugins,
  'systeminsights_firefox_addons'   : systeminsights_firefox_addons,
  'list_system_bindings'            : list_system_bindings,
  'list_system_bindings_json'       : list_system_bindings_json,
  'get_systems_users'               : get_systems_users,
  'get_systems_state'               : get_systems_state,
  'get_systems_hostname'            : print_systems_hostname,
  'get_user_email'                  : print_user_email,
  #'get_user_ids'                    : get_user_ids,
  'update_system'                   : update_system,
  'list_systeminsights_apps'        : list_systeminsights_apps,
  'list_systeminsights_programs'    : list_systeminsights_programs,
  'get_app'                         : get_app,
  'get_program'                     : get_program,
  'get_systeminsights_system_info'  : get_systeminsights_system_info,
  'events'                          : events,
  'trigger'                         : run_trigger,
}

args1 = ['list_systems','list_users','list_commands','list_systeminsights_hardware',
         'list_systemgroups']

args2 = ['trigger','systeminsights_os_version','systeminsights_apps',
         'systeminsights_programs','get_systems_json','get_systems_users',
         'get_systems_state','get_systems_hostname','get_user_email',
         'list_systems_id','list_usergroups_members','list_usergroups_details',
         'list_systemgroups_membership','list_systeminsights_apps','list_systeminsights_programs',
         'get_systeminsights_system_info','get_app','get_program','list_system_bindings',
         'list_system_bindings_json']

if __name__ == '__main__':
    try:
        if sys.argv[1:]:
            if sys.argv[1] == "--help":
                usage()
            elif sys.argv[1] == "events":
                options[sys.argv[1]](sys.argv[2],sys.argv[3])
            elif sys.argv[1] == "update_system":
                options[sys.argv[1]](sys.argv[2],sys.argv[3], sys.argv[4])
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
#EOF
