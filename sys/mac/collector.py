#!/usr/bin/env python2

url = 'https://monitor.nationsinfocorp.com:443/collector'

__version__ = 'mac.001.a1'

import json
import os
import urllib2
import subprocess
import re

import time
import signal

import sys
sys.dont_write_bytecode = True
import ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

def get_system_id():
    jcagent_conf = '/opt/jc/jcagent.conf'
    with open(jcagent_conf, 'r') as jcconf:
        jdata = json.load(jcconf)
    system_id = jdata['systemKey']
    return str(system_id)

def collector(system_id):
    alert_data = None
    rrdList = []

    #from proc import meminfo
    #proc_meminfo = meminfo.get_meminfo()
    #proc_meminfo = get_meminfo()


    #from rrd import free
    #rrd_free = free.get_free()
    #rrd_free = get_free()
    #for item in rrd_free:
    #    rrdList.append(item)

    #from rrd import uptime
    #rrd_uptime = uptime.get_uptime()
#    rrd_uptime = get_uptime()
#    rrdList.append(rrd_uptime)

    #from rrd import df
    #rrd_df = df.get_df()
    #rrd_df = get_df()
    #rrdList.append(rrd_df)

    #from rrd import ps
    #rrd_ps = ps.get_ps()
    rrd_ps = get_ps()
    rrdList.append(rrd_ps)

    #mpstat and iostat , rely on sysstat package

    #if os.path.isfile('/usr/bin/mpstat'):
    #    #from rrd import mpstat
    #    #rrd_mpstat = mpstat.get_mpstat()
    #    rrd_mpstat = get_mpstat()
    #    rrdList.append(rrd_mpstat)

    #if os.path.isfile('/usr/bin/iostat'):
    #    #from rrd import iostat
    #    #rrd_iostat = iostat.get_iostat()
    #    rrd_iostat = get_iostat()
    #    rrdList.append(rrd_iostat)
       
    #json_data  = '{ "system_id": "' + str(system_id) + '"'

    json_data  = '{ "system_id": "' + str(system_id) + '",'
    #json_data += '"meminfo": ' + str(json.dumps(proc_meminfo)) + ','
    json_data += '"rrdata": ' + str(json.dumps(rrdList))

    #alert_data = { 'Error': 'yes', 'Help': 'Please'}
    if alert_data:
        json_data += ',"alert": ' + str(json.dumps(alert_data))

    json_data += '}'
    return json.loads(json_data)


def post(system_id, json_data):
    try:
        request = urllib2.Request(url + '?system_id=' + str(system_id))
        request.add_header('content-type', 'application/json')
        request.add_header('x-api-key', system_id)
        post_data = json.dumps(json.JSONDecoder().decode(json_data))
        response = urllib2.urlopen(request, post_data, timeout=20)
        #print(response.read())
        return response.read()
    except Exception as e:
        #print('HTTP Post error: ' + str(e))
        return str(e)

def check_pid(pid):        
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

def daemonize():
    pidfile = '/var/run/collector.pid'
    if os.path.isfile(pidfile):
        with open(pidfile, 'r') as pidhandle:
            pid = pidhandle.read()
        if len(pid) == 0:
            print('Invalid ' + str(pidfile))
            sys.exit(1)
        if check_pid(int(pid)) is True:
            print('Already running pid: ' + str(pid))
            sys.exit(1)
    fpid = os.fork()
    if fpid != 0:
        try:
            p = open(pidfile, 'w+')
            p.write(str(fpid))
            p.close()
        except IOError as e:
            print(str(e))
            os.kill(fpid, signal.SIGSTOP)
            sys.exit(1)
        sys.exit(0)

    system_id = get_system_id()
    while True:
        json_data = collector(system_id)
        response = post(system_id, json.dumps(json_data))
        time.sleep(300)
    return True

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


