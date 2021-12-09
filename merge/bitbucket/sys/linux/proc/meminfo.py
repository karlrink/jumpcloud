#!/usr/bin/env python

__version__ = 'meminfo.01a'

import sys
sys.dont_write_bytecode = True
import json

def get_meminfo():

    with open('/proc/sys/vm/swappiness', 'r') as proc_swappiness:
        swappiness = int(proc_swappiness.read().strip())

    with open('/proc/meminfo', 'r') as proc_meminfo:
        meminfo = proc_meminfo.readlines()

    # kernels before 3.14 (rh6) do not have MemAvailable...
    # https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=34e431b0ae398fc54ea69ff85ec700722c9da773
    MemAvailable = -1

    for line in meminfo:
        if line.startswith('MemTotal'):
            MemTotal = int(line.split(':')[1].split()[0])
        if line.startswith('MemFree'):
            MemFree = int(line.split(':')[1].split()[0])
        if line.startswith('MemAvailable'):
            MemAvailable = int(line.split(':')[1].split()[0])
        if line.startswith('SwapTotal'):
            SwapTotal = int(line.split(':')[1].split()[0])
        if line.startswith('SwapFree'):
            SwapFree = int(line.split(':')[1].split()[0])
        if line.startswith('Shmem'):
            Shmem = int(line.split(':')[1].split()[0])
        if line.startswith('Buffers'):
            Buffers = int(line.split(':')[1].split()[0])
        if line.startswith('Cached'):
            Cached = int(line.split(':')[1].split()[0])

    #if MemAvailable == -1:
    #    # Backport "MemAvailable" field to /proc/meminfo in Red Hat Enterprise Linux 6
    #    # https://access.redhat.com/solutions/776393
    #    # vm.meminfo_legacy_layout=0
    #    try:
    #        import os
    #        os.system("/sbin/sysctl -w vm.meminfo_legacy_layout=0")
    #    except Exception as e:
    #        print 'Exception: ' + str(e)

    output = {
    'swappiness':str(swappiness),
    'MemTotal':str(MemTotal),
    'MemFree': str(MemFree),
    'SwapTotal':str(SwapTotal),
    'SwapFree':str(SwapFree),
    'Shmem': str(Shmem),
    'Buffers': str(Buffers),
    'Cached':str(Cached)
    }

    if MemAvailable is not -1:
        output["MemAvailable"] = str(MemAvailable)
    else:
        output["vm.meminfo_legacy_layout"] = 1

    return output

if __name__ == "__main__":
    output = get_meminfo()
    print(json.dumps(output, sort_keys=True, indent=4))

