#!/usr/bin/env python3

from __future__ import print_function
import time
import jcapiv2
from jcapiv2.rest import ApiException
from pprint import pprint

import os
import sys
import json

def usage():
    print("Usage: " + sys.argv[0] + " option")
    print("""
    options:

      list_os_version

    """)

# Configure API key authorization: x-api-key
configuration = jcapiv2.Configuration()
if os.environ.get('JUMPCLOUD_API_KEY') is None:
    print("JUMPCLOUD_API_KEY=None")
    sys.exit(1)
else:
    configuration.api_key['x-api-key'] = os.environ.get('JUMPCLOUD_API_KEY')
    # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
    # configuration.api_key_prefix['x-api-key'] = 'Bearer'

    content_type = 'application/json' # str |  (default to application/json)
    accept = 'application/json' # str |  (default to application/json)
    limit = 3 # int |  (optional) (default to 10)
    skip = 0 # int | The offset into the records to return. (optional) (default to 0)
    filter = ['[]'] # list[str] | Supported operators are: eq (optional) (default to [])
    x_org_id = '' # str |  (optional) (default to )


def list_os_version():
    try:
        api_instance = jcapiv2.SystemInsightsApi(jcapiv2.ApiClient(configuration))
        # List System Insights OS Version
        api_response = api_instance.systeminsights_list_os_version(content_type, accept, limit=limit, skip=skip, filter=filter, x_org_id=x_org_id)
        #pprint(api_response)
        #print(api_response)
        #print(str(api_response))
        #jdata = json.loads(str(api_response))
        #jdata = json.loads('{' + str(api_response) + '}')
        #print(str(jdata))
        #print(api_response)
        #jdata = json.loads('{response: ' + str(api_response) + '}')
        #jdata = {'response': api_response}
        #print(jdata)
        #j = json.dumps(jdata)
        #jdata = json.dumps(api_response)
        #jdata = json.dumps('{response: '+ str(api_response))
        #jdata = json.loads(json.dumps('{response: '+ str(api_response) + '}'))
        #print(jdata['response'])

        #r = { 'response': api_response }
        #print(r)
        #for k,v in r:
        #    print(k)
        #j = json.dumps(api_response)

        #jdata = json.loads(json.dumps('{ response: '+ str(api_response) + '}'))
        jdata = json.loads(json.dumps(str(api_response)))
        print(jdata)


    except ApiException as e:
        print("Exception when calling SystemInsightsApi->systeminsights_list_os_version: %s\n" % e)

options = {
  'list_os_version' : list_os_version,
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

  