def get_uptime():
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
    # uptime (linux)
    # 21:46:27 up 1 day, 20:18,  2 users,  load average: 0.00, 0.00, 0.00
    # 21:49:47 up 0 min,  1 user,  load average: 0.21, 0.07, 0.03
    # uptime_line
    # { "rrd": "uptime", "val": "N:1:5:0.82:0.77:0.74" }
    #
    # uptime (mac)
    # 21:57  up 34 days, 23:46, 7 users, load averages: 1.91 2.20 2.25
    # 22:00  up 1 min, 2 users, load averages: 14.23 3.65 1.33


    uptime_line = odict[1]
    uptime_vals = uptime_line.split(",")

    if len(uptime_vals) == 4:
        #if _print: print('six items')
        offset = 1
    elif len(uptime_vals) == 3:
        #if _print: print('five items')
        offset = 0
    else:
        offset = 0

    #uptime_time_line = uptime_vals[0]
    #if len(uptime_vals) == 6:
    #    uptime_day = uptime_time_line.split()[2]
    #else:
    #    uptime_day = 0

    uptime_time_line = uptime_vals[0]

    uptime_users_line = uptime_vals[1 + offset]
    uptime_users = uptime_users_line.split()[0]

    uptime_1_line = uptime_vals[2 + offset]

    print(str(uptime_1_line))
    print('EXIT.EXIT')
    sys.exit()

    uptime_1 = uptime_1_line.split(":")[1]
    uptime_5 = uptime_1_line.split(":")[2]
    uptime_15 = uptime_1_line.split(":")[3]
    #uptime_5 = uptime_vals[3 + offset]
    #uptime_15 = uptime_vals[4 + offset]

    uptime_rrdupdate = 'N:' + str(uptime_day)
    uptime_rrdupdate += ':' + uptime_users.strip() + ':' + uptime_1.strip()
    uptime_rrdupdate += ':' + uptime_5.strip() + ':' + uptime_15.strip()
    json_data = '{"rrd":"%s","val":"%s"}' % ('uptime', uptime_rrdupdate)
    return json.loads(json_data)

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

    root_fs_size = root_fs_line.split()[0 + offset]
    root_fs_used = root_fs_line.split()[1 + offset]
    root_fs_avail = root_fs_line.split()[2 + offset]
    root_fs_use = root_fs_line.split()[3 + offset]
    root_fs_name = root_fs_line.split()[4 + offset ]

    root_rrdupdate = 'N:' + root_fs_size
    root_rrdupdate += ':' + root_fs_used + ':' + root_fs_avail
    root_rrdupdate += ':' + root_fs_use[:-1]
    json_data = '{"rrd":"%s","val":"%s"}' % ('root', root_rrdupdate)
    return json.loads(json_data)

def get_ps():
    collect="ps -ef"
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

    number_of_procs = len(odict)
    number_of_defunct = 0
    for num in odict:
        line = odict[num]
        
        if re.search(r'<defunct>', line): #this.may.or.maynot.work for mac
            number_of_defunct += 1

    ps_rrdupdate = 'N:' + str(number_of_procs)
    ps_rrdupdate += ':' + str(number_of_defunct)
    json_data = '{"rrd":"%s","val":"%s"}' % ('ps', ps_rrdupdate)
    return json.loads(json_data)

def get_vm_stat():
#vm_stat
#Mach Virtual Memory Statistics: (page size of 4096 bytes)
#Pages free:                             3588620.
#Pages active:                           1690815.
#Pages inactive:                         1413599.
#Pages speculative:                       275361.
#Pages throttled:                              0.
#Pages wired down:                        826315.
#Pages purgeable:                          72100.
#"Translation faults":                 772980571.
#Pages copy-on-write:                   14236754.
#Pages zero filled:                    572561088.
#Pages reactivated:                       307921.
#Pages purged:                            529883.
#File-backed pages:                       698254.
#Anonymous pages:                        2681521.
#Pages stored in compressor:             3176023.
#Pages occupied by compressor:            593253.
#Decompressions:                        44165435.
#Compressions:                          53964351.
#Pageins:                               46853435.
#Pageouts:                                  1499.
#Swapins:                               54565528.
#Swapouts:                              56827840.
    pass


def get_sysctl_vm_swapusage():
#sysctl vm.swapusage
#vm.swapusage: total = 4096.00M  used = 2884.75M  free = 1211.25M  (encrypted)
    pass



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
            #print(this_disk_name)
            if this_disk_name == 'Linux':
                continue
            elif this_disk_name == 'Device:':
                continue
            elif this_disk_name == 'Device':
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


if __name__ == '__main__':
    if sys.argv[1:]:
        if sys.argv[1] == "--daemon":
            daemonize()
            sys.exit(0)

    system_id = get_system_id()
    json_data = collector(system_id)
    print(json.dumps(json_data, sort_keys=True, indent=4))
    response = post(system_id, json.dumps(json_data))
    print(response)


