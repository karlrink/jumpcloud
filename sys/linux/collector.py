#!/usr/bin/env python2

__version__ = '007'

import json
import os
import urllib2
import subprocess
import re

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

try:
    import config
    url = config.param['url']
    system_id = config.param['system_id']
except ImportError:
    url = 'https://monitor.nationsinfocorp.com:443/collector'
    system_id = get_system_id()

def collector(system_id):

    alert_data = {}
    rrdList = []

    #from proc import meminfo
    #proc_meminfo = meminfo.get_meminfo()
    proc_meminfo = get_meminfo()


    #from rrd import free
    #rrd_free = free.get_free()
    rrd_free = get_free()
    for item in rrd_free:
        rrdList.append(item)

    #from rrd import uptime
    #rrd_uptime = uptime.get_uptime()
    rrd_uptime = get_uptime()
    rrdList.append(rrd_uptime)

    #from rrd import df
    #rrd_df = df.get_df()
    rrd_df = get_df()
    rrdList.append(rrd_df)

    #from rrd import ps
    #rrd_ps = ps.get_ps()
    rrd_ps, alert_ps = get_ps()
    rrdList.append(rrd_ps)
    if alert_ps:
        alert_data.update(alert_ps)

    #mpstat and iostat , rely on sysstat package

    if os.path.isfile('/usr/bin/mpstat'):
        #from rrd import mpstat
        #rrd_mpstat = mpstat.get_mpstat()
        rrd_mpstat = get_mpstat()
        rrdList.append(rrd_mpstat)

    if os.path.isfile('/usr/bin/iostat'):
        #from rrd import iostat
        #rrd_iostat = iostat.get_iostat()
        rrd_iostat = get_iostat()
        rrdList.append(rrd_iostat)

    dbconf = '/etc/db.conf'
    mysqlSocket = '/var/run/mysqld/mysqld.sock'
    if os.path.isfile(dbconf):
        if os.path.exists(mysqlSocket):
            mysql_data, sbm_data, mysql_alert = get_mysql(dbconf, mysqlSocket)
            if mysql_data:
                rrdList.append(json.loads(mysql_data))
            if sbm_data:
                rrdList.append(json.loads(sbm_data))
            if mysql_alert:
                alert_data.update(mysql_alert)

    if os.path.isfile('/usr/bin/virsh'):
        #apt-get install -y python-libvirt
        #import libvirt

        _uri = 'qemu://'
        _host = ''
        runningDict = ListDomainsDetailedClass(_uri, _host).get()
        rrd_virsh = runningDict['rrdata'] 
        rrdList.extend(rrd_virsh)

    #make sure time is working (ntp/time check)
    #ntp = False
    #if os.path.isfile('/usr/bin/ntpq'):
    #    rrd_ntpq = get_ntpq()
    #    if rrd_ntpq:
    #        rrdList.append(rrd_ntpq)
    #        ntp = True

    if os.path.isfile('/usr/bin/chronyc'):
        rrd_chronyc, alert_chronyc = get_chronyc()
        if rrd_chronyc:
            rrdList.append(rrd_chronyc)
        if alert_chronyc:
            alert_data = alert_chronyc
    else:
        alert_data = {'chrony': 'service not installed'}
        

    #if not ntp:
    #    alert_data = { 'ntp': 'service not running'}
        
    
    #alert_data = { 'Error': 'yes', 'Help': 'Please'}

    json_data  = '{ "system_id": "' + str(system_id) + '",'
    #json_data += '"meminfo": ' + str(json.dumps(proc_meminfo)) + ','
    json_data += '"rrdata": ' + str(json.dumps(rrdList))
    if alert_data:
        #print(alert_data)
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
    import time
    import signal
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
        sys.exit(0)

    if not system_id:
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
        return False

    multilines = output.splitlines()

    odict = {}
    count = 0
    for line in multilines:
        if 'Mem:' in line:
            #print(line)
            free_mem_line = line
        if 'Swap:' in line:
            #print(line)
            free_swap_line = line

        #count += 1
        #print(str(count) + ': ' + line)
        #odict[count] = line
       
    #free_mem_line = odict[2]
    #free_swap_line = odict[3]
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
        return False

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
        return False

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
    alert_data = {}
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
        
        if re.search(r'<defunct>', line):
            number_of_defunct += 1
            alert_data[number_of_defunct] = str(line)

    #alert_data[1] = '503 19591 19580   0  6:57PM ttys010    0:00.00 defunct'

    ps_rrdupdate = 'N:' + str(number_of_procs)
    ps_rrdupdate += ':' + str(number_of_defunct)
    json_data = '{"rrd":"%s","val":"%s"}' % ('ps', ps_rrdupdate)
    return json.loads(json_data), alert_data

