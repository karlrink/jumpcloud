#!/usr/bin/env python2

import sys
import os

def collect_mysql():

    dbconf = '/etc/db.conf'
    mysqlSocket = '/var/run/mysqld/mysqld.sock'

    mysql_json_data = sbm_json_data = ''

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

    mysql_json_data = '     {"rrd":"%s","val":"%s"}' % ('mysql', mysql_rrdupdate)

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

        if Seconds_Behind_Master == 'NULL' or Seconds_Behind_Master == 'None':
            if Slave_IO_Running == 'Preparing':
                sbm_json_data = ''
            else:
                msg =  'Last_SQL_Error ' + str(Last_SQL_Error) + '\n'
                msg += 'Last_SQL_Errno ' + str(Last_SQL_Errno) + '\n'
                msg += 'Last_IO_Error ' + str(Last_IO_Error) + '\n'
                msg += 'Last_IO_Errno ' + str(Last_IO_Errno) + '\n'
                msg += 'Slave_IO_Running ' + str(Slave_IO_Running) + '\n'
                msg += 'Slave_SQL_Running ' + str(Slave_SQL_Running) + '\n'
                msg += ''
        else:
            sbm_json_data = '     {"rrd":"sbm","val":"N:%s"} \n' % (Seconds_Behind_Master)

    return (mysql_json_data, sbm_json_data)


def collector():
    try:
        mysql_json_data, sbm_json_data = collect_mysql()
    except TypeError:
        mysql_json_data = sbm_json_data = ''

    #json_data  = '{ \n'
    #json_data += ' "system_id":"%s", \n' % '123456' 
    #json_data += ' "rrdata": \n'
    #json_data += '     [ \n'

    print(mysql_json_data) 
    print(sbm_json_data) 

if __name__ == '__main__':
    collector()
    

#mysql> create user 'collector'@'localhost' IDENTIFIED WITH mysql_native_password BY 'XXXXXXXXXXXXXXXXXXX';
#mysql> GRANT SELECT, REPLICATION CLIENT ON *.* TO 'collector'@'localhost';

