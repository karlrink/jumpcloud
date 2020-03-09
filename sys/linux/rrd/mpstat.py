#!/usr/bin/env python

import sys
sys.dont_write_bytecode = True
import subprocess
import json
import re

def get_mpstat():

    collect="mpstat"
    p = subprocess.Popen(collect, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    exit_code = p.wait()
    if (exit_code != 0):
        print('Error: ' + str(err) + ' ' + str(output))
        return exit_code
        #sys.exit(1)

    multilines = output.splitlines()

    odict = {}
    count = 0
    for line in multilines:
       count += 1
       #print(str(count) + ': ' + line)
       odict[count] = line

    mpstat_line = odict[4]
    mpstat_vals = mpstat_line.split()
    num_items = len(mpstat_vals)
    #print(num_items)

    last_item = len(mpstat_vals) - 1
    mpstat_idle  = mpstat_vals[int(last_item)]
    mpstat_gnice = mpstat_vals[int(last_item) - 1 ]
    mpstat_guest = mpstat_vals[int(last_item) - 2 ]
    mpstat_steal = mpstat_vals[int(last_item) - 3 ]
    mpstat_soft  = mpstat_vals[int(last_item) - 4 ]
    mpstat_irq   = mpstat_vals[int(last_item) - 5 ]
    mpstat_iowait = mpstat_vals[int(last_item) - 6 ]
    mpstat_sys    = mpstat_vals[int(last_item) - 7 ]
    mpstat_nice   = mpstat_vals[int(last_item) - 8 ]
    mpstat_usr    = mpstat_vals[int(last_item) - 9 ]

    #print(mpstat_idle)
    #print(mpstat_gnice)
    #print(mpstat_guest)
    #print(mpstat_steal)
    #print(mpstat_soft)
    #print(mpstat_irq)
    #print(mpstat_iowait)
    #print(mpstat_sys)
    #print(mpstat_nice)

    mpstat_rrdupdate =  'N:' + mpstat_idle
    mpstat_rrdupdate +=  ':' + mpstat_gnice
    mpstat_rrdupdate +=  ':' + mpstat_guest
    mpstat_rrdupdate +=  ':' + mpstat_steal
    mpstat_rrdupdate +=  ':' + mpstat_soft
    mpstat_rrdupdate +=  ':' + mpstat_irq
    mpstat_rrdupdate +=  ':' + mpstat_iowait
    mpstat_rrdupdate +=  ':' + mpstat_sys
    mpstat_rrdupdate +=  ':' + mpstat_nice

    json_data = '{"rrd":"%s","val":"%s"}' % ('mpstat', mpstat_rrdupdate)

    return json.loads(json_data)


if __name__ == "__main__":
    output = get_mpstat()
    print(json.dumps(output, sort_keys=True, indent=4))


