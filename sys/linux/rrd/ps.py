#!/usr/bin/env python

import sys
sys.dont_write_bytecode = True
import subprocess
import json
import re

def get_ps():

    collect="ps -ef"
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

    number_of_procs = len(odict)
    number_of_defunct = 0
    for num in odict:
        line = odict[num]
        
        if re.search(r'<defunct>', line):
            number_of_defunct += 1

    ps_rrdupdate = 'N:' + str(number_of_procs)
    ps_rrdupdate += ':' + str(number_of_defunct)

    json_data = '{"rrd":"%s","val":"%s"}' % ('ps', ps_rrdupdate)

    return json.loads(json_data)


if __name__ == "__main__":
    output = get_ps()
    print(json.dumps(output, sort_keys=True, indent=4))


