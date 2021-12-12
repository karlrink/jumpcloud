#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""jumpcloud: command."""

from __future__ import absolute_import

__version__ = '2.0.0'

import sys
import os
import json
from subprocess import Popen, PIPE

import requests

if sys.version_info[0] < 3:
    raise Exception("Python 3 Please")

# Configure API key authorization: x-api-key
if os.environ.get('JUMPCLOUD_API_KEY') is None:
    print("JUMPCLOUD_API_KEY=None")
    sys.exit(1)

def usage():
    """self: usage."""
    print("Usage: " + sys.argv[0] + " option ")
    print("""
    options:

      list-systems [json|os|os-version|hostname|serial|insights|state|fde|agent|root-ssh]
      list-systems-id
      get-systems-json [system_id]
      get-systems-remoteip [system_id]
      get-systems-os system_id
      get-systems-hostname [system_id]
      get-systems-users [system_id]
      get-systems-memberof [system_id]
      delete-system [system_id]

      list-users [json|suspended|locked|password-expired|not-activated|ldap-bind|mfa]
      get-user-email [user_id]

      list-usergroups [json]
      list-usergroups-members [group_id]
      list-usergroups-details [group_id]

      list-systemgroups [json]
      list-systemgroups-membership [group_id]
      get-systemgroups-name [group_id]

      set-systems-memberof system_id group_id
      set-users-memberof user_id system_id
      set-users-memberof_admin user_id system_id
      del-users-memberof user_id system_id

      list-systeminsights-hardware [json|csv]
      systeminsights-os-version [system_id]
      get-systeminsights-system-info [system_id]

      list-systeminsights-apps [system_id]
      list-systeminsights-programs [system_id]

      systeminsights-apps [system_id]
      systeminsights-programs [system_id]

      get-app [bundle_name]
      get-program [name]

      systeminsights-browser-plugins
      systeminsights-firefox-addons

      list-system-bindings [user_id]
      list-user-bindings [system_id]

      list-commands [json]
      get-command [command_id] [associations|systems|systemgroups]
      mod-command [command_id] [add|remove] [system_id]

      trigger [name]

      list-command-results [command_id]
      delete-command-results [command_id]

      update-system [system_id] [key] [value]

      add-systems-remoteip-awssg [system_id] [awssg_id] [port]

      events [startDate] [endDate] 
      Note: Dates must be formatted as RFC3339: "2020-01-15T16:20:01Z"
    """)
    print('Version: ' + str(__version__))
    sys.exit(0)


def systeminsights_os_version(system_id=None):
    """get: api v2 systeminsights system_id os_version."""
    skip = 0
    limit = 100
    jumpcloud_url = "https://console.jumpcloud.com/api/v2/systeminsights"

    if system_id:
        system_id = ''.join(system_id)
        _url = jumpcloud_url + "/" + str(system_id) + "/os_version"
        response = get_response_json(_url)
        print(json.dumps(response, indent=4))
        return response

    _url = jumpcloud_url + "/os_version?limit=" + str(limit) + "&skip=" + str(skip)
    response = get_response_json(_url)
    resultlist = response
    while len(response) > 0:
        skip += 100
        _url = jumpcloud_url + "/os_version?limit=" + str(limit) + "&skip=" + str(skip)
        response = get_response_json(_url)
        resultlist.extend(response)
    return resultlist


def list_command_results(command_id=None):
    """get: api commandresults command_id."""
    skip = 0
    limit = 100
    jumpcloud_url = "https://console.jumpcloud.com/api/commandresults"

    if command_id:
        command_id = ''.join(command_id)
        _url = jumpcloud_url + "/" + str(command_id)
        response = get_response_json(_url)
        print(json.dumps(response, indent=4))
        return response

    _url = jumpcloud_url + "?limit=" + str(limit) + "&skip=" + str(skip)
    response = get_response_json(_url)
    resultlist = response
    while len(response) > 0:
        skip += 100
        _url = jumpcloud_url + "?limit=" + str(limit) + "&skip=" + str(skip)
        response = get_response_json(_url)
        resultlist.extend(response)
    return resultlist


def delete_command_results(command_id):
    """delete: api commandresults command_id."""
    command_id = ''.join(command_id)
    _url = "https://console.jumpcloud.com/api/commandresults/" + str(command_id)
    response = requests.delete(_url,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'})
    print(response)
    return response
#QA1


def print_systems_users_json(system_id=None):
    """print: systems users json."""
    if system_id:
        system_id = ''.join(system_id)
    jdata = get_systems_users_json(system_id)
    print(json.dumps(jdata, sort_keys=True, indent=4))


def get_systems_users_json(system_id=None):
    """get: api v2 systems system_id users."""
    skip = 0
    limit = 100
    jumpcloud_url = "https://console.jumpcloud.com/api/v2/systems/"
    _url = jumpcloud_url + str(system_id) + "/users?limit=" + str(limit) + "&skip=" + str(skip)
    response_json = get_response_json(_url)
    return response_json


def get_systems_memberof_json(system_id=None):
    """get: api v2 systems system_id memberof."""
    skip = 0
    limit = 100
    jumpcloud_url = "https://console.jumpcloud.com/api/v2/systems/"
    _url = jumpcloud_url + str(system_id) + "/memberof?limit=" + str(limit) + "&skip=" + str(skip)
    response_json = get_response_json(_url)
    return response_json


#https://docs.jumpcloud.com/2.0/system-group-members-and-membership/
#manage-the-members-of-a-system-group
def set_systems_memberof(system_id, group_id, verbose=True):
    """post: api v2 systemgroups group_id members."""
    _url = "https://console.jumpcloud.com/api/v2/systemgroups/" + str(group_id) + "/members"

    data = {'op': 'add', 'type': 'system', 'id': system_id}
    encoded_body = json.dumps(data).encode('utf-8')
    response = requests.post(_url,
                           headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                    'Content-Type': 'application/json',
                                    'Accept': 'application/json'},
                           body=encoded_body)

    if verbose:
        print(str(response.status), str(response.json()))
    return str(response.status), str(response.json())
#QA2


def set_users_memberof(user_id, system_id, verbose=True):
    """post: api v2 systems system_id assocations."""
    #https://docs.jumpcloud.com/2.0/systems/manage-associations-of-a-system

    _url = "https://console.jumpcloud.com/api/v2/systems/" + str(system_id) + "/associations"

    data = {'op': 'add', 'type': 'user', 'id': user_id}
    encoded_body = json.dumps(data).encode('utf-8')
    response = requests.post(_url,
                           headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                    'Content-Type': 'application/json',
                                    'Accept': 'application/json'},
                           body=encoded_body)

    if verbose:
        print(str(response.status), str(response.json()))
    return str(response.status), str(response.json())