def get_mpstat():
    collect="mpstat"
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

def get_mysql(dbconf, mysqlSocket):

    #dbconf = '/etc/db.conf'
    #mysqlSocket = '/var/run/mysqld/mysqld.sock'

    mysql_data = sbm_data = alert_data = ''

    try:
      import mysql.connector
    except ImportError as e:
      print(str(e))
      print('    redhat install: yum install mysql-connector-python')
      print('    debian install: apt-get install python-mysql.connector')
      return False

    try:
        with open(dbconf) as conf:
            for line in conf:
                if line.startswith("define('dbUser'"):
                    dbUser = line.split(',')[1].strip('\'').split('\'')[0]
                if line.startswith("define('dbPass'"):
                    dbPass = line.split(',')[1].strip('\'').split('\'')[0]
    except IOError as e:
        print(str(e))
        return False

    try:
        config = {
          'user': dbUser,
          'password': dbPass,
          'unix_socket': mysqlSocket,
          'database': 'mysql',
          'raise_on_warnings': True,
        }
    except UnboundLocalError as e:
        print('Error UnboundLocalError ' + str(e))
        if "local variable 'dbUser' referenced before assignment" in e:
            print('No dbUser var ' + str(e))
            return False

    if not os.path.exists(mysqlSocket):
        print('not os.path.exists ' + str(mysqlSocket))
        return False

    #collect mysql stats...
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as e:
        print(str(e))
        return False

    cursor = cnx.cursor(buffered=True)
    try:
        #get mysql version
        sql = "select version();"
        cursor.execute(sql)
        select_version = cursor.fetchone()

        if str(select_version[0]).startswith("10"):
            sql = "show all slaves status;"
        else:
            sql = "show slave status;"

        #get slave status
        cursor.execute(sql)
        if cursor.rowcount > 0:
            show_slave_status = dict(zip(cursor.column_names, cursor.fetchone()))
        else:
            #cursor.close()
            #cnx.close()
            #msg = 'Error: show_slave_status: cursor.rowcount > 0'
            #return msg
            show_slave_status = ''

        #get status
        sql = "show status;"
        cursor.execute(sql)
        if cursor.rowcount > 0:
            show_status = cursor.fetchall()
        else:
            show_status = ''

    except mysql.connector.Error as e:
        print(str(e))
        return False

    cursor.close()
    cnx.close()

    # we now have show_slave_status fetchone()
    # we now have show_status fetchall()

    #print(str(select_version))
    #print(str(show_slave_status))
    #print(str(show_status))

    #collect mysql show_status...
    # yeah, we could do: Aborted_clients = Aborted_connects = etc... = str(0)
    # but its easier to view and align with the server side this way
    Aborted_clients      = str(0)
    Aborted_connects     = str(0)
    Access_denied_errors = str(0)
    Bytes_received       = str(0)
    Bytes_sent           = str(0)
    Connections          = str(0)
    Created_tmp_files    = str(0)
    Innodb_buffer_pool_pages_data    = str(0)
    Innodb_buffer_pool_bytes_data    = str(0)
    Innodb_buffer_pool_bytes_dirty   = str(0)
    Innodb_buffer_pool_pages_flushed = str(0)
    Innodb_buffer_pool_pages_free    = str(0)
    Innodb_buffer_pool_pages_total   = str(0)
    Innodb_buffer_pool_reads         = str(0)
    Innodb_data_pending_fsyncs       = str(0)
    Innodb_data_pending_reads        = str(0)
    Innodb_data_pending_writes       = str(0)
    Innodb_data_reads                = str(0)
    Innodb_data_writes               = str(0)
    Innodb_dblwr_writes              = str(0)
    Innodb_row_lock_current_waits    = str(0)
    Innodb_row_lock_time             = str(0)
    Innodb_row_lock_time_avg         = str(0)
    Innodb_row_lock_time_max         = str(0)
    Innodb_num_open_files            = str(0)
    Innodb_row_lock_waits            = str(0)
    Innodb_rows_read                 = str(0)
    Innodb_rows_updated              = str(0)
    Innodb_rows_deleted              = str(0)
    Innodb_rows_inserted             = str(0)
    Max_used_connections             = str(0)
    Memory_used       = str(0)
    Open_files        = str(0)
    Open_tables       = str(0)
    Opened_files      = str(0)
    Opened_tables     = str(0)
    Qcache_hits       = str(0)
    Queries           = str(0)
    Questions         = str(0)
    Slave_connections = str(0)
    Slaves_connected  = str(0)
    Slow_queries      = str(0)
    Threads_connected = str(0)
    Threads_running   = str(0)
    Uptime            = str(0)

    for row in show_status:
        #print(str(row))

        if row[0] == 'Aborted_clients':
          Aborted_clients = str(row[1])

        if row[0] == 'Aborted_connects':
          Aborted_connects = str(row[1])

        if row[0] == 'Access_denied_errors':
          Access_denied_errors = str(row[1])

        if row[0] == 'Bytes_received':
          Bytes_received = str(row[1])

        if row[0] == 'Bytes_sent':
          Bytes_sent = str(row[1])

        if row[0] == 'Connections':
          Connections = str(row[1])

        if row[0] == 'Created_tmp_files':
          Created_tmp_files = str(row[1])

        if row[0] == 'Innodb_buffer_pool_pages_data':
          Innodb_buffer_pool_pages_data = str(row[1])

        if row[0] == 'Innodb_buffer_pool_bytes_data':
          Innodb_buffer_pool_bytes_data = str(row[1])

        if row[0] == 'Innodb_buffer_pool_bytes_dirty':
          Innodb_buffer_pool_bytes_dirty = str(row[1])

        if row[0] == 'Innodb_buffer_pool_pages_flushed':
          Innodb_buffer_pool_pages_flushed = str(row[1])

        if row[0] == 'Innodb_buffer_pool_pages_free':
          Innodb_buffer_pool_pages_free = str(row[1])

        if row[0] == 'Innodb_buffer_pool_pages_total':
          Innodb_buffer_pool_pages_total = str(row[1])

        if row[0] == 'Innodb_buffer_pool_reads':
          Innodb_buffer_pool_reads = str(row[1])

        if row[0] == 'Innodb_data_pending_fsyncs':
          Innodb_data_pending_fsyncs = str(row[1])

        if row[0] == 'Innodb_data_pending_reads':
          Innodb_data_pending_reads = str(row[1])

        if row[0] == 'Innodb_data_pending_writes':
          Innodb_data_pending_writes = str(row[1])

        if row[0] == 'Innodb_data_reads':
          Innodb_data_reads = str(row[1])

        if row[0] == 'Innodb_data_writes':
          Innodb_data_writes = str(row[1])

        if row[0] == 'Innodb_dblwr_writes':
          Innodb_dblwr_writes = str(row[1])

        if row[0] == 'Innodb_row_lock_current_waits':
          Innodb_row_lock_current_waits = str(row[1])

        if row[0] == 'Innodb_row_lock_time':
          Innodb_row_lock_time = str(row[1])

        if row[0] == 'Innodb_row_lock_time_avg':
          Innodb_row_lock_time_avg = str(row[1])

        if row[0] == 'Innodb_row_lock_time_max':
          Innodb_row_lock_time_max = str(row[1])

        if row[0] == 'Innodb_num_open_files':
          Innodb_num_open_files = str(row[1])

        if row[0] == 'Innodb_row_lock_waits':
          Innodb_row_lock_waits = str(row[1])

        if row[0] == 'Innodb_rows_read':
          Innodb_rows_read = str(row[1])

        if row[0] == 'Innodb_rows_updated':
          Innodb_rows_updated = str(row[1])

        if row[0] == 'Innodb_rows_deleted':
          Innodb_rows_deleted = str(row[1])

        if row[0] == 'Innodb_rows_inserted':
          Innodb_rows_inserted = str(row[1])

        if row[0] == 'Max_used_connections':
          Max_used_connections = str(row[1])

        if row[0] == 'Memory_used':
          Memory_used = str(row[1])

        if row[0] == 'Open_files':
          Open_files = str(row[1])

        if row[0] == 'Open_tables':
          Open_tables = str(row[1])

        if row[0] == 'Opened_files':
          Opened_files = str(row[1])

        if row[0] == 'Opened_tables':
          Opened_tables = str(row[1])

        if row[0] == 'Qcache_hits':
          Qcache_hits = str(row[1])

        if row[0] == 'Queries':
          Queries = str(row[1])

        if row[0] == 'Questions':
          Questions = str(row[1])

        if row[0] == 'Slave_connections':
          Slave_connections = str(row[1])

        if row[0] == 'Slaves_connected':
          Slaves_connected = str(row[1])

        if row[0] == 'Slow_queries':
          Slow_queries = str(row[1])

        if row[0] == 'Threads_connected':
          Threads_connected = str(row[1])

        if row[0] == 'Threads_running':
          Threads_running = str(row[1])

        if row[0] == 'Uptime':
          Uptime = str(row[1])

    mysql_rrdupdate = 'N'
    mysql_rrdupdate +=  ':' + Aborted_clients
    mysql_rrdupdate +=  ':' + Aborted_connects
    mysql_rrdupdate +=  ':' + Access_denied_errors
    mysql_rrdupdate +=  ':' + Bytes_received
    mysql_rrdupdate +=  ':' + Bytes_sent
    mysql_rrdupdate +=  ':' + Connections
    mysql_rrdupdate +=  ':' + Created_tmp_files
    mysql_rrdupdate +=  ':' + Innodb_buffer_pool_pages_data
    mysql_rrdupdate +=  ':' + Innodb_buffer_pool_bytes_data
    mysql_rrdupdate +=  ':' + Innodb_buffer_pool_bytes_dirty
    mysql_rrdupdate +=  ':' + Innodb_buffer_pool_pages_flushed
    mysql_rrdupdate +=  ':' + Innodb_buffer_pool_pages_free
    mysql_rrdupdate +=  ':' + Innodb_buffer_pool_pages_total
    mysql_rrdupdate +=  ':' + Innodb_buffer_pool_reads
    mysql_rrdupdate +=  ':' + Innodb_data_pending_fsyncs
    mysql_rrdupdate +=  ':' + Innodb_data_pending_reads
    mysql_rrdupdate +=  ':' + Innodb_data_pending_writes
    mysql_rrdupdate +=  ':' + Innodb_data_reads
    mysql_rrdupdate +=  ':' + Innodb_data_writes
    mysql_rrdupdate +=  ':' + Innodb_dblwr_writes
    mysql_rrdupdate +=  ':' + Innodb_row_lock_current_waits
    mysql_rrdupdate +=  ':' + Innodb_row_lock_time
    mysql_rrdupdate +=  ':' + Innodb_row_lock_time_avg
    mysql_rrdupdate +=  ':' + Innodb_row_lock_time_max
    mysql_rrdupdate +=  ':' + Innodb_num_open_files
    mysql_rrdupdate +=  ':' + Innodb_row_lock_waits
    mysql_rrdupdate +=  ':' + Innodb_rows_read
    mysql_rrdupdate +=  ':' + Innodb_rows_updated
    mysql_rrdupdate +=  ':' + Innodb_rows_deleted
    mysql_rrdupdate +=  ':' + Innodb_rows_inserted
    mysql_rrdupdate +=  ':' + Max_used_connections
    mysql_rrdupdate +=  ':' + Memory_used
    mysql_rrdupdate +=  ':' + Open_files
    mysql_rrdupdate +=  ':' + Open_tables
    mysql_rrdupdate +=  ':' + Opened_files
    mysql_rrdupdate +=  ':' + Opened_tables
    mysql_rrdupdate +=  ':' + Qcache_hits
    mysql_rrdupdate +=  ':' + Queries
    mysql_rrdupdate +=  ':' + Questions
    mysql_rrdupdate +=  ':' + Slave_connections
    mysql_rrdupdate +=  ':' + Slaves_connected
    mysql_rrdupdate +=  ':' + Slow_queries
    mysql_rrdupdate +=  ':' + Threads_connected
    mysql_rrdupdate +=  ':' + Threads_running
    mysql_rrdupdate +=  ':' + Uptime

    mysql_data = '     {"rrd":"%s","val":"%s"}' % ('mysql', mysql_rrdupdate)

    #collect sbm....
    slaveHost = False
    if 'Slave_SQL_State' in show_slave_status:
        slaveHost = True
    if 'Slave_IO_State' in show_slave_status:
        slaveHost = True

    #print('slaveHost ' + str(slaveHost))
    if slaveHost:
        Seconds_Behind_Master = Last_IO_Errno = Last_IO_Error = Last_SQL_Errno = Last_SQL_Error = Slave_IO_Running = Slave_SQL_Running = str('Empty')

        if str(show_slave_status['Seconds_Behind_Master']):
            Seconds_Behind_Master = str(show_slave_status['Seconds_Behind_Master'])

        if str(show_slave_status['Last_IO_Errno']):
            Last_IO_Errno = str(show_slave_status['Last_IO_Errno'])

        if str(show_slave_status['Last_IO_Error']):
            Last_IO_Error = str(show_slave_status['Last_IO_Error'])

        if str(show_slave_status['Last_SQL_Errno']):
            Last_SQL_Errno = str(show_slave_status['Last_SQL_Errno'])

        if str(show_slave_status['Last_SQL_Error']):
            Last_SQL_Error = str(show_slave_status['Last_SQL_Error'])

        if str(show_slave_status['Slave_IO_Running']):
            Slave_IO_Running = str(show_slave_status['Slave_IO_Running'])

        if str(show_slave_status['Slave_SQL_Running']):
            Slave_SQL_Running = str(show_slave_status['Slave_SQL_Running'])

        #Seconds_Behind_Master = 'NULL'
        if Seconds_Behind_Master == 'NULL' or Seconds_Behind_Master == 'None':
            if Slave_IO_Running == 'Preparing':
                sbm_data = ''
            else:
                alert_data = { 'Seconds_Behind_Master': str('NULL'),
                               'Last_SQL_Error': str(Last_SQL_Error),
                               'Last_SQL_Errno': str(Last_SQL_Errno),
                               'Last_IO_Error': str(Last_IO_Error),
                               'Last_IO_Errno': str(Last_IO_Errno),
                               'Slave_IO_Running': str(Slave_IO_Running),
                               'Slave_SQL_Running': str(Slave_SQL_Running),
                             }
                #print(alert_data)
        else:
            sbm_data = '{"rrd":"sbm","val":"N:%s"}' % (Seconds_Behind_Master)

    return (mysql_data, sbm_data, alert_data)

