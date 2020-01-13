#!/usr/bin/env python

__version__='0.1.2'

import sys
if sys.version_info[0] < 3:
    raise Exception("Please use Python 3 ")

import jcapiv1
from jcapiv1.rest import ApiException as ApiException1

import jcapiv2
from jcapiv2.rest import ApiException as ApiException2

import time
import os
import json
import urllib3

def usage():
    print("Usage: " + sys.argv[0] + " option")
    print("""
    options:

      list_systems
      list_systems_json
      list_systems_os
      list_systems_os_version
      list_systems_id [os]
      list_systems_hostname
      list_systems_serial
      systeminsights_os_version [system_id]

      list_user_groups
      list_user_group_members [group_id]
      list_system_groups
      list_system_group_members [group_id]
      list_users
      list_systemusers
      list_commands

      get_systems [system_id]
      get_systems_version
      get_systems_id
      get_systems_hostname [system_id]
      get_user_ids
      get_user_email [user_id]

      systeminsights_apps [system_id]
      systeminsights_programs [system_id]

      systeminsights_browser_plugins
      systeminsights_firefox_addons

      list_systeminsights_apps [system_id]
      list_systeminsights_programs [system_id]

      get_app [bundle_name]
      get_program [name]

      list_system_bindings [user_id]
`
      update_system [system_id] [key] [value]

      trigger [name]

    """)

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

import ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)): 
    ssl._create_default_https_context = ssl._create_unverified_context

#def list_os_version():
#    configuration = jcapiv2.Configuration()
#    configuration.api_key['x-api-key'] = os.environ.get('JUMPCLOUD_API_KEY')
#    try: # List System Insights OS Version
#        api_instance = jcapiv2.SystemInsightsApi(jcapiv2.ApiClient(configuration))
#        api_response = api_instance.systeminsights_list_os_version(content_type, accept_type, limit=100, skip=skip, filter=filter, x_org_id=x_org_id)
#        print(api_response)
#    except ApiException2 as e:
#        print("Exception when calling SystemInsightsApi->systeminsights_list_os_version: %s\n" % e)

def systeminsights_os_version(system_id=None):
    urllib3.disable_warnings()

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


def list_user_groups():
    configuration = jcapiv2.Configuration()
    configuration.api_key['x-api-key'] = os.environ.get('JUMPCLOUD_API_KEY')
    try:
        api_instance = jcapiv2.UserGroupsApi(jcapiv2.ApiClient(configuration))
        user_groups = api_instance.groups_user_list(content_type, accept_type, limit=100)
        #pprint(user_groups)
        print(user_groups)
    except ApiException2 as e:
        print("Exception when calling UserGroupsApi->groups_user_list: %s\n" % e)

def list_system_groups():
    urllib3.disable_warnings()
    URL="https://console.jumpcloud.com/api/v2/systemgroups?limit=100"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #pprint(response.data.decode('utf-8'))
    print(json.dumps(json.loads(response.data.decode('utf-8')), sort_keys=False, indent=4))

def systeminsights_browser_plugins():
    urllib3.disable_warnings()
    URL="https://console.jumpcloud.com/api/v2/systeminsights/browser_plugins"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #pprint(response.data.decode('utf-8'))
    print(json.dumps(json.loads(response.data.decode('utf-8')), sort_keys=False, indent=4))

def systeminsights_firefox_addons():
    urllib3.disable_warnings()
    URL="https://console.jumpcloud.com/api/v2/systeminsights/firefox_addons?limit=100"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #pprint(response.data.decode('utf-8'))
    print(json.dumps(json.loads(response.data.decode('utf-8')), sort_keys=False, indent=4))



#def systeminsights_list_apps():
#    configuration = jcapiv2.Configuration()
#    configuration.api_key['x-api-key'] = os.environ.get('JUMPCLOUD_API_KEY')
#    try:
#        api_instance = jcapiv2.SystemInsightsApi(jcapiv2.ApiClient(configuration))
#        api_response = api_instance.systeminsights_list_apps(content_type, accept_type, limit=limit, x_org_id=x_org_id, skip=skip, filter=filter)
#        pprint(api_response)
#    except ApiException2 as e:
#        print("Exception when calling SystemInsightsApi->systeminsights_list_apps: %s\n" % e)