#QA2


def set_users_memberof_admin(user_id, system_id, verbose=True):
    """post: api v2 systems sysetem_id associations add sudo."""
    #https://docs.jumpcloud.com/2.0/systems/manage-associations-of-a-system

    _url = "https://console.jumpcloud.com/api/v2/systems/" + str(system_id) + "/associations"

    data = {'op': 'add', 'type': 'user', 'id': user_id,
            'attributes': {'sudo':{'enabled':True, 'withoutPassword': False}}
            }
    encoded_body = json.dumps(data).encode('utf-8')
    response = requests.post(_url,
                           headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                    'Content-Type': 'application/json',
                                    'Accept': 'application/json'},
                           body=encoded_body)

    if verbose:
        print(str(response.status), str(response.json()))
    return str(response.status), str(response.json())
#QA2


def del_users_memberof(user_id, system_id, verbose=True):
    """post: api v2 systems system_id assocations remove user_id."""
    #https://docs.jumpcloud.com/2.0/systems/manage-associations-of-a-system

    _url = "https://console.jumpcloud.com/api/v2/systems/" + str(system_id) + "/associations"

    data = {'op': 'remove', 'type': 'user', 'id': user_id}
    encoded_body = json.dumps(data).encode('utf-8')
    response = requests.post(_url,
                           headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                    'Content-Type': 'application/json',
                                    'Accept': 'application/json'},
                           body=encoded_body)

    if verbose:
        print(str(response.status), str(response.json()))
    return str(response.status), str(response.json())
#QA2


def print_systems_memberof(system_id=None):
    """print: get_systemgroups_name group_id."""
    if system_id:
        system_id = ''.join(system_id)
    jdata = get_systems_memberof_json(system_id)
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
    """get_systems_users_json: system_id."""
    if system_id:
        system_id = ''.join(system_id)
    jdata = get_systems_users_json(system_id)

    if len(jdata) == 1:
        print(json.dumps(jdata, indent=4))
        return True

    for line in jdata:
        print(line['id'])

    return True


#https://docs.jumpcloud.com/2.0/user-groups/list-all-users-groups
#https://github.com/TheJumpCloud/jcapi-python/tree/master/jcapiv2
#List all User Groups
#GET /usergroups
def list_usergroups_json():
    """print: get_usergroups_json."""
    jdata = get_usergroups_json(group_id=None)
    print(json.dumps(jdata, sort_keys=False, indent=4))


def list_usergroups():
    """print: get_usergroups_json."""
    jdata = get_usergroups_json(group_id=None)
    for line in jdata:
        print(str(line['id']) + ' "' + str(line['name']) + '"' )


def get_usergroups_json(group_id=None, skip=0, limit=100):
    """get: api v2 usergroups group_id."""
    if group_id:
        group_id = ''.join(group_id)
    else:
        group_id = ''

    jumpcloud_url = "https://console.jumpcloud.com/api/v2/usergroups/"

    _url = jumpcloud_url + str(group_id) + "?limit=" + str(limit) + "&skip=" + str(skip)
    response_json = get_response_json(_url)
    return response_json


def get_systemgroups_json(group_id=None):
    """get: api v2 systemgroups group_id."""
    jumpcloud_url = "https://console.jumpcloud.com/api/v2/systemgroups"
    if group_id:
        group_id = ''.join(group_id)
        _url = jumpcloud_url + "/" + str(group_id) + "?limit=100&skip=0"
    else:
        group_id = ''
        _url = jumpcloud_url + "?limit=100&skip=0"
    response_json = get_response_json(_url)
    return response_json


def list_systemgroups_json(group_id=None):
    """print: get_systemgroups_json."""
    jdata = get_systemgroups_json(group_id)
    print(json.dumps(jdata, sort_keys=True, indent=4))


def list_systemgroups():
    """print: get_systemgroups_json."""
    jdata = get_systemgroups_json(group_id=None)
    for line in jdata:
        print(line['id'] + ' "' + line['name'] + '"')


def systeminsights_browser_plugins():
    """get: api v2 systeminsights browser_plugins."""
    _url = "https://console.jumpcloud.com/api/v2/systeminsights/browser_plugins"
    response_json = get_response_json(_url)
    print(json.dumps(response_json, indent=4))
    return response_json


def systeminsights_firefox_addons():
    """get: api v2 systeminsights firefox_addons."""
    _url = "https://console.jumpcloud.com/api/v2/systeminsights/firefox_addons?limit = 100"
    response_json = get_response_json(_url)
    print(json.dumps(response_json, indent=4))
    return response_json


def systeminsights_apps(system_id=None): #GET /systeminsights/{system_id}/apps
    """get: get_systeminsights_list_apps_json."""
    if system_id:
        system_id = ''.join(system_id)

    count=0
    skip = 0
    limit = 100

    response = get_systeminsights_list_apps_json(system_id, skip, limit)
    print(json.dumps(response, sort_keys=False, indent=4))

    if len(response) == 1:
        print('I have spoken.') #Kuiil
        return

    count += len(response)

    while len(response) > 0:
        skip += 100
        response = get_systeminsights_list_apps_json(system_id, skip, limit)
        count += len(response)
        print(json.dumps(response, sort_keys=False, indent=4))
        if system_id is None:
            print('Count: ' + str(count))

    print('Count: ' + str(count))


#GET /systeminsights/{system_id}/apps
def get_systeminsights_list_apps_json(system_id=None, skip=0, limit=100):
    """get: api v2 systeminsights system_id apps."""
    jumpcloud_url = "https://console.jumpcloud.com/api/v2/systeminsights"
    if system_id:
        _url = jumpcloud_url + "/" + str(system_id)
        _url += "/apps?limit=" + str(limit) + "&skip=" + str(skip)
    else:
        _url = jumpcloud_url + "/apps?limit=" + str(limit) + "&skip=" + str(skip)

    response_json = get_response_json(_url)
    return response_json


def systeminsights_programs(system_id=None): #GET /systeminsights/{system_id}/programs
    """get: get_systeminsights_list_programs_json."""
    if len(system_id) != 0:
        system_id = ''.join(system_id)
    else:
        system_id = None

    count = 0
    skip = 0
    limit = 100

    response = get_systeminsights_list_programs_json(system_id, skip, limit)
    print(json.dumps(response, sort_keys=False, indent=4))

    if len(response) == 1:
        print('I have spoken.') #Kuiil
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


