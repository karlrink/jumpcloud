#!/usr/bin/env python2

__version__ = "001"

import BaseHTTPServer
import cgi
import os
import sys
import glob
import time
import subprocess
import re

import multiprocessing
import itertools

import threading

saveq = multiprocessing.Queue()

import config

debug = False

class httpServHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_GET(self):
    if self.path.find('?') != -1:
      self.path, self.query_string = self.path.split('?', 1)
    else:
      self.query_string = 'Empty'

    #self.send_response(200)
    #self.send_header('Content-type','text/html')
    #self.send_header('Content-type','image/png')
    #self.end_headers()

    self.globals = dict(cgi.parse_qsl(self.query_string))

    #host = self.globals['host']
    #host  =  self.globals.get('host', 'Empty')
    system_id  =  self.globals.get('system_id', 'Empty')
    back  =  self.globals.get('back', 'Empty')
    scale =  self.globals.get('scale', 'Empty')
    rrd   =   self.globals.get('rrd', 'Empty')
    ds   =   self.globals.get('ds', 'Empty')
    start = self.globals.get('start', 'Empty')
    end =   self.globals.get('end', 'Empty')
    display = self.globals.get('display', 'Empty')

    #if debug: print 'host: ' + host
    if debug: print 'system_id: ' + system_id
    if debug: print 'back: ' + back
    if debug: print 'scale: ' + scale
    if debug: print 'rrd: ' + rrd
    if debug: print 'ds: ' + ds
    if debug: print 'start: ' + start
    if debug: print 'end: ' + end
    if debug: print 'display: ' + display

    #rrdpath = '/data/rrd/' + host + '/'
    rrdpath = config.plot['datadir'] + '/' + str(system_id) + '/'
    print(rrdpath)
    if not os.path.exists(rrdpath):
        self.wfile.write("Error: no os.path.exists " + rrdpath)
        return False
        sys.exit(1)

    rrdlist = []
    if rrd != 'Empty':
        if debug: print 'just this rrd: ' + rrd
        # verify rrdfile exists...
        rrdfile = rrdpath + rrd + '.rrd'
        if debug: print 'this rrdfile is: ' + rrdfile
        if not os.path.isfile(rrdfile):
            self.wfile.write("Error: no os.path.isfile " + rrdfile)
            return False
        rrdlist.append(rrdfile)
    else:
        #rrdlist = ['/data/rrd/db-ca4-01/mysql_check_ca4.rrd']
        for rrdfile in glob.glob(rrdpath + '*.rrd'):
            #print rrdfile
            rrdlist.append(rrdfile)
    if debug: print str(rrdlist)

    #outdir = '/app/plot/display/'
    outdir = config.plot['workdir'] + '/display/'
    if not os.path.isdir(outdir):
        print('NO OUTPUT DIR: ' + str(outdir))
        return False
    #finaldir = outdir + host
    finaldir = outdir + system_id
    if debug: print finaldir
    if not os.path.exists(finaldir):
      os.makedirs(finaldir)

    #print 'DIE DIE DIE'
    #return False

    epochnow = int(time.time())

    if back != 'Empty':
        val = int(back)
    else:
        val = 7

    if scale != 'Empty':
        if scale == 'year':
            seconds = 60 * 60 * 24 * 365
        elif scale == 'month':
            seconds = 60 * 60 * 24 * 30
        elif scale == 'day':
            seconds = 60 * 60 * 24
        elif scale == 'hour':
            seconds = 60 * 60
        elif scale == 'minute':
            seconds = 60
        else:
            self.wfile.write("Error: invalid scale " + scale)
            return False
    else:
        scale = 'day'
        seconds = 60 * 60 * 24


    if start != 'Empty':
        back = scale = 'Empty'
        #start = yyyy-mm-ddTHH:MM:ss # '2016-01-01T16:45:00'
        start, error = validateDate(start)
        if error:
            self.wfile.write(error)
            return False
    else:
        #secondsback = 60 * 60 * 24 * 7
        secondsback = seconds * val
        start = epochnow - secondsback

    if end != 'Empty':
        end, error = validateDate(end)
        if error:
            self.wfile.write(error)
            return False
    else:
        end = epochnow

    if debug: print 'start ' + str(start)
    if debug: print 'end ' + str(end)

    #print 'DIE DIE DIE'
    #return False

    # gen graphs...
    processes = []
    count = 0
    for rrd in rrdlist:
        filename = os.path.basename(rrd)
        basename = os.path.splitext(filename)[0]
        if debug: print 'infile: ' + rrd

        if ds != 'Empty':
            if debug: print 'ds present as ' + str(type(ds)) + ' ' + str(ds)
            dsdict = {ds:ds}
        else:
            dsdict = getDDSdict(filename)


        if debug: print 'dsdict is what? ' + str(dsdict)
        if dsdict is None:
            dsdict = getRRDinfo(rrdpath + filename)

        if dsdict is None:
            if debug: print 'unknown is here, give me a break'
            break
