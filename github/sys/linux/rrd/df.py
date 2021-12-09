#!/usr/bin/env python

import sys
sys.dont_write_bytecode = True
import subprocess
import json

def get_df(disk='/'):

    collect="df -m"
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

    for key in odict:
        val = odict[key]
        #if val.endswith('/'):
        if val.endswith(disk):
            root_fs_line = val

    #print(root_fs_line)

    root_fs_vals = root_fs_line.split()
    #print 'root_fs_line ' + str(root_fs_line)
    #['/dev/vda1', '32G', '2.6G', '28G', '9%', '/']
    #['410G', '9.5G', '380G', '3%', '/']

    if len(root_fs_vals) == 6:
        #print 'six items'
        offset = 1
    elif len(root_fs_vals) == 5:
        #print 'five items'
        offset = 0
    else:
        offset = 0

    #print 'DIE DIE DIE'
    #return False

    root_fs_size = root_fs_line.split()[0 + offset]
    #print 'root_fs_size: ' + root_fs_size

    root_fs_used = root_fs_line.split()[1 + offset]
    #print 'root_fs_used: ' + root_fs_used

    root_fs_avail = root_fs_line.split()[2 + offset]
    #print 'root_fs_avail: ' + root_fs_avail

    root_fs_use = root_fs_line.split()[3 + offset]
    #print 'root_fs_use: ' + root_fs_use
    #print 'root_fs_use trim: ' + root_fs_use[:-1]

    root_fs_name = root_fs_line.split()[4 + offset ]
    #print 'root_fs_name: ' + root_fs_name

    #root_rrdupdate =  str(epochtime) + ':' + root_fs_size
    root_rrdupdate = 'N:' + root_fs_size
    root_rrdupdate += ':' + root_fs_used + ':' + root_fs_avail
    root_rrdupdate += ':' + root_fs_use[:-1]

    #thisname = 'root'
    #if debug: print thisname + ' ' + str(root_rrdupdate)

    #json_data += '{"rrd":"swap","val":"%s"}]' % (swap_rrdupdate)
    json_data = '{"rrd":"%s","val":"%s"}' % ('root', root_rrdupdate)

    return json.loads(json_data)


if __name__ == "__main__":
    output = get_df(disk='/')
    print(json.dumps(output, sort_keys=True, indent=4))