#GET /systeminsights/{system_id}/programs
def get_systeminsights_list_programs_json(system_id=None, skip=0, limit=100):
    """get: api v2 systeminsights programs."""
    jumpcloud_url = "https://console.jumpcloud.com/api/v2/systeminsights"
    if system_id is None:
        _url = jumpcloud_url + "/programs?limit=" + str(limit) + "&skip=" + str(skip)
    else:
        _url = jumpcloud_url + "/" + str(system_id)
        _url += "/programs?limit=" + str(limit) + "&skip=" + str(skip)

    response_json = get_response_json(_url)
    return response_json


def get_commands_json(command_id=None): #GET/api/commands/{id} #api.v1
    """get: api commands command_id."""
    if command_id:
        command_id = ''.join(command_id)
    else:
        command_id = ''
    _url = "https://console.jumpcloud.com/api/commands/" + str(command_id)
    response_json = get_response_json(_url)
    return response_json


def list_commands_json():
    """print: get_commands_json."""
    jdata = get_commands_json()
    print(json.dumps(jdata, sort_keys=True, indent=4))


def list_commands():
    """print: get_commands_json results."""
    jdata = get_commands_json()
    for data in jdata['results']:
        _line = data.get('id') + ' ' + data.get('name') + ' (' + data.get('commandType') + ') '
        _line += '["' + data.get('launchType') + '"] '
        print(_line)


#GET/api/v2/commands/{id}/[associations?,systems,systemgroups]
def get_commands_api2_json(command_id=None, segment=None):
    """get: api v2 commands command_id."""
    if command_id:
        command_id = ''.join(command_id)

    segments = ['associations','systems','systemgroups']

    if not segment in segments:
        print("Unknown option: " + str(segment))
        return str("Unknown option: " + str(segment))

    if segment == 'associations':
        param = "&targets=system"
    else:
        param = ""

    limit = 100
    skip  = 0

    jumpcloud_url = "https://console.jumpcloud.com/api/v2/commands"

    _url = jumpcloud_url + "/" + str(command_id) + "/" + str(segment)
    _url += "?limit=" + str(limit) + "&skip=" + str(skip) + str(param)

    response = get_response_json(_url)
    resultlist = response
    while len(response) > 0:
        skip += 100
        _url = jumpcloud_url + "/" + str(command_id) + "/" + str(segment)
        _url += "?limit=" + str(limit) + "&skip=" + str(skip) + str(param)
        response = get_response_json(_url)
        resultlist.extend(response)

    return resultlist


def list_commands_api2(command_id=None, segment=None):
    """print: get_commands_api2_json."""
    if command_id:
        command_id = ''.join(command_id)

    if segment:
        segment = ''.join(segment)

    jdata = get_commands_api2_json(command_id, segment)
    print(json.dumps(jdata, sort_keys=True, indent=4))


def mod_command(command_id=None, _op=None, system_id=None): #POST/api/v2/commands/{id}/associations
    """post: api v2 commands command_id associations."""
    if command_id:
        command_id = ''.join(command_id)

    ops = ['add','remove']

    if not _op in ops:
        print("Unknown option: " + str(_op))
        return False

    if system_id:
        system_id = ''.join(system_id)

    _url = "https://console.jumpcloud.com/api/v2/commands/" + str(command_id) + "/associations"

    data = {'op': _op, 'type': 'system', 'id': system_id}
    encoded_body = json.dumps(data).encode('utf-8')
    print(encoded_body)
    response = requests.post(_url,
                           headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                    'Content-Type': 'application/json',
                                    'Accept': 'application/json'},
                           body=encoded_body)

    print(str(response.status))
    print(response.json())
    return True
#QA3


#https://docs.jumpcloud.com/2.0/traits/filter
#https://console.jumpcloud.com/api/v2/systeminsights/5df3efcdf2d66c6f6a287136/
#apps?limit=100&filter=bundle_name:eq:ControlStrip
#GET /systeminsights/{system_id}/apps
def list_systeminsights_apps(system_id=None):
    """get: get_systeminsights_apps_json."""
    system_id = ''.join(system_id)

    count = 0
    skip = 0
    limit = 100

    response = get_systeminsights_apps_json(system_id, skip, limit)
    responselist = response

    while len(response) > 0:
        skip += 100
        response = get_systeminsights_apps_json(system_id, skip, limit)
        responselist = responselist + response

    for line in responselist:
        count += 1
        line_str = str(count) + ' ' + line['name']
        line_str += ' (' + line['bundle_name'] + ') Version: ' + line['bundle_short_version']
        print(line_str)


#GET /systeminsights/{system_id}/apps
def get_systeminsights_apps_json(system_id=None, skip=0, limit=100):
    """get: api v2 systeminsights system_id apps."""
    system_id = ''.join(system_id)
    jumpcloud_url = "https://console.jumpcloud.com/api/v2/systeminsights"
    _url = jumpcloud_url + "/" + str(system_id) + "/apps?limit=" + str(limit) + "&skip=" + str(skip)
    response_json = get_response_json(_url)
    return response_json


def list_systeminsights_programs(system_id=None): #GET /systeminsights/{system_id}/programs
    """get: get_systeminsights_programs_json."""
    system_id = ''.join(system_id)

    count = 0
    skip = 0
    limit = 100

    response = get_systeminsights_programs_json(system_id, skip, limit)
    responselist = response

    while len(response) > 0:
        skip += 100
        response = get_systeminsights_programs_json(system_id, skip, limit)
        responselist = responselist + response

    for line in responselist:
        count += 1
        line_str = str(count) + ' ' + line['name']
        line_str += ' (' + line['publisher'] + ') Version: ' + line['version']
        print(line_str)


#GET /systeminsights/{system_id}/programs
def get_systeminsights_programs_json(system_id=None, skip=0, limit=100):
    """get: api v2 systeminsights system_id programs."""
    system_id = ''.join(system_id)
    jumpcloud_url = "https://console.jumpcloud.com/api/v2/systeminsights"
    _url = jumpcloud_url + "/" + str(system_id) + "/programs?limit="
    _url += str(limit) + "&skip=" + str(skip)
    response_json = get_response_json(_url)
    return response_json


# api/v2/systeminsights/apps?limit = 100&skip = 0&filter=bundle_name:eq:Maps
def get_app(name=None): #GET /systeminsights/apps
    """get: get_systeminsights_app_json."""
    skip = 0
    limit = 100

    response = get_systeminsights_app_json(name, skip, limit)
    responselist = response

    while len(response) > 0:
        skip += 100
        response = get_systeminsights_app_json(name, skip, limit)
        responselist = responselist + response
    return responselist


def print_get_app(name=None):
    """print: get_app(name)."""
    name = ''.join(name)
    responselist = get_app(name)
    count=0
    for line in responselist:
        count += 1
        line_str = line['system_id']  + ' ' + line['name']
        line_str += ' (' + line['bundle_name'] + ') Version: ' + line['bundle_short_version']
        print(line_str)


