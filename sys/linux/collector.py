#!/usr/bin/env python2

import json
import os

def get_system_id():
    jcagent_conf = '/opt/jc/jcagent.conf'
    with open(jcagent_conf, 'r') as jcconf:
        jdata = json.load(jcconf)
    system_id = jdata['systemKey']
    return str(system_id)

from proc import meminfo
proc_meminfo = meminfo.get_meminfo()
#print(json.dumps(proc_meminfo, sort_keys=True, indent=4))

rrdList = []

from rrd import free
rrd_free = free.get_free()
#print(json.dumps(rrd_free, sort_keys=True, indent=4))
for item in rrd_free:
    rrdList.append(item)

from rrd import uptime
rrd_uptime = uptime.get_uptime()
#print(json.dumps(rrd_uptime, sort_keys=True, indent=4))
rrdList.append(rrd_uptime)

from rrd import df
rrd_df = df.get_df()
#print(json.dumps(rrd_df, sort_keys=True, indent=4))
rrdList.append(rrd_df)

from rrd import ps
rrd_ps = ps.get_ps()
#print(json.dumps(rrd_ps, sort_keys=True, indent=4))
rrdList.append(rrd_ps)

#mpstat and iostat , rely on sysstat package

if os.path.isfile('/usr/bin/mpstat'):
    from rrd import mpstat
    rrd_mpstat = mpstat.get_mpstat()
    #print(json.dumps(rrd_mpstat, sort_keys=True, indent=4))
    rrdList.append(rrd_mpstat)

if os.path.isfile('/usr/bin/iostat'):
    from rrd import iostat
    rrd_iostat = iostat.get_iostat()
    #print(json.dumps(rrd_iostat, sort_keys=True, indent=4))
    rrdList.append(rrd_iostat)
   


system_id = get_system_id()
#system_id = '1234567'
json_data  = '{ "system_id": "' + str(system_id) + '",'
json_data += '"meminfo": ' + str(json.dumps(proc_meminfo)) + ','
json_data += '"rrdata": ' + str(json.dumps(rrdList)) 
json_data += '}'

#print(json_data)
#print(json.dumps(json.loads(json_data), sort_keys=True, indent=4))



import urllib2
url = 'http://127.0.0.1:5000/collector'

import os
import ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

if __name__ == '__main__':

    print(json.dumps(json.loads(json_data), sort_keys=True, indent=4))

    try:
        request = urllib2.Request(url + '?system_id=' + str(system_id))
        request.add_header('content-type', 'application/json')
        request.add_header('x-api-key', system_id)
        post_data = json.dumps(json.JSONDecoder().decode(json_data))
        response = urllib2.urlopen(request, post_data, timeout=20)
        print(response.read())
    except Exception as e:
        print('HTTP Post error: ' + str(e))


