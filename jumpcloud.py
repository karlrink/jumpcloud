#!/usr/bin/env python3

from __future__ import print_function
import time
from pprint import pprint

import jcapiv1
from jcapiv1.rest import ApiException as ApiException1

import jcapiv2
from jcapiv2.rest import ApiException as ApiException2


import os
import sys
import json

def usage():
    print("Usage: " + sys.argv[0] + " option")
    print("""
    options:

      list_os_version
      list_user_groups
      list_users

    """)

# Configure API key authorization: x-api-key
if os.environ.get('JUMPCLOUD_API_KEY') is None:
    print("JUMPCLOUD_API_KEY=None")
    sys.exit(1)

#    configuration.api_key['x-api-key'] = os.environ.get('JUMPCLOUD_API_KEY')
#    # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
#    # configuration.api_key_prefix['x-api-key'] = 'Bearer'
#
#    content_type = 'application/json' # str |  (default to application/json)
#    accept = 'application/json' # str |  (default to application/json)
#    limit = 3 # int |  (optional) (default to 10)
#    skip = 0 # int | The offset into the records to return. (optional) (default to 0)
#    filter = ['[]'] # list[str] | Supported operators are: eq (optional) (default to [])
#    x_org_id = '' # str |  (optional) (default to )

content_type = 'application/json' # str |  (default to application/json)
accept = 'application/json' # str |  (default to application/json)
limit = 3 # int |  (optional) (default to 10)
skip = 0 # int | The offset into the records to return. (optional) (default to 0)
filter = ['[]'] # list[str] | Supported operators are: eq (optional) (default to [])
x_org_id = '' # str |  (optional) (default to )



def list_os_version():
    configuration = jcapiv2.Configuration()
    configuration.api_key['x-api-key'] = os.environ.get('JUMPCLOUD_API_KEY')
    try: # List System Insights OS Version
        api_instance = jcapiv2.SystemInsightsApi(jcapiv2.ApiClient(configuration))
        api_response = api_instance.systeminsights_list_os_version(content_type, accept, limit=limit, skip=skip, filter=filter, x_org_id=x_org_id)
        pprint(api_response)
        #jdata = json.loads(json.dumps(str(api_response)))
        #print(jdata)
    except ApiException2 as e:
        print("Exception when calling SystemInsightsApi->systeminsights_list_os_version: %s\n" % e)

def list_user_groups():
    configuration = jcapiv2.Configuration()
    configuration.api_key['x-api-key'] = os.environ.get('JUMPCLOUD_API_KEY')
    try:
        api_instance = jcapiv2.UserGroupsApi(jcapiv2.ApiClient(configuration))
        user_groups = api_instance.groups_user_list(content_type, accept)
        pprint(user_groups)
    except ApiException2 as e:
        print("Exception when calling UserGroupsApi->groups_user_list: %s\n" % e)

def list_users():
    configuration = jcapiv1.Configuration()
    configuration.api_key['x-api-key'] = os.environ.get('JUMPCLOUD_API_KEY')
    try:
        api_instance = jcapiv1.SystemusersApi(jcapiv1.ApiClient(configuration))
        users = api_instance.systemusers_list(content_type, accept)
        pprint(users)
    except ApiException1 as e:
        print("Exception when calling SystemusersApi->systemusers_list: %s\n" % err)

        
options = {
  'list_os_version'  : list_os_version,
  'list_user_groups' : list_user_groups,
  'list_users'       : list_users,
}

if __name__ == '__main__':

    if sys.argv[1:]:
        if sys.argv[1] == "--help":
            usage()
            sys.exit(0)
        try:
            options[sys.argv[1]]()
        except KeyError as e:
            print("KeyError: " + str(e))
            sys.exit(1)
    else:
        usage()
        sys.exit(1)

  