# api/v2/systeminsights/apps?limit=100&skip=0&filter=bundle_name:eq:Maps
def get_systeminsights_app_json(name=None, skip=0, limit=100): #GET /systeminsights/apps
    """get: api v2 systeminsights apps."""
    jumpcloud_url = "https://console.jumpcloud.com/api/v2/systeminsights/apps"
    _url = jumpcloud_url + "?limit=" + str(limit) + "&skip="
    _url += str(skip) + "&filter=bundle_name:eq:" + str(name)
    response_json = get_response_json(_url)
    return response_json


# api/v2/systeminsights/programs?limit = 100&skip = 0&filter=name:eq:Microsoft Teams
def get_program(name=None): #GET /systeminsights/programs
    """get: get_systeminsights_program_json."""
    name = ''.join(name)

    count=0
    skip = 0
    limit = 100

    response = get_systeminsights_program_json(name, skip, limit)
    responselist = response

    while len(response) > 0:
        skip += 100
        response = get_systeminsights_program_json(name, skip, limit)
        responselist = responselist + response

    for line in responselist:
        count += 1
        line_str = line['system_id']  + ' ' + line['name']
        line_str += ' (' + line['publisher'] + ') Version: ' + line['version']
        print(line_str)


# api/v2/systeminsights/programs?limit=100&skip=0&filter=name:eq:Microsoft Teams
def get_systeminsights_program_json(name=None, skip=0, limit=100): #GET /systeminsights/programs
    """get: api v2 systeminsights programs."""
    jumpcloud_url = "https://console.jumpcloud.com/api/v2/systeminsights/programs"
    _url = jumpcloud_url + "?limit=" + str(limit) + "&skip=" + str(skip)
    _url += "&filter=name:eq:" + str(name)
    response_json = get_response_json(_url)
    return response_json


def run_trigger(trigger=None):
    """post: api command trigger."""
    trigger = ''.join(trigger)

    _url = "https://console.jumpcloud.com/api/command/trigger/" + str(trigger)
    encoded_body = json.dumps({})
    response = requests.post(_url,
                           headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                    'Content-Type': 'application/json'},
                           body=encoded_body)
    print(response)
    print(response.json())
    return response
#QA4


def update_system(system_id=None, key=None, value=None):
    """put: api systems systems_id."""
    system_id = ''.join(system_id)
    print(system_id)

    key    = ''.join(key)
    print(key)

    value    = ''.join(value)
    print(value)

    encoded_body = json.dumps({ key : value })

    print(encoded_body)

    _url = "https://console.jumpcloud.com/api/systems/" + str(system_id)

    response = requests.put(_url,
                           headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                    'Content-Type': 'application/json',
                                    'Accept': 'application/json'},
                           body=encoded_body)
    print(response.json())
    return response
#https://docs.jumpcloud.com/1.0/authentication-and-authorization/system-context
#https://docs.jumpcloud.com/1.0/systems/list-an-individual-system
#https://github.com/TheJumpCloud/SystemContextAPI/blob/master/examples/instance-shutdown-initd
#QA4


def get_system_bindings_json(user_id=None):
    """get: api v2 users user_id systems."""
    skip = 0
    limit = 100
    _url = "https://console.jumpcloud.com/api/v2/users/" + str(user_id) + "/systems"
    _url += "?limit=" + str(limit) + "&skip=" + str(skip)
    response = get_response_json(_url)
    resultlist = response
    while len(response) > 0:
        skip += 100
        _url = "https://console.jumpcloud.com/api/v2/users/" + str(user_id) + "/systems"
        _url += "?limit=" + str(limit) + "&skip=" + str(skip)
        response = get_response_json(_url)
        resultlist.extend(response)

    return resultlist


def list_system_bindings_json(user_id=None):
    """print: get_system_bindings_json user_id."""
    user_id = ''.join(user_id)
    jdata = get_system_bindings_json(user_id)
    print(json.dumps(jdata, sort_keys=True, indent=4))


def list_system_bindings(user_id=None):
    """print: get_system_bindings_json hostname."""
    user_id = ''.join(user_id)
    data = get_system_bindings_json(user_id)
    #print(data)
    #print(str(type(data)))
    for line in data:
        hostname = get_systems_hostname(line['id'])
        print(line['id'] + ' ' + str(hostname))


#https://docs.jumpcloud.com/2.0/systems/list-the-users-bound-to-a-system
#List the Users bound to a System
#GET/systems/{system_id}/users
def get_user_bindings_json(system_id=None):
    """get: api v2 systems system_id users."""
    skip = 0
    limit = 100
    _url = "https://console.jumpcloud.com/api/v2/systems/" + str(system_id) + "/users"
    _url += "?limit=" + str(limit) + "&skip=" + str(skip)

    response = get_response_json(_url)
    resultlist = response
    while len(response) > 0:
        skip += 100
        _url = "https://console.jumpcloud.com/api/v2/systems/" + str(system_id) + "/users"
        _url += "?limit=" + str(limit) + "&skip=" + str(skip)
        response = get_response_json(_url)
        resultlist.extend(response)
    return resultlist


def list_user_bindings_json(system_id=None):
    """print: get_user_bindings_json."""
    system_id = ''.join(system_id)
    jdata = get_user_bindings_json(system_id)
    print(json.dumps(jdata, sort_keys=True, indent=4))


def list_user_bindings(system_id=None):
    """print: get_user_bindings_json user_email."""
    system_id = ''.join(system_id)
    jdata = get_user_bindings_json(system_id)

    for line in jdata:
        user_email = get_user_email(line['id'])
        print(line['id'] + ' ' + str(user_email))


def get_systems_hostname(system_id=None):
    """return: str get_systems_json_single hostname."""
    system_id = ''.join(system_id)
    jdata = get_systems_json_single(system_id)
    #return str(jdata['hostname'])
    return str(jdata.get('hostname', None))


def print_systems_hostname(system_id=None):
    """print: get_systems_json_single hostname."""
    system_id = ''.join(system_id)
    jdata = get_systems_json_single(system_id)
    print(jdata['hostname'])


#def get_systems_remoteip(system_id=None, verbose=True) -> None:
def get_systems_remoteip(system_id=None, verbose=True):
    """return: str get_systems_json_single remoteIP."""
    system_id = ''.join(system_id)
    jdata = get_systems_json_single(system_id)
    if verbose:
        print(str(jdata['remoteIP']))
    return jdata['remoteIP']