#m1.defunct
        #p = multiprocessing.Process(target=genGraph, args=(rrd,dsdict,start,end,outdir,host,saveq))
        p = threading.Thread(target=genGraph, args=(rrd,dsdict,start,end,outdir,system_id,saveq))
        p.start()
        count += 1
        processes.append(count)
        if debug: print 'Launched process ' + str(count)

    for i in processes:
        p.join()

    graphs2d = [saveq.get() for p in processes]
    graphs = list(itertools.chain(*graphs2d))
    #print(graphs)

    # rrd=mpstat ds=idle
    #if ds != 'Empty':
    #    if debug: print 'this ds: ' + ds
    #    # verify ds exists...
    #    graphs = list('')
    #    print 'this is the last place on earth...'

    self.send_response(200)

    if display == 'img':
        self.send_header('Content-type','image/png')
    else:
        self.send_header('Content-type','text/html')

    self.end_headers()

    for graph in graphs:
        try:
            if display == 'img':
                self.wfile.write(file(graph,"rb").read())
            else:
                data_uri = open(graph, 'rb').read().encode('base64').replace('\n', '')
                img_tag = '<img src="data:image/png;base64,{0}" alt="">'.format(data_uri)
                self.wfile.write(img_tag)
        except IOError as err:
            self.wfile.write(str(err))

    return True

import distutils.spawn
def is_tool(name):
  return distutils.spawn.find_executable(name) is not None

def validateDate(date=None):
        start = error = None
        #start = yyyy-mm-ddTHH:MM:ss # '2016-01-01T16:45:00'
        dpattern = 'yyyy-mm-ddTHH:MM:ss for example, try something like: 2016-01-01T16:45:00 \n'
        if debug: print 'start time: ' + date
        idate = itime = '0'
        try:
            idate, itime = date.split('T', 1)
        except ValueError, UnboundLocalError:
            #self.wfile.write("Error: invalid date format " + date + '\n' + dpattern)
            #return False
            error = 'Error: invalid date format ' + date + '\n' + dpattern
            return start, error

        if debug: print 'idate ' + str(idate)
        if debug: print 'itime ' + str(itime)
        try:
            itime = time.mktime(time.strptime(idate + 'T' + itime, "%Y-%m-%dT%H:%M:%S"))
        except ValueError:
            #self.wfile.write("Error: invalid date format " + idate + ' ' + itime + '\n' + dpattern)
            #return False
            error = 'Error: invalid date format ' + idate + ' ' + itime + '\n' + dpattern
            return start, error

        #epoch = int(itime)
        start = int(itime)
        return start, error

def getDDSdict(filename=None):
    if filename == 'sbm.rrd':
        if debug: print 'yes, file is sbm.rrd'
        dsdict = dds_sbm
    elif filename == 'ping4.rrd':
        if debug: print 'yes, file is ping4.rrd'
        dsdict = dds_ping4
    elif filename == '_HOST_.rrd':
        if debug: print 'yes, file is _HOST_.rrd'
        dsdict = dds_mysql_check
    elif filename == 'mysql_check_ca4.rrd':
        if debug: print 'yes, file is mysql_check_ca4.rrd'
        dsdict = dds_mysql_check
    elif filename == 'mysql_check.rrd':
        if debug: print 'yes, file is mysql_check.rrd'
        dsdict = dds_mysql_check
    else:
        if debug: print 'unknown'
        dsdict = None

    return dsdict


