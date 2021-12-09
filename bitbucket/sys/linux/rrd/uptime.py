#!/usr/bin/env python

import sys
sys.dont_write_bytecode = True
import subprocess
import json
import re

def get_uptime():
#def get_uptime(_print=False):
    collect="uptime"
    p = subprocess.Popen(collect, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    exit_code = p.wait()
    if (exit_code != 0):
        print('Error: ' + str(err) + ' ' + str(output))
        sys.exit(1)

    multilines = output.splitlines()

    odict = {}
    count = 0
    for line in multilines:
       count += 1
       #if _print: print(str(count) + ': ' + line)
       odict[count] = line

    ##########################################################
    # uptime
    # 21:46:27 up 1 day, 20:18,  2 users,  load average: 0.00, 0.00, 0.00
    # 21:49:47 up 0 min,  1 user,  load average: 0.21, 0.07, 0.03
    # uptime_line
    # { "rrd": "uptime", "val": "N:1:5:0.82:0.77:0.74" }

    uptime_line = odict[1]
    uptime_vals = uptime_line.split(",")

    if len(uptime_vals) == 6:
        #if _print: print('six items')
        offset = 1
    elif len(uptime_vals) == 5:
        #if _print: print('five items')
        offset = 0
    else:
        offset = 0

    uptime_time_line = uptime_vals[0]
    if len(uptime_vals) == 6:
        uptime_day = uptime_time_line.split()[2]
    else:
        uptime_day = 0
    uptime_users_line = uptime_vals[1 + offset]
    uptime_users = uptime_users_line.split()[0]
    uptime_1_line = uptime_vals[2 + offset]
    uptime_1 = uptime_1_line.split(":")[1]
    uptime_5 = uptime_vals[3 + offset]
    uptime_15 = uptime_vals[4 + offset]

    #uptime_rrdupdate =  str(epochtime) + ':' + str(uptime_day)
    uptime_rrdupdate = 'N:' + str(uptime_day)
    uptime_rrdupdate += ':' + uptime_users.strip() + ':' + uptime_1.strip()
    uptime_rrdupdate += ':' + uptime_5.strip() + ':' + uptime_15.strip()

    ##########################################################

    sys_json_data = '     {"rrd":"%s","val":"%s"}' % ('uptime', uptime_rrdupdate)

    return json.loads(sys_json_data)

if __name__ == "__main__":
    output = get_uptime()
    print(json.dumps(output, sort_keys=True, indent=4))