def add_systems_remoteip_awssg(system_id, awssg_id, port=3389):
    """print: aws cli add remote ip."""
    remote_ip = get_systems_remoteip(system_id, verbose=False)
    print(remote_ip)
    print(awssg_id)

    #from subprocess import Popen, PIPE, STDOUT
    cmd = 'aws ec2 authorize-security-group-ingress --group-id '+str(awssg_id)
    cmd += ' --protocol tcp --port '+str(port)+' --cidr '+str(remote_ip)+'/32'

    #proc = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
    with Popen(cmd.split(), stdout=PIPE, stderr=PIPE) as proc:
        out = proc.stdout.readlines()
        err = proc.stderr.readlines()

    for __o in out:
        print('out: '+str(__o.decode('utf-8')))

    for __e in err:
        print('err: '+str(__e.decode('utf-8')))

    return out, err


def get_systems_json_single(system_id=None):
    """get: api systems system_id."""
    if system_id:
        _url = "https://console.jumpcloud.com/api/systems/" + str(system_id)
    else:
        _url = "https://console.jumpcloud.com/api/systems"
    response_json = get_response_json(_url)
    return response_json


def get_systems_json_response(skip, limit):
    """get: api systems multi."""
    _url = "https://console.jumpcloud.com/api/systems?skip=" + str(skip) + '&limit=' + str(limit)
    response_json = get_response_json(_url)
    return response_json


def get_systems_json():
    """return: json get_systems_json_response."""
    skip = 0
    data = get_systems_json_response(skip, limit = 100)
    totalcount = data['totalCount']
    resultlist = data['results']

    while len(data['results']) > 0:
        skip += 100
        data = get_systems_json_response(skip, limit = 100)
        resultlist.extend(data['results'])

    dictdata = { 'totalCount': totalcount, 'results': resultlist }
    jdata = json.dumps(dictdata)
    return json.loads(jdata)


def get_user_email(user_id=None):
    """return: str get_systemusers_json email."""
    if user_id:
        user_id = ''.join(user_id)
    jdata = get_systemusers_json_single(user_id)
    return str(jdata['email'])


def print_user_email(user_id=None):
    """print: get_systemusers_json email."""
    if user_id:
        user_id = ''.join(user_id)
        jdata = get_systemusers_json_single(user_id)
        #print(jdata)
        print(jdata['email'])
    else:
        print('None')


def get_systemgroups_name(group_id=None):
    """return: str get_systemgroups_json name."""
    if group_id:
        group_id = ''.join(group_id)
    jdata = get_systemgroups_json(group_id)
    return str(jdata['name'])


def print_systemgroups_name(group_id=None):
    """print: get_systemgroups_json name."""
    if group_id:
        group_id = ''.join(group_id)
        jdata = get_systemgroups_json(group_id)
        print(jdata['name'])
    else:
        print('None')


#https://docs.jumpcloud.com/2.0/system-group-members-and-membership/
#list-system-groups-group-membership
def list_systemgroups_membership(group_id=None, skip=0, limit=100):
    """get: api v2 systemgroups group_id membership."""
    group_id = ''.join(group_id)

    jumpcloud_url = "https://console.jumpcloud.com/api/v2/systemgroups"
    _url = jumpcloud_url + "/" + str(group_id) + "/membership"
    _url += "?limit=" + str(limit) + "&skip=" + str(skip)

    response = get_response_json(_url)
    resultlist = response
    while len(response) > 0:
        skip += 100
        _url = jumpcloud_url + "/" + str(group_id) + "/membership"
        _url += "?limit=" + str(limit) + "&skip=" + str(skip)
        response = get_response_json(_url)
        resultlist.extend(response)

    for data in resultlist:
        print(data['id'] + ' ' + get_systems_hostname(data.get('id')))


def list_usergroups_members(group_id=None, skip=0, limit=100):
    """get: api v2 usergroups group_id members."""
    group_id = ''.join(group_id)

    jumpcloud_url = "https://console.jumpcloud.com/api/v2/usergroups"
    _url = jumpcloud_url + "/" + str(group_id) + "/members"
    _url += "?limit=" + str(limit) + "&skip=" + str(skip)

    response = get_response_json(_url)
    resultlist = response
    while len(response) > 0:
        skip += 100
        _url = jumpcloud_url + "/" + str(group_id) + "/members"
        _url += "?limit=" + str(limit) + "&skip=" + str(skip)
        response = get_response_json(_url)
        resultlist.extend(response)

    users = []
    for user in resultlist:
        users.append(user.get('to').get('id'))

    for user_id in users:
        user_email = get_user_email(user_id)
        print(str(user_id) + ' ' + str(user_email))


def list_usergroups_details(group_id=None):
    """get: api v2 usergroups group_id."""
    group_id = ''.join(group_id)
    _url = "https://console.jumpcloud.com/api/v2/usergroups/" + str(group_id)
    response_json = get_response_json(_url)
    print(json.dumps(response_json, sort_keys=True, indent=4))
    return response_json


def get_systemusers_json_single(user_id=None):
    """get: api systemusers user_id."""
    if user_id:
        user_id = ''.join(user_id)
    else:
        user_id = ''
    _url = "https://console.jumpcloud.com/api/systemusers/" + str(user_id)
    response_json = get_response_json(_url)
    return response_json


def get_systemusers_json():
    """return: json get_systemusers_json_multi."""
    skip = 0
    limit = 100
    data = get_systemusers_json_multi(skip, limit)
    totalcount = data['totalCount']
    resultlist = data['results']

    while len(data['results']) > 0:
        skip += 100
        data = get_systemusers_json_multi(skip, limit=100)
        resultlist.extend(data['results'])

    dictdata = { 'totalCount': totalcount, 'results': resultlist }
    jdata = json.dumps(dictdata)
    return json.loads(jdata)


#def get_systemusers_json_multi(skip, limit):
#    """get: api systemusers json multi."""
#    _url = "https://console.jumpcloud.com/api/systemusers"
#    _url += "?skip=" + str(skip) + '&limit=' + str(limit)
#
#    http = urllib3.PoolManager(assert_hostname=False, cert_reqs='CERT_NONE')
#    response = http.request('GET', _url,
#                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
#                                     'Content-Type': CONTENT_TYPE,
#                                     'Accept': ACCEPT_TYPE})
#    return json.loads(response.data.decode('utf-8'))