def getRRDinfo(infile=None):
    if debug: print 'Lets figure this out... ' + infile
    cmdline  = 'rrdtool info ' + infile

    rrdtool_command = is_tool('rrdtool')
    if not rrdtool_command:
        print('NO RRDTOOL COMMAND')
        return False


    cmdprocess = subprocess.Popen(cmdline.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = cmdprocess.communicate()

    exit_code = cmdprocess.wait()
    if (exit_code != 0):
        print 'Error: not working properly: ' + cmdline
        return False

    #print 'output ' + str(output)
    mlines = output.splitlines()

    dslist = []
    pattern = re.compile('^ds\[')
    for item in mlines:
        #print 'mlines ' + item
        if pattern.match(item):
            itemtrim = item.split(".")[0]
            itemtrim = re.sub('^ds','', itemtrim)
            itemtrim = re.sub('^\[','', itemtrim)
            itemtrim = re.sub('\]$','', itemtrim)
            dslist.append(itemtrim)

    #if debug: print 'dslist... ' + str(dslist)
    uniques = set(dslist)
    ulist = list(uniques)
    if debug: print 'ulist... ' + str(ulist)

    #dsdict is what? {'1': 'rta', '2': 'pl'}

    dsdict = {}

    for item in ulist:
        dsdict[item] = item

    return dsdict


dds_mysql_check = {
 '1':'Connections',
 '2':'Open_files',
 '3':'Open_tables',
 '4':'Qcache_free_memory',
 '5':'Qcache_hits',
 '6':'Qcache_inserts',
 '7':'Qcache_lowmem_prunes',
 '8':'Qcache_not_cached',
 '9':'Qcache_queries_in_cache',
'10':'Queries',
'11':'Questions',
'12':'Table_locks_waited',
'13':'Threads_connected',
'14':'Threads_running',
'15':'Uptime',
}

dds_sbm = {
  'sbm':'Seconds_Behind_Master',
}

dds_ping4 = {
  '1':'rta',
  '2':'pl',
}


def getDSinfo(infile=None):
    print 'getDSinfo'

#def genGraph(rrd=None,dsdict=None,start=None,end=None,outdir=None,host=None):
def genGraph(rrd=None,dsdict=None,start=None,end=None,outdir=None,system_id=None,saveq=None):

    if debug: print 'rrd is ' + rrd
    db = rrd

    filename = os.path.basename(rrd)
    pathname = os.path.dirname(rrd)
    basename = os.path.splitext(filename)[0]

    if debug: print 'filename is ' + filename
    if debug: print 'pathname is ' + pathname
    if debug: print 'basename is ' + basename

    if dsdict is None:
        print 'No Can Do: NoneType: ' + rrd
        return False

    #if dsdict is bool:
    #    print 'No Can Do: boolType: '
    #    return False

    psize = len(dsdict)
    #print 'psize ' + str(psize)
    #print str(dsdict)

    #pool = multiprocessing.Pool(psize)

    #print 'DIE DIE DIE'
    #return True
    #sys.exit(1)

    outfiles = []
    processes = []
    count = 0
    for key, value in dsdict.iteritems():
        ds = key
        #title = value
        #title = host + ' ' + basename + ' ' + value
        title = system_id + ' ' + basename + ' ' + value

        #outfile = outdir + host + '/' + basename + '.' + ds + '.png'
        outfile = outdir + system_id + '/' + basename + '.' + ds + '.png'
        if debug:
            cmdline  = 'rrdtool graphv ' + outfile + ' -a PNG '
        else:
            cmdline  = 'rrdtool graph ' + outfile + ' -a PNG '

        cmdline += ' --title="%s" ' % title
        cmdline += ' --start %s --end %s ' % (start,end)
        cmdline += ' DEF:%s=%s:%s:AVERAGE ' % (ds,db,ds)
        cmdline += ' LINE2:%s#FF0000 ' % (ds)

        if debug:
            cmdline = cmdline + ''
        else:
            cmdline = cmdline + ' >/dev/null 2>&1'

        if debug: print cmdline
#m2
        p = multiprocessing.Process(target=os.system(cmdline), args=())
        #p = threading.Thread(target=os.system(cmdline), args=())
        p.start()

        #pool.apply_async(os.system(cmdline), args=())
        #processes.append(pool)

        processes.append(p)

        outfiles.append(outfile)
        #outfiles.extend(outfile)
        count += 1
        if debug: print 'SubLaunched ' + str(count) + ' ' + outfile


    #for p in processes: p.close()
    for p in processes: p.join()
    saveq.put(outfiles)
    return outfiles


if __name__ == "__main__":
  #os.chdir('/app/plot')
  os.chdir(str(config.plot['workdir']))
  servAddr = ('',8001)
  serv = BaseHTTPServer.HTTPServer(servAddr, httpServHandler)
  print 'Startup ' + str(time.asctime())
  serv.serve_forever()



