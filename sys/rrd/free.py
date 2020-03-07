#!/usr/bin/env python

import sys
sys.dont_write_bytecode = True
import subprocess
import json

def get_free():

    collect="free -m"
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
       #print(str(count) + ': ' + line)
       odict[count] = line

    free_mem_line = odict[2]
    free_swap_line = odict[3]
    #print 'free_mem is: ' + free_mem_line

    mem_total = free_mem_line.split()[1]
    mem_used = free_mem_line.split()[2]
    mem_free = free_mem_line.split()[3]
    mem_shared = free_mem_line.split()[4]
    mem_buffers = free_mem_line.split()[5]
    mem_cached = free_mem_line.split()[6]

    mem_rrdupdate = 'N:' + mem_total
    mem_rrdupdate += ':' + mem_used + ':' + mem_free
    mem_rrdupdate += ':' + mem_shared + ':' + mem_buffers
    mem_rrdupdate += ':' + mem_cached

    swap_total = free_swap_line.split()[1]
    swap_used = free_swap_line.split()[2]
    swap_free = free_swap_line.split()[3]

    swap_rrdupdate = 'N:' + swap_total
    swap_rrdupdate += ':' + swap_used + ':' + swap_free

    json_data = '[{"rrd":"mem","val":"%s"},' % (mem_rrdupdate)
    json_data += '{"rrd":"swap","val":"%s"}]' % (swap_rrdupdate)

    return json.loads(json_data)

    #free -m
    #1:               total        used        free      shared  buff/cache   available
    #2: Mem:           1989         736         126           1        1125        1104
    #3: Swap:          1023           3        1020
    #[{"rrd":"mem","val":"N:1989:736:126:1:1125:1104"},
    #{"rrd":"swap","val":"N:1023:3:1020"}]

if __name__ == "__main__":
    output = get_free()
    print(json.dumps(output, sort_keys=True, indent=4))
    #print(output)
    #print(json.dumps(json.loads([ output ])))


