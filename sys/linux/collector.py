#!/usr/bin/env python2

url = 'https://monitor.nationsinfocorp.com:443/collector'

__version__ = '005'

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
    
    #alert_data = { 'Error': 'yes', 'Help': 'Please'}

    json_data  = '{ "system_id": "' + str(system_id) + '",'
    json_data += '"meminfo": ' + str(json.dumps(proc_meminfo)) + ','
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
        sys.exit(1)

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

if __name__ == '__main__':
    post_request = True
    if sys.argv[1:]:
        if sys.argv[1] == "--daemon":
            daemonize()
            sys.exit(0)
        if sys.argv[1] == "--disable-post":
            post_request = False

    system_id = get_system_id()
    json_data = collector(system_id)
    print(json.dumps(json_data, sort_keys=True, indent=4))
    if post_request:
        response = post(system_id, json.dumps(json_data))
        try:
            print(json.loads(response))
        except Exception as e:
            print(response)
    else:
        print("POST DISABLED")