def get_response_json(_url):
    """get: url: return json."""
    response = requests.get(_url,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'})
    return response.json()


def get_systemusers_json_multi(skip, limit):
    """get: api systemusers json: return dict."""
    _url = "https://console.jumpcloud.com/api/systemusers"
    _url += "?skip=" + str(skip) + '&limit=' + str(limit)
    response = get_response_json(_url)
    return response


def list_users():
    """print: get_systemusers_json users."""
    jdata = get_systemusers_json()
    if len(jdata) == 0:
        print('Zero (0) response')

    for data in jdata['results']:
        middlename = data.get('middlename')
        if middlename == "" or middlename is None:
            middlename = ' '
        else:
            middlename = ' ' + str(data.get('middlename')) + ' '

        _line = str(data.get('_id')) + ' ' + str(data.get('username'))
        _line += ' (' + str(data.get('displayname')) + ') '
        _line += '["' + str(data.get('firstname'))
        _line += str(middlename) + str(data.get('lastname')) + '"] '
        _line += str(data.get('email'))
        print(_line)


def list_users_suspended(_print=True):
    """return: dict get_systemusers_json suspended."""
    thisdict = {}
    jdata = get_systemusers_json()
    if len(jdata) == 0:
        print('Zero (0) response')
    for data in jdata['results']:
        suspended = data.get('suspended')
        if str(suspended) == 'True':
            _line = data.get('_id') + ' ' + data.get('username') + ' ' + data.get('email') + ' '
            _line += 'suspended:' + str(suspended)
            if _print:
                print(_line)
            thisdict[data.get('_id')] = data.get('email')
    return thisdict


def list_users_locked(_print=True):
    """return: dict get_systemusers_json account_locked."""
    thisdict = {}
    jdata = get_systemusers_json()
    if len(jdata) == 0:
        print('Zero (0) response')
    for data in jdata['results']:
        account_locked = data.get('account_locked')
        if str(account_locked) != 'False':
            _line = data.get('_id') + ' ' + data.get('username') + ' ' + data.get('email') + ' '
            _line += 'account_locked:' + str(account_locked)
            if _print:
                print(_line)
            thisdict[data.get('_id')] = data.get('email')
    return thisdict


def list_users_password_expired(_print=True):
    """return: dict get_systemusers_json password_expired."""
    thisdict = {}
    jdata = get_systemusers_json()
    if len(jdata) == 0:
        print('Zero (0) response')
    for data in jdata['results']:
        password_expired = data.get('password_expired')
        if str(password_expired) != 'False':
            _line = data.get('_id') + ' ' + data.get('username') + ' ' + data.get('email') + ' '
            _line += 'password_expired:' + str(password_expired)
            if _print:
                print(_line)
            thisdict[data.get('_id')] = data.get('email')
    return thisdict


def list_users_not_activated(_print=True):
    """return: dict get_systemusers_json activated."""
    thisdict = {}
    jdata = get_systemusers_json()
    if len(jdata) == 0:
        print('Zero (0) response')
    for data in jdata['results']:
        activated = data.get('activated')
        if str(activated) != 'True':
            _line = data.get('_id') + ' ' + data.get('username') + ' ' + data.get('email') + ' '
            _line += 'activated:' + str(activated)
            if _print:
                print(_line)
            thisdict[data.get('_id')] = data.get('email')
    return thisdict


def list_users_ldap_bind(_print=True):
    """return: dict get_systemusers_json ldap_bind."""
    thisdict = {}
    jdata = get_systemusers_json()
    if len(jdata) == 0:
        print('Zero (0) response')
    for data in jdata['results']:
        ldap_binding_user = data.get('ldap_binding_user')
        if str(ldap_binding_user) == 'True':
            _line = data.get('_id') + ' ' + data.get('username') + ' ' + data.get('email') + ' '
            _line += 'ldap_binding_user:' + str(ldap_binding_user)
            if _print:
                print(_line)
            thisdict[data.get('_id')] = data.get('email')
    return thisdict


def list_users_mfa():
    """print: get_systemusers_json mfa."""
    jdata = get_systemusers_json()
    if len(jdata) == 0:
        print('Zero (0) response')
    for data in jdata['results']:
        mfa_json = json.dumps(data.get('mfa'), sort_keys=True)
        _output = data.get('_id') + ' "' + data.get('email') + ' ' + str(mfa_json)
        print(_output)


def list_users_json():
    """print: get_systemusers_json."""
    response = get_systemusers_json()
    if len(response) == 0:
        print('Zero (0) response')
    print(json.dumps(response, sort_keys=True, indent=4))


def list_systems_json(system_id=None):
    """print: get_systems_json_single."""
    if system_id:
        system_id = ''.join(system_id)
        jdata = get_systems_json_single(system_id)
    else:
        jdata = get_systems_json_single()
    print(json.dumps(jdata, sort_keys=True, indent=4))


#def list_systems_id():
def list_systems_id(skip=0):
    """print: get_systems_id_json system_id."""
    skip = 0
    jdata = get_systems_id_json(skip, limit=100)
    for data in jdata['results']:
        print(data.get('_id'))

    while len(jdata['results']) > 0:
        skip += 100
        jdata = get_systems_id_json(skip, limit=100)
        for data in jdata['results']:
            print(data.get('_id'))


def get_systems_id_json(skip, limit):
    """get: api systems."""
    _url = "https://console.jumpcloud.com/api/systems?skip=" + str(skip) + '&limit=' + str(limit)
    response_json = get_response_json(_url)
    return response_json


def get_systems_id():
    """return: idList get_systems_id_json."""
    idlist = []
    skip = 0
    jdata = get_systems_id_json(skip, limit = 100)
    for data in jdata['results']:
        idlist.append(data.get('_id'))

    while len(jdata['results']) > 0:
        skip += 100
        jdata = get_systems_id_json(skip, limit = 100)
        for data in jdata['results']:
            idlist.append(data.get('_id'))

    return idlist


def list_systeminsights_hardware():
    """print: get_systeminsights_system_info_json hardware."""
    idlist = get_systems_id()

    for system_id in idlist:
        response = get_systeminsights_system_info_json(system_id, skip=0, limit=100)
        if len(response) == 0:
            print(str(system_id))
        for line in response:
            memgb = round(int(line['physical_memory']) / 1024 / 1024 / 1024)
            _line =  str(system_id) + ' ' + line['computer_name'] + ' (' + line['hostname'] + ') '
            _line += line['hardware_model'] + ' (' + line['hardware_vendor'] + ') '
            _line += line['cpu_type'] + ' (' + str(line['cpu_physical_cores']) + ') '
            _line += line['cpu_brand'] + ' ' + str(line['physical_memory'])
            _line += ' Bytes (' + str(memgb) + ' GB) ["'
            _line += str(line['hardware_serial']) + '"] '
            print(_line)


def list_systeminsights_hardware_csv():
    """print: get_systeminsights_system_info_json csv."""
    idlist = get_systems_id()

    for system_id in idlist:
        #print(system_id)
        response = get_systeminsights_system_info_json(system_id, skip=0, limit=100)
        if len(response) == 0:
            print(str(system_id))
        for line in response:
            memgb = round(int(line['physical_memory']) / 1024 / 1024 / 1024)
            #print(line)
            _line =  str(system_id) + ',' + line['computer_name'] + ',(' + line['hostname'] + '),'
            _line += str(line['hardware_model']).replace(",", " ")
            _line += ',(' + line['hardware_vendor'] + '),'
            _line += line['cpu_type'] + ',(' + str(line['cpu_physical_cores']) + '),'
            _line += line['cpu_brand'] + ',' + str(line['physical_memory'])
            _line += ' Bytes,(' + str(memgb) + ' GB),["'
            _line += str(line['hardware_serial']) + '"] '
            print(_line)


def list_systeminsights_hardware_json():
    """print: get_systeminsights_system_info_json."""
    #count = 0
    skip = 0
    limit = 100

    idlist = get_systems_id()

    for system_id in idlist:
        response = get_systeminsights_system_info_json(system_id, limit, skip)
        if len(response) == 0:
            response = {  'system_id' : system_id  }
        print(json.dumps(response, sort_keys=False, indent=4))


def get_systeminsights_system_info(system_id=None):
    """print: get_systeminsights_system_info_json system_id."""
    system_id = ''.join(system_id)
    jdata = get_systeminsights_system_info_json(system_id, skip=0, limit=100)
    print(json.dumps(jdata, sort_keys=False, indent=4))


#List System Insights System Info
#GET /systeminsights/system_info
#Valid filter fields are system_id and cpu_subtype.
#https://docs.jumpcloud.com/2.0/system-insights/list-system-insights-system-info
def get_systeminsights_system_info_json(system_id=None, limit=None, skip=None):
    """get: api v2 systeminsights system_info limit skip filter system_id."""
    skip = 0
    limit = 100

    system_id = ''.join(system_id)
    jumpcloud_url = "https://console.jumpcloud.com/api/v2/systeminsights/system_info"
    _url = jumpcloud_url + "?limit=" + str(limit) + "&skip=" + str(skip)
    _url += "&filter=system_id:eq:" + str(system_id)
    response_json = get_response_json(_url)
    return response_json


def list_systems():
    """print: get_systems_json hostname arch."""
    jdata = get_systems_json()
    for data in jdata['results']:
        print(str(data.get('_id')) + ' "'
              + str(data.get('displayName')) + '" ('
              + str(data.get('hostname'))  + ') '
              + str(data.get('os')) + ' '
              + str(data.get('version')) + ' '
              + str(data.get('arch')))


def list_systems_hostname():
    """print: get_systems_json hostname."""
    jdata = get_systems_json()
    for data in jdata['results']:
        print(str(data.get('_id')) + ' ' + str(data.get('hostname')))


def list_systems_os(_print=True):
    """return: dict get_systems_json os."""
    thisdict = {}
    jdata = get_systems_json()
    for data in jdata['results']:
        if _print:
            print(str(data.get('_id')) + ' ' + str(data.get('os')))
        thisdict[data.get('_id')] = data.get('os')
    return thisdict


def get_systems_os(system_id, _print=True):
    """return: str get_systems_json_single os."""
    system_id = ''.join(system_id)
    jdata = get_systems_json_single(system_id)
    if _print:
        print(str(jdata['os']))
    return jdata['os']


def list_systems_serial():
    """print: get_systems_json serialNumber."""
    jdata = get_systems_json()
    for data in jdata['results']:
        print(str(data.get('_id')) + ' ("' + str(data.get('serialNumber')) + '") ')


def list_systems_agent():
    """print: get_systems_json agentVersion."""
    jdata = get_systems_json()
    for data in jdata['results']:
        data_str = str(data.get('_id')) + ' ' + str(data.get('hostname'))
        data_str += ' ("' + str(data.get('agentVersion')) + '") '
        print(data_str)


def list_systems_os_version():
    """print: get_systems_json os version."""
    jdata = get_systems_json()
    for data in jdata['results']:
        data_str = str(data.get('_id')) + ' ' + str(data.get('os')) + ' ' + str(data.get('version'))
        data_str += ' ' + str(data.get('arch'))
        print(data_str)


def list_systems_insights():
    """print: get_systems_json systemInsights."""
    jdata = get_systems_json()
    for data in jdata['results']:
        _line = str(data.get('_id')) + ' "' + str(data.get('displayName'))
        _line += '" (' + str(data.get('hostname'))
        _line += ') ' + str(data.get('os')) + ' ' + str(data.get('version'))
        _line += ' ' + str(data.get('arch'))
        _line += ' ' + json.dumps(str(data.get('systemInsights')))
        print(_line)


def list_systems_state():
    """print: get_systems_json lastContact."""
    jdata = get_systems_json()
    for data in jdata['results']:
        _line = str(data.get('_id')) + ' "' + str(data.get('displayName'))
        _line += '" (' + str(data.get('hostname'))
        _line += ') '+ str(data.get('lastContact')) + ' active: '
        _line += str(json.dumps(data.get('active')))
        print(_line)


def list_systems_fde():
    """print: get_systems_json fde."""
    jdata = get_systems_json()
    if len(jdata) == 0:
        print('Zero (0) response')
    if len(jdata) == 1:
        print(str(jdata))
        print('I have spoken.') #Kuiil
        return

    for data in jdata['results']:
        fde_json = json.dumps(data.get('fde'), sort_keys=True)
        _line = str(data.get('_id')) + ' "' + str(data.get('displayName'))
        _line += '" (' + str(data.get('hostname'))
        _line += ') ' + str(data.get('os')) + ' ' + str(data.get('version'))
        _line += ' ' + str(data.get('arch'))
        _line += ' ' + str(data.get('fileSystem')) + ' [' + str(fde_json) + ']'
        print(_line)


def list_systems_root_ssh():
    """print: get_systems_json allowSshRootLogin."""
    jdata = get_systems_json()
    for data in jdata['results']:
        root_ssh = json.dumps(data.get('allowSshRootLogin'), sort_keys=True)
        _line = str(data.get('_id')) + ' "' + str(data.get('displayName'))
        _line += '" (' + str(data.get('hostname'))
        _line += ') ' + str(data.get('os'))
        _line += ' allowSshRootLogin ' + ' [' + str(root_ssh) + ']'
        print(_line)


def delete_system(system_id=None):
    """delete: api systems system_id."""
    if system_id:
        system_id = ''.join(system_id)
    else:
        print('system_id required')
        return {'delete':False, 'system_id':None}

    _url = "https://console.jumpcloud.com/api/systems/" + str(system_id)

    response = requests.delete(_url,
                            headers={'x-api-key': os.environ.get('JUMPCLOUD_API_KEY'),
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'})
    print(response)
    return response
#QA1


#https://support.jumpcloud.com/support/s/article/jumpcloud-events-api1
def get_events_json(startdate=None, enddate=None):
    """get: events.""" # i think this url is depricated.
    startdate = ''.join(startdate)
    enddate =   ''.join(enddate)
    jumpcloud_url = "https://events.jumpcloud.com/events"
    _url = jumpcloud_url + "?startDate=" + str(startdate) + '&endDate=' + str(enddate)
    response_json = get_response_json(_url)
    return response_json


def events(start=None, end=None):
    """print: get_events_json."""
    jdata = get_events_json(start, end)
    print(json.dumps(jdata, sort_keys=False, indent=4))


options = {
  'list-systems'                    : list_systems,
  'list-systems-id'                 : list_systems_id,
  'list-systems-hostname'           : list_systems_hostname,
  'list-systems-serial'             : list_systems_serial,
  'list-systems-json'               : list_systems_json,
  'get-systems-json'                : list_systems_json,
  'get-systems-remoteip'            : get_systems_remoteip,
  'add-systems-remoteip-awssg'      : add_systems_remoteip_awssg,
  'list-systems-os'                 : list_systems_os,
  'list-systems-agent'              : list_systems_agent,
  'list-systems-os-version'         : list_systems_os_version,
  'list-systeminsights-hardware'    : list_systeminsights_hardware,
  'list-systeminsights-hardware-json' : list_systeminsights_hardware_json,
  'list-systeminsights-hardware-csv'  : list_systeminsights_hardware_csv,
  'list-systems-insights'           : list_systems_insights,
  'list-systems-state'              : list_systems_state,
  'list-systems-fde'                : list_systems_fde,
  'list-systems-root-ssh'           : list_systems_root_ssh,
  'delete-system'                   : delete_system,
  'systeminsights-os-version'       : systeminsights_os_version,
  'list-usergroups'                 : list_usergroups,
  'list-usergroups-json'            : list_usergroups_json,
  'list-usergroups-members'         : list_usergroups_members,
  'list-usergroups-details'         : list_usergroups_details,
  'list-systemgroups'               : list_systemgroups,
  'list-systemgroups-json'          : list_systemgroups_json,
  'list-systemgroups-membership'    : list_systemgroups_membership,
  'list-users'                      : list_users,
  'list-users-json'                 : list_users_json,
  'list-users-mfa'                  : list_users_mfa,
  'list-users-suspended'            : list_users_suspended,
  'list-users-locked'               : list_users_locked,
  'list-users-password-expired'     : list_users_password_expired,
  'list-users-not-activated'        : list_users_not_activated,
  'list-users-ldap-bind'            : list_users_ldap_bind,
  'list-commands'                   : list_commands,
  'list-commands-json'              : list_commands_json,
  'get-command'                     : list_commands_api2,
  'mod-command'                     : mod_command,
  'systeminsights-apps'             : systeminsights_apps,
  'systeminsights-programs'         : systeminsights_programs,
  'systeminsights-browser-plugins'  : systeminsights_browser_plugins,
  'systeminsights-firefox-addons'   : systeminsights_firefox_addons,
  'list-system-bindings'            : list_system_bindings,
  'list-system-bindings-json'       : list_system_bindings_json,
  'list-user-bindings'              : list_user_bindings,
  'list-user-bindings-json'         : list_user_bindings_json,
  'get-systems-users'               : get_systems_users,
  'get-systems-os'                  : get_systems_os,
  'get-systems-memberof'            : print_systems_memberof,
  'set-systems-memberof'            : set_systems_memberof,
  'set-users-memberof'              : set_users_memberof,
  'set-users-memberof-admin'        : set_users_memberof_admin,
  'del-users-memberof'              : del_users_memberof,
  'get-systems-users-json'          : print_systems_users_json,
  'get-systems-hostname'            : print_systems_hostname,
  'get-user-email'                  : print_user_email,
  'get-systemgroups-name'           : print_systemgroups_name,
  'update-system'                   : update_system,
  'list-systeminsights-apps'        : list_systeminsights_apps,
  'list-systeminsights-programs'    : list_systeminsights_programs,
  'get-app'                         : print_get_app,
  'get-program'                     : get_program,
  'get-systeminsights-system-info'  : get_systeminsights_system_info,
  'list-command-results'            : list_command_results,
  'delete-command-results'          : delete_command_results,
  'events'                          : events,
  'trigger'                         : run_trigger,
}

args1 = ['list-systems','list-users','list-commands','list-systeminsights-hardware',
         'list-systemgroups']

args2 = ['trigger','systeminsights-os-version','systeminsights-apps',
         'systeminsights-programs','get-systems-json','get-systems-users',
         'get-systems-hostname','get-user-email','get-systems-remoteip',
         'list-systems-id','list-usergroups-members','list-usergroups-details',
         'list-systemgroups-membership','list-systeminsights-apps','list-systeminsights-programs',
         'get-systeminsights-system-info','get-app','get-program','list-system-bindings',
         'list-user-bindings','list-user-bindings-json','list-system-bindings-json',
         'get-systems-users-json','delete-system','get-systems-memberof','get-systemgroups-name',
         'list-command-results','delete-command-results','get-systems-os']

def main():
    """main: app."""
    try:
        if sys.argv[1:]:
            if sys.argv[1] == "--help":
                usage()
            elif sys.argv[1] == "--version":
                print(__version__)
            elif sys.argv[1] == "events" or sys.argv[1] == "get-command":
                options[sys.argv[1]](sys.argv[2],sys.argv[3])
            elif sys.argv[1] == "add-systems-remoteip-awssg":
                options[sys.argv[1]](sys.argv[2],sys.argv[3],sys.argv[4])
            elif sys.argv[1] == "update-system" or sys.argv[1] == "mod-command":
                options[sys.argv[1]](sys.argv[2],sys.argv[3], sys.argv[4])
            elif sys.argv[1] == "set-systems-memberof" or sys.argv[1] == "set-users-memberof" \
                    or sys.argv[1] == "set-users-memberof-admin":
                options[sys.argv[1]](sys.argv[2],sys.argv[3])
            elif sys.argv[1] == "del-users-memberof":
                options[sys.argv[1]](sys.argv[2],sys.argv[3])
            elif len(sys.argv) > 2 and sys.argv[1] in args1:
                options[str(sys.argv[1] + '-' + sys.argv[2])]()
            elif sys.argv[1] in args2:
                options[sys.argv[1]](sys.argv[2:])
            else:
                options[sys.argv[1]]()
        else:
            usage()
    except KeyError as _e:
        print("KeyError: " + str(_e))
        sys.exit(1)


if __name__ == '__main__':
    main()
