#!/usr/bin/env python

import json

from proc import meminfo
#proc_meminfo = meminfo.get_meminfo()
#print(json.dumps(proc_meminfo, sort_keys=True, indent=4))

from rrd import free
rrd_free = free.get_free()
print(json.dumps(rrd_free, sort_keys=True, indent=4))