def get_ntpq():
    ntpq_data = {}

    collect="/usr/bin/ntpq -pn"
    p = subprocess.Popen(collect, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, err = p.communicate()

    exit_code = p.wait()
    if (exit_code != 0):
        print('Error: ' + str(err) + ' ' + str(output))
        return False

    #print(err)
    if 'Connection refused' in err:
        #print('ntpd not running')
        #return 'ntpd not running'
        return None

    multilines = output.splitlines()

    odict = {}
    count = 0
    for line in multilines:
            count += 1
            #line = line.split()
            #print(len(line))
            #print(line)
            #if len(line) > 1:
            #    print(line)

    ntpq_data = {'rrd': 'ntp', 'val': 'N:' + str(count)}
    return ntpq_data


def get_chronyc():
    chronyc_data = {}
    chronyc_alert = {}

    collect="/usr/bin/chronyc -n tracking"
    p = subprocess.Popen(collect, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, err = p.communicate()

    exit_code = p.wait()
    if (exit_code != 0):
        #print('Error: ' + str(err) + ' ' + str(output))
        chronyc_alert = {'chrony': str(err) + ' ' + str(output)}
        return chronyc_data, chronyc_alert

    multilines = output.splitlines()

    odict = {}
    count = 0
    for line in multilines:
            count += 1
            #line = line.split()
            #print(len(line))
            #print(line)
            #if len(line) > 1:
            #    print(line)

    chronyc_data = {'rrd': 'chrony', 'val': 'N:' + str(count)}
    return chronyc_data, chronyc_alert



###############################################################################
#hypervisor

class ListDomainsClass(object):
    def __init__(self, uri, host):
        self.uri = uri
        self.host = host

    def get(self):
        returnDict = {}
        uri_handle = str(self.uri) + str(self.host) + '/system'
        try:
            self.conn = libvirt.openReadOnly(uri_handle)
        except libvirt.libvirtError as e:
            return {"Error":str(e)}

        domains = self.conn.listAllDomains(0)
        if len(domains) != 0:
            for domain in domains:
                state = self.domstate(domain.name())
                returnDict[domain.name()] = str(state).lower()

        return returnDict

    def domstate(self,domName=None):
        dom = self.conn.lookupByName(domName)
        if dom == None:
            return str('NOTFOUND').lower()

        state, reason = dom.state()
        if state == libvirt.VIR_DOMAIN_NOSTATE:
            state='NOSTATE'
        elif state == libvirt.VIR_DOMAIN_RUNNING:
            state='RUNNING'
        elif state == libvirt.VIR_DOMAIN_BLOCKED:
            state='BLOCKED'
        elif state == libvirt.VIR_DOMAIN_PAUSED:
            state='PAUSED'
        elif state == libvirt.VIR_DOMAIN_SHUTDOWN:
            state='SHUTDOWN'
        elif state == libvirt.VIR_DOMAIN_SHUTOFF:
            state='SHUTOFF'
        elif state == libvirt.VIR_DOMAIN_CRASHED:
            state='CRASHED'
        elif state == libvirt.VIR_DOMAIN_PMSUSPENDED:
            state='PMSUSPENDED'
        else:
            state='UNKNOWN'

        return str(state).lower()

class ListDomainsDetailedClass(ListDomainsClass):
    def get(self):
        runningDict = {}
        uri_handle = str(self.uri) + str(self.host) + '/system'
        #print('uri_handle ' + uri_handle)
        try:
            self.conn = libvirt.openReadOnly(uri_handle)
        except libvirt.libvirtError as e:
            return {"Error":str(e)}

        hvm_type = str(self.conn.getType())
        hypervisor_type = hvm_type.lower()

        nodeinfo = self.conn.getInfo()
        hvm_model = str(nodeinfo[0])
        hvm_mem = str(nodeinfo[1])
        hvm_cpu = str(nodeinfo[2])
        stats = self.conn.getCPUStats(libvirt.VIR_NODE_CPU_STATS_ALL_CPUS)

        hypervisor_cpu = {
          'count': str(hvm_cpu),
          'type': str(hvm_model),
          'kernel': str(stats['kernel']),
          'idle': str(stats['idle']),
          'user': str(stats['user']),
          'iowait': str(stats['iowait'])
        }

#  "hypervisor": {
#    "cpu": {
#      "count": "24", 
#      "idle": "50414176940000000", 
#      "iowait": "558116710000000", 
#      "kernel": "794222650000000", 
#      "type": "x86_64", 
#      "user": "4615971910000000"
#    }, 

        hypervisor_cpu_rrd_val = 'N:' + str(hypervisor_cpu['count'])
        hypervisor_cpu_rrd_val += ':' + str(hypervisor_cpu['idle'])
        hypervisor_cpu_rrd_val += ':' + str(hypervisor_cpu['iowait'])
        hypervisor_cpu_rrd_val += ':' + str(hypervisor_cpu['kernel'])
        hypervisor_cpu_rrd_val += ':' + str(hypervisor_cpu['user'])
        hypervisor_cpu_rrd = {'rrd':'hypervisor.cpu', 'val': str(hypervisor_cpu_rrd_val)}

        memfree = self.conn.getFreeMemory()
        memfreeMB = memfree / 1024 / 1024
        memusedMB = int(hvm_mem) - int(memfreeMB)

        hypervisor_mem = {
          'total': str(hvm_mem),
          'used': str(memusedMB),
          'free': str(memfreeMB)
        }

#    "mem": {
#      "free": "195", 
#      "total": "32116", 
#      "used": "31921"
#    }, 

        hypervisor_mem_rrd_val = 'N:' + str(hypervisor_mem['free'])
        hypervisor_mem_rrd_val += ':' + str(hypervisor_mem['total'])
        hypervisor_mem_rrd_val += ':' + str(hypervisor_mem['used'])
        hypervisor_mem_rrd = {'rrd':'hypervisor.mem', 'val': str(hypervisor_mem_rrd_val)}


        hypervisor = {
          'type': hypervisor_type,
          'cpu': hypervisor_cpu,
          'mem': hypervisor_mem
        }

        runningDict['hypervisor'] = hypervisor

#####################################################################################################
        def domStatus(domName=None):
            runningStatus = {}

            dom = self.conn.lookupByName(domName)
            if dom == None:
                print json.dumps({"Error":"Failed to find domain " + str(domName)}, indent=2)
                return False

            state = self.domstate(domName)

            state_lower_case = str(state).lower()
            runningStatus['state'] = state_lower_case

            active = dom.isActive()
            if active == True:
                ok=1
            else:
                return {'state': state}

            cpus = dom.maxVcpus() #dom cpu count
            if cpus != -1:
                pass
            else:
                print json.dumps({"Error":"major error getting dom.Vcpus()"}, indent=2)
                return False

            cpu_stats = dom.getCPUStats(True)
            cpu_time = str(cpu_stats[0]['cpu_time'])
            system_time = str(cpu_stats[0]['system_time'])
            user_time = str(cpu_stats[0]['user_time'])

            dom_cpu = {
              'count': str(cpus),
              'cpu_time': cpu_time,
              'system_time': system_time,
              'user_time': user_time
            }

            runningStatus['cpu'] = dom_cpu

            mem = dom.maxMemory()
            if mem > 0:
                pass
            else:
                print json.dumps({"Error":"major error getting dom.maxMemory()"}, indent=2)
                return False

            dom_mem = {}
            mem_stats  = dom.memoryStats()

            for name in mem_stats:
                if name:
                    dom_mem[name] = str(mem_stats[name])

            runningStatus['mem'] = dom_mem

            from xml.dom import minidom
            raw_xml = dom.XMLDesc(0)
            #print(str(raw_xml))
#  <devices>
#    <emulator>/usr/bin/kvm</emulator>
#    <disk type='file' device='disk'>
#      <driver name='qemu' type='raw'/>
#      <source file='/ssd/data/appserv-sturm/hda.raw'/>
#      <backingStore/>
#      <target dev='hda' bus='virtio'/>
#      <alias name='virtio-disk0'/>
#      <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
#    </disk>

            xml = minidom.parseString(raw_xml)

            diskTypes = xml.getElementsByTagName('disk')
            diskDict = {}
            source = ''

            for diskType in diskTypes:
                diskNodes = diskType.childNodes
                for diskNode in diskNodes:
                    if diskNode.nodeName[0:1] != '#':
                        if diskNode.nodeName == 'source':
                            for attr in diskNode.attributes.keys():
                                #print('NAME ' + str(diskNode.attributes[attr].name))
                                #print('VALUE ' + str(diskNode.attributes[attr].value))
                                if diskNode.attributes[attr].name == 'dev':
                                    source = str(diskNode.attributes[attr].value)
                                elif diskNode.attributes[attr].name == 'file':
                                    source = str(diskNode.attributes[attr].value)
                                else:
                                    source = 'Unknown'
                        if diskNode.nodeName == 'target':
                            for attr in diskNode.attributes.keys():
                                if diskNode.attributes[attr].name == 'dev':
                                    target = str(diskNode.attributes[attr].value)
                                    rd_req, rd_bytes, wr_req, wr_bytes, err = dom.blockStats(source)

                                    diskDict[target] = {
                                      'device': str(source),
                                      'read_requests_issued': str(rd_req),
                                      'bytes_read': str(rd_bytes),
                                      'write_requests_issued': str(wr_req),
                                      'bytes_written': str(wr_bytes),
                                      'number_of_errors': str(err)
                                    }
            runningStatus['disk'] = diskDict

            netDict = {}
            interfaceTypes = xml.getElementsByTagName('interface')
            count = 0
            for interfaceType in interfaceTypes:
                netname = 'eth' + str(count)
                count = count + 1
                ifaceDict = {}
                interfaceNodes = interfaceType.childNodes
                for interfaceNode in interfaceNodes:
                    if interfaceNode.nodeName[0:1] != '#':
                        for attr in interfaceNode.attributes.keys():
                            if interfaceNode.attributes[attr].name == 'address':
                                mac = str(interfaceNode.attributes[attr].value)
                                ifaceDict['mac'] = mac

                            if interfaceNode.attributes[attr].name == 'bridge':
                                bridge = str(interfaceNode.attributes[attr].value)
                                ifaceDict['bridge'] = bridge

                            if interfaceNode.attributes[attr].name == 'dev':
                                iface = str(interfaceNode.attributes[attr].value)

                                stats = dom.interfaceStats(iface)

                                ifaceDict['read_bytes'] = str(stats[0])
                                ifaceDict['read_packets'] = str(stats[1])
                                ifaceDict['read_errors'] = str(stats[2])
                                ifaceDict['read_drops'] = str(stats[3])
                                ifaceDict['write_bytes'] = str(stats[4])
                                ifaceDict['write_packets'] = str(stats[5])
                                ifaceDict['write_errors'] = str(stats[6])
                                ifaceDict['write_drops'] = str(stats[7])
                    netDict[netname] = ifaceDict
            runningStatus['net'] = netDict

            return runningStatus
#####################################################################################################

        rrdList = []
        domDict = {}
        domains = self.conn.listAllDomains(0)
        if len(domains) != 0:
            for domain in domains:
                status = domStatus(domain.name())
                domDict[domain.name()] = status

                if status['state'] == 'running':
                    mem = status.get('mem', None)
                    if mem:
                        #mem_actual = status['mem']['XXactual']
                        actual = status.get('mem').get('actual', 0)
                        available = status.get('mem').get('available', 0)
                        major_fault = status.get('mem').get('major_fault', 0)
                        minor_fault = status.get('mem').get('minor_fault', 0)
                        rss = status.get('mem').get('rss', 0)
                        swap_in = status.get('mem').get('swap_in', 0)
                        swap_out = status.get('mem').get('swap_out', 0)
                        unused = status.get('mem').get('unused', 0)

                        rrd_val = 'N:' + str(actual)
                        rrd_val += ':' + str(available)
                        rrd_val += ':' + str(major_fault)
                        rrd_val += ':' + str(minor_fault)
                        rrd_val += ':' + str(rss)
                        rrd_val += ':' + str(swap_in)
                        rrd_val += ':' + str(swap_out)
                        rrd_val += ':' + str(unused)
                        rrd = {'rrd': str(domain.name()) + '.mem', 'val': rrd_val}
                        rrdList.append(rrd)

#      "mem": {
#        "actual": "2097152", 
#        "available": "2044968", 
#        "major_fault": "0", 
#        "minor_fault": "0", 
#        "rss": "871248", 
#        "swap_in": "0", 
#        "swap_out": "0", 
#        "unused": "1930192"
#      }, 

#      "mem": {
#        "actual": "10485760", 
#        "rss": "10304984"
#      }, 

                    cpu = status.get('cpu', None)
                    if cpu:
                        count = status.get('cpu').get('count', 0)
                        cpu_time = status.get('cpu').get('cpu_time', 0)
                        system_time = status.get('cpu').get('system_time', 0)
                        user_time = status.get('cpu').get('suser_time', 0)

                        rrd_val = 'N:' + str(count)
                        rrd_val += ':' + str(cpu_time)
                        rrd_val += ':' + str(system_time)
                        rrd_val += ':' + str(user_time)
                        rrd = {'rrd': str(domain.name()) + '.cpu', 'val': rrd_val}
                        rrdList.append(rrd)

#      "cpu": {
#        "count": "1", 
#        "cpu_time": "3128286556798", 
#        "system_time": "736360000000", 
#        "user_time": "36310000000"
#      }, 


                    net = status.get('net', None)
                    if net:
                        for item in net:
                            #print(item) #eth0
                            read_bytes = status.get('net').get(item).get('read_bytes', 0)
                            read_drops = status.get('net').get(item).get('read_drops', 0)
                            read_errors = status.get('net').get(item).get('read_errors', 0)
                            read_packets = status.get('net').get(item).get('read_packets', 0)
                            write_bytes = status.get('net').get(item).get('write_bytes', 0)
                            write_drops = status.get('net').get(item).get('write_drops', 0)
                            write_errors = status.get('net').get(item).get('write_errors', 0)
                            write_packets = status.get('net').get(item).get('write_packets', 0)

                            rrd_val = 'N:' + str(read_bytes)
                            rrd_val += ':' + str(read_drops)
                            rrd_val += ':' + str(read_errors)
                            rrd_val += ':' + str(read_packets)
                            rrd_val += ':' + str(write_bytes)
                            rrd_val += ':' + str(write_drops)
                            rrd_val += ':' + str(write_errors)
                            rrd_val += ':' + str(write_packets)

                            rrd = {'rrd': str(domain.name()) + '.' + str(item), 'val': rrd_val}
                            rrdList.append(rrd)

#      "net": {
#        "eth0": {
#          "bridge": "br0", 
#          "mac": "52:54:00:a2:14:5b", 
#          "read_bytes": "74962610801", 
#          "read_drops": "0", 
#          "read_errors": "0", 
#          "read_packets": "46391059", 
#          "write_bytes": "51867066125", 
#          "write_drops": "0", 
#          "write_errors": "0", 
#          "write_packets": "38797256"
#        }
#      }, 

                      
                    disk = status.get('disk', None)
                    if disk:
                        for item in disk:
                            #print(item) #hda
                            bytes_read = status.get('disk').get(item).get('bytes_read', 0)
                            bytes_written = status.get('disk').get(item).get('bytes_written', 0)
                            read_requests_issued = status.get('disk').get(item).get('read_requests_issued', 0)
                            write_requests_issued = status.get('disk').get(item).get('write_requests_issued', 0)

                            rrd_val = 'N:' + str(bytes_read)
                            rrd_val += ':' + str(bytes_written)
                            rrd_val += ':' + str(read_requests_issued)
                            rrd_val += ':' + str(write_requests_issued)
                            
                            rrd = {'rrd': str(domain.name()) + '.' + str(item), 'val': rrd_val}
                            rrdList.append(rrd)

#      "disk": {
#        "hda": {
#          "bytes_read": "2884285952", 
#          "bytes_written": "14652522496", 
#          "device": "/data/prod-proxy/hda.qcow2", 
#          "number_of_errors": "-1", 
#          "read_requests_issued": "91544", 
#          "write_requests_issued": "498427"
#        }
#      }, 
      
        runningDict['domains'] = domDict

        rrdList.append(hypervisor_cpu_rrd)
        rrdList.append(hypervisor_mem_rrd)
        runningDict['rrdata'] =  rrdList 

        self.conn.close()
        return runningDict

#hypervisor
###############################################################################

if __name__ == '__main__':
    post_request = True
    if sys.argv[1:]:
        if sys.argv[1] == "--daemon":
            daemonize()
            sys.exit(0)
        if sys.argv[1] == "--disable-post":
            post_request = False

    if not system_id:
        system_id = get_system_id()

    if os.path.isfile('/usr/bin/virsh'):
        #apt-get install -y python-libvirt
        import libvirt

    json_data = collector(system_id)
    print(json.dumps(json_data, sort_keys=True, indent=4))
    if post_request:
        response = post(system_id, json.dumps(json_data))
        try:
            print(json.dumps(json.loads(response)))
        except Exception as e:
            print(response)
    else:
        print("POST DISABLED")



