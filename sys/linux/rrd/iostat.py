#!/usr/bin/env python

import sys
sys.dont_write_bytecode = True
import subprocess
import json
import re

def get_iostat():

    collect="iostat -d"
    p = subprocess.Popen(collect, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    exit_code = p.wait()
    if (exit_code != 0):
        print('Error: ' + str(err) + ' ' + str(output))
        return exit_code

    multilines = output.splitlines()

    odict = {}
    count = 0
    for line in multilines:
       count += 1
       #print(str(count) + ': ' + line)
       odict[count] = line

    disk_tps = disk_blkreads = disk_blkwrtns = disk_blkrd = disk_blkwr = 0
    for key,value in odict.iteritems():
        line = value.split()
        if line:
            this_disk_name = line[0]
            if this_disk_name == 'Linux':
                continue
            elif this_disk_name == 'Device:':
                continue

            this_disk_tps  = line[1]
            this_disk_blkreads  = line[2]
            this_disk_blkwrtns  = line[3]
            this_disk_blkrd  = line[4]
            this_disk_blkwr  = line[5]

            disk_tps = disk_tps + float(this_disk_tps)
            disk_blkreads = disk_blkreads + float(this_disk_blkreads)
            disk_blkwrtns = disk_blkwrtns + float(this_disk_blkwrtns)
            disk_blkrd = disk_blkrd + float(this_disk_blkrd)
            disk_blkwr = disk_blkwr + float(this_disk_blkwr)


    iostat_rrdupdate = 'N:' + str(disk_tps)
    iostat_rrdupdate += ':' + str(disk_blkreads) + ':' + str(disk_blkwrtns)
    iostat_rrdupdate += ':' + str(disk_blkrd) + ':' + str(disk_blkwr)

    json_data = '{"rrd":"%s","val":"%s"}' % ('iostat', iostat_rrdupdate)

    return json.loads(json_data)


if __name__ == "__main__":
    output = get_iostat()
    print(json.dumps(output, sort_keys=True, indent=4))