#def systeminsights_list_apps():
#    urllib3.disable_warnings()
#    URL="https://console.jumpcloud.com/api/v2/systeminsights/apps?limit=100"
#    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
#    response = http.request('GET', URL,
#                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
#                                     'Content-Type': content_type,
#                                     'Accept': accept_type})
#    #pprint(response.data.decode('utf-8'))
#    print(json.dumps(json.loads(response.data.decode('utf-8')), sort_keys=False, indent=4))

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

    #print('CHECK.FOR.RETURN.HERE')
    #print(response['message'])

    #if 'Bad' in response['message']:
    #    print('Bail.Bad')
    #    sys.exit(0)

    #if 'Bad' in response.get('message'):
    #    print('Bail.Bad')
    #    sys.exit(0)

#{
#    "message": "Bad Request: invalid object id \"5df3efcdf2d66c6f6a287\""
#}

    if len(response) == 1:
        if debug: print('I have spoken. 1')
        sys.exit(0)

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

    #for line in responseList:
    #    count += 1
    #    #print(str(count) + ' ' + line['name'] + ' (' + line['bundle_name'] + ') Version: ' + line['bundle_short_version'])
    #    print(str(count) + ' ' + str(line) )
    #print(json.dumps(json.loads(responseList), sort_keys=False, indent=4))
    #for line in responseList:
    #    count += 1
    #    print(json.dumps(line, sort_keys=False, indent=4))
    


def get_systeminsights_list_apps_json(system_id=None, skip=0, limit=100): #GET /systeminsights/{system_id}/apps
    urllib3.disable_warnings()

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






########################
########################



#def systeminsights_list_programs():
#    configuration = jcapiv2.Configuration()
#    configuration.api_key['x-api-key'] = os.environ.get('JUMPCLOUD_API_KEY')
#    try:
#        api_instance = jcapiv2.SystemInsightsApi(jcapiv2.ApiClient(configuration))
#        api_response = api_instance.systeminsights_list_programs(content_type, accept_type, limit=100, x_org_id=x_org_id, skip=skip, filter=filter)
#        pprint(api_response)
#    except ApiException2 as e:
#        print("Exception when calling SystemInsightsApi->systeminsights_list_programs: %s\n" % e)

#def systeminsights_list_programs():
#    urllib3.disable_warnings()
#    URL="https://console.jumpcloud.com/api/v2/systeminsights/programs?limit=100"
#    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
#    response = http.request('GET', URL,
#                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
#                                     'Content-Type': content_type,
#                                     'Accept': accept_type})
#    #pprint(response.data.decode('utf-8'))
#    print(json.dumps(json.loads(response.data.decode('utf-8')), sort_keys=False, indent=4))

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
    urllib3.disable_warnings()

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




def list_users():
    configuration = jcapiv1.Configuration()
    configuration.api_key['x-api-key'] = os.environ.get('JUMPCLOUD_API_KEY')
    try:
        api_instance = jcapiv1.SystemusersApi(jcapiv1.ApiClient(configuration))
        users = api_instance.systemusers_list(content_type, accept_type)
        #pprint(users)
        print(users)
    except ApiException1 as e:
        print("Exception when calling SystemusersApi->systemusers_list: %s\n" % err)

def list_commands():
    configuration = jcapiv1.Configuration()
    configuration.api_key['x-api-key'] = os.environ.get('JUMPCLOUD_API_KEY')
    try:
        api_instance = jcapiv1.CommandsApi(jcapiv1.ApiClient(configuration))
        api_response = api_instance.commands_list(content_type, accept_type, skip=skip, fields=fields, limit=limit, sort=sort, filter=filter, x_org_id=x_org_id)
        #pprint(api_response)
        print(api_response)
    except ApiException1 as e:
        print("Exception when calling CommandsApi->commands_list: %s\n" % e)

def systeminsights_list_system_apps_jcapiv2(system_id=None): #GET /systeminsights/{system_id}/apps

    system_id = ''.join(system_id)
    print(system_id)

    configuration = jcapiv2.Configuration()
    configuration.api_key['x-api-key'] = os.environ.get('JUMPCLOUD_API_KEY')

    try:
        api_instance = jcapiv2.SystemInsightsApi(jcapiv2.ApiClient(configuration))
        api_response = api_instance.systeminsights_list_system_apps(system_id=system_id, content_type=content_type, accept=accept_type, limit=100, skip=skip, filter=filter, x_org_id=x_org_id)
        #pprint(api_response)
        print(api_response)
    except ApiException2 as e:
        print("Exception when calling SystemInsightsApi->systeminsights_list_system_apps: %s\n" % e)
