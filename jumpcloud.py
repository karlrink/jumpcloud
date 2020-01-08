#!/usr/bin/env python

from __future__ import print_function
from pprint import pprint

import sys
if sys.version_info[0] < 3:
    raise Exception("Please use Python 3")

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

      list_os_version
      systeminsights_os_version
      list_user_groups
      list_user_group_members [group_id]
      list_system_groups
      list_system_group_members [group_id]
      list_users
      list_systemusers
      list_commands
      get_systems
      get_system_ids
      get_system_hostname [system_id]
      get_user_ids
      get_user_email [user_id]
      systeminsights_list_apps
      systeminsights_list_programs

      systeminsights_list_system_apps [system_id]

      list_system_bindings [user_id]

      trigger [name]

    """)

# Configure API key authorization: x-api-key
if os.environ.get('JUMPCLOUD_API_KEY') is None:
    print("JUMPCLOUD_API_KEY=None")
    sys.exit(1)

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


def list_os_version():
    configuration = jcapiv2.Configuration()
    configuration.api_key['x-api-key'] = os.environ.get('JUMPCLOUD_API_KEY')
    try: # List System Insights OS Version
        api_instance = jcapiv2.SystemInsightsApi(jcapiv2.ApiClient(configuration))
        api_response = api_instance.systeminsights_list_os_version(content_type, accept_type, limit=100, skip=skip, filter=filter, x_org_id=x_org_id)
        print(api_response)
    except ApiException2 as e:
        print("Exception when calling SystemInsightsApi->systeminsights_list_os_version: %s\n" % e)

def systeminsights_os_version():
    urllib3.disable_warnings()
    URL="https://console.jumpcloud.com/api/v2/systeminsights/os_version?limit=100"
    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
    response = http.request('GET', URL,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': content_type,
                                     'Accept': accept_type})
    #pprint(response.data.decode('utf-8'))
    jdata = json.loads(response.data.decode('utf-8'))
    print(json.dumps(jdata, sort_keys=False, indent=4))


def list_user_groups():
    configuration = jcapiv2.Configuration()
    configuration.api_key['x-api-key'] = os.environ.get('JUMPCLOUD_API_KEY')
    try:
        api_instance = jcapiv2.UserGroupsApi(jcapiv2.ApiClient(configuration))
        user_groups = api_instance.groups_user_list(content_type, accept_type, limit=100)
        pprint(user_groups)
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


def systeminsights_list_apps():
    configuration = jcapiv2.Configuration()
    configuration.api_key['x-api-key'] = os.environ.get('JUMPCLOUD_API_KEY')
    try:
        api_instance = jcapiv2.SystemInsightsApi(jcapiv2.ApiClient(configuration))
        api_response = api_instance.systeminsights_list_apps(content_type, accept_type, limit=limit, x_org_id=x_org_id, skip=skip, filter=filter)
        pprint(api_response)
    except ApiException2 as e:
        print("Exception when calling SystemInsightsApi->systeminsights_list_apps: %s\n" % e)

def systeminsights_list_programs():
    configuration = jcapiv2.Configuration()
    configuration.api_key['x-api-key'] = os.environ.get('JUMPCLOUD_API_KEY')
    try:
        api_instance = jcapiv2.SystemInsightsApi(jcapiv2.ApiClient(configuration))
        api_response = api_instance.systeminsights_list_programs(content_type, accept_type, limit=limit, x_org_id=x_org_id, skip=skip, filter=filter)
        pprint(api_response)
    except ApiException2 as e:
        print("Exception when calling SystemInsightsApi->systeminsights_list_programs: %s\n" % e)


def list_users():
    configuration = jcapiv1.Configuration()
    configuration.api_key['x-api-key'] = os.environ.get('JUMPCLOUD_API_KEY')
    try:
        api_instance = jcapiv1.SystemusersApi(jcapiv1.ApiClient(configuration))
        users = api_instance.systemusers_list(content_type, accept_type)
        pprint(users)
    except ApiException1 as e:
        print("Exception when calling SystemusersApi->systemusers_list: %s\n" % err)

def list_commands():
    configuration = jcapiv1.Configuration()
    configuration.api_key['x-api-key'] = os.environ.get('JUMPCLOUD_API_KEY')
    try:
        api_instance = jcapiv1.CommandsApi(jcapiv1.ApiClient(configuration))
        api_response = api_instance.commands_list(content_type, accept_type, skip=skip, fields=fields, limit=limit, sort=sort, filter=filter, x_org_id=x_org_id)
        pprint(api_response)
    except ApiException1 as e:
        print("Exception when calling CommandsApi->commands_list: %s\n" % e)

def systeminsights_list_system_apps(system_id=None):

    system_id = ''.join(system_id)

    configuration = jcapiv2.Configuration()
    configuration.api_key['x-api-key'] = os.environ.get('JUMPCLOUD_API_KEY')
    try:
        api_instance = jcapiv2.SystemInsightsApi(jcapiv2.ApiClient(configuration))
        api_response = api_instance.systeminsights_list_system_apps(system_id, content_type, accept_type, limit=limit, skip=skip, filter=filter, x_org_id=x_org_id)
        pprint(api_response)
    except ApiException2 as e:
        print("Exception when calling SystemInsightsApi->systeminsights_list_system_apps: %s\n" % e)


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

def get_system_hostname(system_id=None):
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
        get_system_hostname(sys)

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
        #get_system_hostname(sys)
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

def get_systems():
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
    print(json.dumps(jdata, sort_keys=True, indent=4))

def get_system_ids():
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
    for data in jdata['results']:
        print(data.get('_id') + ' ' + data.get('hostname'))
    
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
  'list_os_version'                 : list_os_version,
  'systeminsights_os_version'       : systeminsights_os_version,
  'list_user_groups'                : list_user_groups,
  'list_user_group_members'         : list_user_group_members,
  'list_system_groups'              : list_system_groups,
  'list_system_group_members'       : list_system_group_members,
  'list_users'                      : list_users,
  'list_systemusers'                : list_systemusers,
  'list_commands'                   : list_commands,
  'systeminsights_list_apps'        : systeminsights_list_apps,
  'systeminsights_list_programs'    : systeminsights_list_programs,
  'systeminsights_list_system_apps' : systeminsights_list_system_apps,
  'list_system_bindings'            : list_system_bindings,
  'get_systems'                     : get_systems,
  'get_system_hostname'             : get_system_hostname,
  'get_user_email'                  : get_user_email,
  'get_system_ids'                  : get_system_ids,
  'get_user_ids'                    : get_user_ids,
  'trigger'                         : run_trigger,
}

if __name__ == '__main__':

    if sys.argv[1:]:
        if sys.argv[1] == "--help":
            usage()
            sys.exit(0)

        if sys.argv[1] == "trigger" or \
           sys.argv[1] == "systeminsights_list_system_apps" or \
           sys.argv[1] == "get_system_hostname" or \
           sys.argv[1] == "get_user_email" or \
           sys.argv[1] == "list_user_group_members" or \
           sys.argv[1] == "list_system_group_members" or \
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
