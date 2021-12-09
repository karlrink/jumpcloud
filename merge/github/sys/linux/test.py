#!/usr/bin/env python

import json

from proc import meminfo
proc_meminfo = meminfo.get_meminfo()
print(json.dumps(proc_meminfo, sort_keys=True, indent=4))

from rrd import free
rrd_free = free.get_free()
print(json.dumps(rrd_free, sort_keys=True, indent=4))

from rrd import uptime
rrd_uptime = uptime.get_uptime()
print(json.dumps(rrd_uptime, sort_keys=True, indent=4))

from rrd import df
rrd_df = df.get_df()
print(json.dumps(rrd_df, sort_keys=True, indent=4))

from rrd import ps
rrd_ps = ps.get_ps()
print(json.dumps(rrd_ps, sort_keys=True, indent=4))

#mpstat #iostat , rely on sysstat package

from rrd import mpstat
rrd_mpstat = mpstat.get_mpstat()
print(json.dumps(rrd_mpstat, sort_keys=True, indent=4))

from rrd import iostat
rrd_iostat = iostat.get_iostat()
print(json.dumps(rrd_iostat, sort_keys=True, indent=4))