#https://github.com/TheJumpCloud/jcapi-python/blob/master/jcapiv2/docs/SystemInsightsApi.md#systeminsights_list_apps

#https://docs.jumpcloud.com/2.0/traits/filter
#https://console.jumpcloud.com/api/v2/systeminsights/5df3efcdf2d66c6f6a287136/apps?limit=100&filter=bundle_name:eq:ControlStrip
def systeminsights_list_system_apps(system_id=None): #GET /systeminsights/{system_id}/apps
    urllib3.disable_warnings()

    system_id = ''.join(system_id)
    #print(system_id)
    URL="https://console.jumpcloud.com/api/v2/systeminsights/" + str(system_id) + "/apps?limit=100"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #pprint(response.data.decode('utf-8'))
    print(json.dumps(json.loads(response.data.decode('utf-8')), sort_keys=False, indent=4))


def list_systeminsights_apps(system_id=None): #GET /systeminsights/{system_id}/apps

    system_id = ''.join(system_id)
    #print(system_id)

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

    #print(str(len(responseList)))

    for line in responseList:
        count += 1
        print(str(count) + ' ' + line['name'] + ' (' + line['bundle_name'] + ') Version: ' + line['bundle_short_version'])


#    {
#        "name": "Python.app",
#        "path": "/System/Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app",
#        "bundle_executable": "Python",
#        "bundle_identifier": "org.python.python",
#        "bundle_name": "Python",
#        "bundle_short_version": "2.7.16",
#        "bundle_version": "2.7.16",
#        "bundle_package_type": "APPL",
#        "environment": "",
#        "element": "",
#        "compiler": "",
#        "development_region": "English",
#        "display_name": "",
#        "info_string": "2.7.16, (c) 2001-2016 Python Software Foundation.",
#        "minimum_system_version": "",
#        "category": "",
#        "applescript_enabled": "1",
#        "copyright": "(c) 2001-2016 Python Software Foundation.",
#        "last_opened_time": -1,
#        "system_id": "5df3efcdf2d66c6f6a287136",
#        "collection_time": "2020-01-11T21:37:29.541Z"
#    },

def get_systeminsights_apps_json(system_id=None, skip=0, limit=100): #GET /systeminsights/{system_id}/apps
    urllib3.disable_warnings()

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
    urllib3.disable_warnings()

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

    #print(str(len(responseList)))

    for line in responseList:
        count += 1
        print(line['system_id']  + ' ' + line['name'] + ' (' + line['bundle_name'] + ') Version: ' + line['bundle_short_version'])
        #print(str(count) + str(line))



# api/v2/systeminsights/apps?limit=100&skip=0&filter=bundle_name:eq:Maps
def get_systeminsights_app_json(name=None, skip=0, limit=100): #GET /systeminsights/apps
    urllib3.disable_warnings()

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
    urllib3.disable_warnings()

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
    urllib3.disable_warnings() #https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings

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
    urllib3.disable_warnings()

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


def list_system_bindings(user_id=None): #https://github.com/TheJumpCloud/JumpCloudAPI
    urllib3.disable_warnings()

    print("user_id is " + str(user_id))
    user_id = ''.join(user_id)

    URL="https://console.jumpcloud.com/api/systemusers/" + str(user_id) + "/systems"

    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type})
    print(response.data.decode('utf-8'))

def get_systems_hostname(system_id=None):
    urllib3.disable_warnings()

    #print("system_id is " + str(system_id))
    system_id = ''.join(system_id)

    URL="https://console.jumpcloud.com/api/systems/" + str(system_id)

    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #print(response.data.decode('utf-8'))
    jdata = json.loads(response.data.decode('utf-8'))
    print(jdata['hostname'])

#api.v1
def get_systems(system_id=None):
    urllib3.disable_warnings()

    system_id = ''.join(system_id)

    URL="https://console.jumpcloud.com/api/systems/" + str(system_id)

    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    jdata = json.loads(response.data.decode('utf-8'))
    print(json.dumps(jdata, indent=4, sort_keys=True))


def get_user_email(user_id=None):
    urllib3.disable_warnings()

    user_id = ''.join(user_id)

    URL="https://console.jumpcloud.com/api/systemusers/" + str(user_id)

    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #print(response.data.decode('utf-8'))
    jdata = json.loads(response.data.decode('utf-8'))
    print(jdata['email'])


#https://docs.jumpcloud.com/2.0/system-group-members-and-membership/list-system-groups-group-membership
def list_system_group_members(group_id=None):
    urllib3.disable_warnings()

    #print("group_id is " + str(group_id))
    group_id = ''.join(group_id)

    URL="https://console.jumpcloud.com/api/v2/systemgroups/" + str(group_id) + "/membership"

    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #print(response.data.decode('utf-8'))
    #print(json.dumps(json.loads(response.data.decode('utf-8')), sort_keys=True, indent=4))
    #jdata = json.dumps(json.loads(response.data.decode('utf-8')))
    jdata = json.loads(response.data.decode('utf-8'))
    #print(jdata)
    #for item in jdata:
    #    print(jdata.get('id'))
    #for data in jdata['id']:

    systems = []
    for system in jdata:
        #print(system.get('id'))
        systems.append(system.get('id'))

    #print(systems)
    for sys in systems:
        get_systems_hostname(sys)

def list_user_group_members(group_id=None):
    urllib3.disable_warnings()

    #print("group_id is " + str(group_id))
    group_id = ''.join(group_id)

    URL="https://console.jumpcloud.com/api/v2/usergroups/" + str(group_id) + "/members"

    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #print(response.data.decode('utf-8'))
    jdata = json.loads(response.data.decode('utf-8'))

    users = []
    for user in jdata:
        #print(user)
        #print(user.get('to').get('id'))
        users.append(user.get('to').get('id'))

    #print(users)
    for user_id in users:
        #get_systems_hostname(sys)
        #print(user_id)
        get_user_email(user_id)


                     
def list_systemusers():
    urllib3.disable_warnings()
    URL="https://console.jumpcloud.com/api/systemusers"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type})
    #pprint(response.data.decode('utf-8'))
    print(json.dumps(json.loads(response.data.decode('utf-8')), sort_keys=True, indent=4))

#def get_systems():
#    urllib3.disable_warnings()
#    URL="https://console.jumpcloud.com/api/systems"
#    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
#    response = http.request('GET', URL,
#                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
#                                     'Content-Type': content_type,
#                                     'Accept': accept_type})
#    #pprint(response.data.decode('utf-8'))
#    jdata = json.loads(response.data.decode('utf-8'))
#    #print('totalCount: ' + str(jdata['totalCount']))
#    print(json.dumps(jdata, sort_keys=True, indent=4))

#https://docs.jumpcloud.com/1.0/systems/list-all-systems
#List All Systems GET /systems
def list_systems_json():
    urllib3.disable_warnings()
    URL="https://console.jumpcloud.com/api/systems"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    jdata = json.loads(response.data.decode('utf-8'))
    #print('totalCount: ' + str(jdata['totalCount']))
    print(json.dumps(jdata, sort_keys=True, indent=4))


def get_systems_id():
    urllib3.disable_warnings()
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
        #print(data.get('_id') + ' ' + data.get('hostname'))
        print(data.get('_id'))
    #print('totalCount: ' + str(jdata['totalCount']))

def list_systems_id(operatingsystem=None):
    urllib3.disable_warnings()

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
                print(data.get('_id') + ' ' + str(data.get('os')))
                #print(data.get('_id'))
        else:
            #print(data.get('_id') + ' ' + data.get('os'))
            print(data.get('_id'))
    #print('totalCount: ' + str(jdata['totalCount']))



def list_systems_hostname():
    urllib3.disable_warnings()
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

def list_systems_os():
    urllib3.disable_warnings()
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
    urllib3.disable_warnings()
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



def list_systems_list():
    urllib3.disable_warnings()
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
        print(data.get('_id') + ' ' + data.get('displayName') + ' (' + data.get('hostname')  + ') ' + data.get('os') + ' ' + data.get('version') + ' ' + data.get('arch'))
    #print('totalCount: ' + str(jdata['totalCount']))



def get_systems_version():
    urllib3.disable_warnings()
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
        print(data.get('_id') + ' ' + data.get('displayName') + ' (' + data.get('hostname')  + ') ' + data.get('os') + ' ' + data.get('version') + ' ' + data.get('arch'))
    #print('totalCount: ' + str(jdata['totalCount']))

def list_systems_os_version():
    urllib3.disable_warnings()
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



    
def get_user_ids():
    urllib3.disable_warnings()
    URL="https://console.jumpcloud.com/api/systemusers"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #pprint(response.data.decode('utf-8'))
    jdata = json.loads(response.data.decode('utf-8'))
    #print('totalCount: ' + str(jdata['totalCount']))
    for data in jdata['results']:
        print(data.get('_id') + ' ' + data.get('email'))


options = {
  'list_systems'                    : list_systems_list,
  'list_systems_id'                 : list_systems_id,
  'list_systems_hostname'           : list_systems_hostname,
  'list_systems_serial'             : list_systems_serial,
  'list_systems_json'               : list_systems_json,
  'list_systems_os'                 : list_systems_os,
  'list_systems_os_version'         : list_systems_os_version,
  'systeminsights_os_version'       : systeminsights_os_version,
  'list_user_groups'                : list_user_groups,
  'list_user_group_members'         : list_user_group_members,
  'list_system_groups'              : list_system_groups,
  'list_system_group_members'       : list_system_group_members,
  'list_users'                      : list_users,
  'list_systemusers'                : list_systemusers,
  'list_commands'                   : list_commands,
  'systeminsights_apps'             : systeminsights_apps,
  'systeminsights_programs'         : systeminsights_programs,
  'systeminsights_browser_plugins'  : systeminsights_browser_plugins,
  'systeminsights_firefox_addons'   : systeminsights_firefox_addons,
  'list_system_bindings'            : list_system_bindings,
  'get_systems'                     : get_systems,
  'get_systems_version'             : get_systems_version,
  'get_systems_id'                  : get_systems_id,
  'get_systems_hostname'            : get_systems_hostname,
  'get_user_email'                  : get_user_email,
  'get_user_ids'                    : get_user_ids,
  'update_system'                   : update_system,
  'list_systeminsights_apps'        : list_systeminsights_apps,
  'list_systeminsights_programs'    : list_systeminsights_programs,
  'get_app'                         : get_app,
  'get_program'                     : get_program,
  'trigger'                         : run_trigger,
}

if __name__ == '__main__':

    if sys.argv[1:]:
        if sys.argv[1] == "--help":
            usage()
            sys.exit(0)

        if sys.argv[1] == "update_system":
            try:
                options[sys.argv[1]](sys.argv[2],sys.argv[3], sys.argv[4])
                sys.exit(0)
            except KeyError as e:
                print("KeyError: " + str(e))
                sys.exit(1)


        if sys.argv[1] == "trigger" or \
           sys.argv[1] == "systeminsights_os_version" or \
           sys.argv[1] == "systeminsights_apps" or \
           sys.argv[1] == "systeminsights_programs" or \
           sys.argv[1] == "get_systems" or \
           sys.argv[1] == "get_systems_hostname" or \
           sys.argv[1] == "get_user_email" or \
           sys.argv[1] == "list_systems_id" or \
           sys.argv[1] == "list_user_group_members" or \
           sys.argv[1] == "list_system_group_members" or \
           sys.argv[1] == "list_systeminsights_apps" or \
           sys.argv[1] == "list_systeminsights_programs" or \
           sys.argv[1] == "get_app" or \
           sys.argv[1] == "get_program" or \
           sys.argv[1] == "list_system_bindings":
            try:
                options[sys.argv[1]](sys.argv[2:])
                sys.exit(0)
            except KeyError as e:
                print("KeyError: " + str(e))
                sys.exit(1)


        try:
            options[sys.argv[1]]()
        except KeyError as e:
            print("KeyError: " + str(e))
            sys.exit(1)
    else:
        usage()
        sys.exit(1)

#EOF

# page through...
#https://console.jumpcloud.com/api/v2/systeminsights/5df3efcdf2d66c6f6a287136/apps?limit=100&skip=0
#https://console.jumpcloud.com/api/v2/systeminsights/5df3efcdf2d66c6f6a287136/apps?limit=100&skip=99

#https://console.jumpcloud.com/api/v2/systeminsights/5df3efcdf2d66c6f6a287136/apps?limit=100&filter=bundle_name:eq:Microsoft%20Teams
#https://console.jumpcloud.com/api/v2/systeminsights/apps?limit=100&filter=bundle_name:eq:Safari

#https://console.jumpcloud.com/api/v2/systeminsights/programs?limit=100&filter=name:eq:Microsoft%20Teams
#https://console.jumpcloud.com/api/v2/systeminsights/apps?limit=100&filter=bundle_name:eq:Microsoft%20Teams


