
__version__ = '001'

from flask import Flask
from flask import request
from flask import jsonify
import logging
import json
import os

import rrdtool

import config

app = Flask(__name__)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)
#app.logger.setLevel(logging.DEBUG)
#app.logger.debug('this will show in the log')

datadir = '/data/rrd'
x_api_key_file = '/data/x-api-key.txt'

@app.route("/collector", methods=['POST']) #collector?system_id=5e30c0b9890a7a4766268b59
def collector():
    app.logger.debug('app.logger.debug')

    headers_api_key = request.headers.getlist("x-api-key", None)

    if not headers_api_key:
        app.logger.debug('no x-api-key')
        return jsonify('{x-api-key:None}'), 200, {'Content-Type': 'application/json; charset=utf-8'}

    api_key = ''.join(headers_api_key)
    found_api_key = False
    with open(x_api_key_file, 'r') as filehandle:
        filedata = filehandle.readlines()
        for line in filedata:
            if api_key in line:
                found_api_key = True

    if not found_api_key:
        return jsonify('{x-api-key:NotFound}'), 200, {'Content-Type': 'application/json; charset=utf-8'}

    system_id = request.args.get("system_id", None)
    if not system_id:
        return jsonify('{system_id:None}'), 200, {'Content-Type': 'application/json; charset=utf-8'}

    if request.method == 'POST':
        return post_request(system_id)
    else:
        return ''

def post_request(system_id):

    jdata = request.get_json()

    rrdList = jdata['rrdata']
    #print(type(rrdList))
    #for rr in rrdList:
    #    print(rr)
    #    print(type(rr))

    if len(rrdList) == 0:
        return jsonify('{rrd:False}'), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        for rr in rrdList:
            #rrd = rr['rrd']
            #val = rr['val']
            #rrdfile =  datadir + '/' + system_id + '/' + rrd + '.rrd'
            #print(rr)
            #print(type(rr))
            if type(rr) is dict:
                #print(rr['rrd'])
                rrd = rr['rrd']
                val = rr['val']
                path = datadir + '/' + system_id
                if not os.path.isdir(path):
                    os.mkdir(path)

                rrdfile =  path + '/' + rrd + '.rrd'

                if rrd == 'mem' and not os.path.isfile(rrdfile):
                    memRRD(rrdfile)
                    continue

                if rrd == 'swap' and not os.path.isfile(rrdfile):
                    swapRRD(rrdfile)
                    continue

                if rrd == 'uptime' and not os.path.isfile(rrdfile):
                    uptimeRRD(rrdfile)
                    continue

                if rrd == 'root' and not os.path.isfile(rrdfile):
                    rootRRD(rrdfile)
                    continue

                if rrd == 'ps' and not os.path.isfile(rrdfile):
                    psRRD(rrdfile)
                    continue

                if rrd == 'mpstat' and not os.path.isfile(rrdfile):
                    mpstatRRD(rrdfile)
                    continue

                if rrd == 'iostat' and not os.path.isfile(rrdfile):
                    iostatRRD(rrdfile)
                    continue


                if os.path.isfile(rrdfile):
                    rrdtool.update(str(rrdfile), str(val))
                else:
                    app.logger.debug('missing ' + rrdfile)

                #try:
                #    rrdtool.update(str(rrdfile), str(val))
                #except rrdtool.error as e:
                #    print('rrdtool.error ' + str(e))

    system_id_file = datadir + '/' + str(system_id) + '/' + str(system_id) + '.json'
    with open(system_id_file, 'w+') as jsonfile:
        json.dump(jdata, jsonfile)

    return jsonify('{post:OK}'), 200, {'Content-Type': 'application/json; charset=utf-8'}


def send_ses_email(receivers, subject, message):
    import smtplib, ssl
    sender_email = config.ses['smtp_from']
    smtp_server  = config.ses['smtp_host']
    port         = config.ses['smtp_port']
    smtp_user    = config.ses['smtp_user']
    smtp_pass    = config.ses['smtp_pass']

    header =  ("From: %s\r\nTo: %s\r\n"
            % (sender_email, ",".join(receivers)))
    header += ("Subject: %s\r\n\r\n" % (subject))
    msg = header + message

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(smtp_user, smtp_pass)
        server.sendmail(sender_email, receivers, msg)
    print('emailto: ' + str(receivers))


def memRRD(rrdfile=None):
# free -m
#             total       used       free     shared    buffers     cached
#Mem:          3819       3553        266          0        251       2977
    #print "running rrdtool create"
    #cmdline = 'rrdtool create ' + rrdfile
    #cmdline += ' --start 0 --step 300 '
    #cmdline += ' DS:total:GAUGE:600:U:U '
    #cmdline += ' DS:used:GAUGE:600:U:U '
    #cmdline += ' DS:free:GAUGE:600:U:U '
    #cmdline += ' DS:shared:GAUGE:600:U:U '
    #cmdline += ' DS:buffers:GAUGE:600:U:U '
    #cmdline += ' DS:cached:GAUGE:600:U:U '
    #cmdline += ' RRA:AVERAGE:0.5:1:360 '
    #cmdline += ' RRA:AVERAGE:0.5:12:1008 '
    #cmdline += ' RRA:AVERAGE:0.5:288:2016 '
    #print("cmdline: " + cmdline)
    #os.system(cmdline)

    #print(rrdfile)

    data_sources=[ 'DS:total:GAUGE:600:U:U',
                   'DS:used:GAUGE:600:U:U',
                   'DS:free:GAUGE:600:U:U',
                   'DS:shared:GAUGE:600:U:U',
                   'DS:buffers:GAUGE:600:U:U',
                   'DS:cached:GAUGE:600:U:U' ]

    rrdtool.create( rrdfile, '--start', '0',
                             '--step', '300',
                    data_sources,
                    'RRA:AVERAGE:0.5:1:360',
                    'RRA:AVERAGE:0.5:12:1008',
                    'RRA:AVERAGE:0.5:288:2016' )
    #https://oss.oetiker.ch/rrdtool/prog/rrdpython.en.html
    return True

def swapRRD(rrdfile=None):
# free -m
#             total       used       free
#Swap:         5999          0       5999
    #print "running rrdtool create"
    #cmdline = 'rrdtool create ' + rrdfile
    #cmdline += ' --start 0 --step 300 '
    #cmdline += ' DS:total:GAUGE:600:U:U '
    #cmdline += ' DS:used:GAUGE:600:U:U '
    #cmdline += ' DS:free:GAUGE:600:U:U '
    #cmdline += ' RRA:AVERAGE:0.5:1:360 '
    #cmdline += ' RRA:AVERAGE:0.5:12:1008 '
    #cmdline += ' RRA:AVERAGE:0.5:288:2016 '
    #if debug: print "cmdline: " + cmdline
    #os.system(cmdline)

    data_sources=[ 'DS:total:GAUGE:600:U:U',
                   'DS:used:GAUGE:600:U:U',
                   'DS:free:GAUGE:600:U:U'
                 ]

    rrdtool.create( rrdfile, '--start', '0',
                             '--step', '300',
                    data_sources,
                    'RRA:AVERAGE:0.5:1:360',
                    'RRA:AVERAGE:0.5:12:1008',
                    'RRA:AVERAGE:0.5:288:2016' )
    return True

def uptimeRRD(rrdfile=None):
# uptime
#14:55  up 3 days,  3:20, 15 users, load averages: 1.67 1.58 1.63
#and remember no days...
#{ "rrd": "uptime", "val": "1469852403:1:5:0.82:0.77:0.74" }
    #cmdline = 'rrdtool create ' + rrdfile
    #cmdline += ' --start 0 --step 300 '
    #cmdline += ' DS:days:GAUGE:600:U:U '
    #cmdline += ' DS:users:GAUGE:600:U:U '
    #cmdline += ' DS:one:GAUGE:600:U:U '
    #cmdline += ' DS:five:GAUGE:600:U:U '
    #cmdline += ' DS:fifteen:GAUGE:600:U:U '
    #cmdline += ' RRA:AVERAGE:0.5:1:360 '
    #cmdline += ' RRA:AVERAGE:0.5:12:1008 '
    #cmdline += ' RRA:AVERAGE:0.5:288:2016 '
    #if debug: print "cmdline: " + cmdline
    #os.system(cmdline)

    data_sources=[ 'DS:days:GAUGE:600:U:U',
                   'DS:users:GAUGE:600:U:U',
                   'DS:one:GAUGE:600:U:U',
                   'DS:five:GAUGE:600:U:U',
                   'DS:fifteen:GAUGE:600:U:U'
                 ]

    rrdtool.create( rrdfile, '--start', '0',
                             '--step', '300',
                    data_sources,
                    'RRA:AVERAGE:0.5:1:360',
                    'RRA:AVERAGE:0.5:12:1008',
                    'RRA:AVERAGE:0.5:288:2016' )
    return True

def rootRRD(rrdfile=None):
#root_fs_size: 32125
#root_fs_used: 2566
#root_fs_avail: 27922
#root_fs_use: 9%
    #print "running rrdtool create"
    #cmdline = 'rrdtool create ' + rrdfile
    #cmdline += ' --start 0 --step 300 '
    #cmdline += ' DS:size:GAUGE:600:U:U '
    #cmdline += ' DS:used:GAUGE:600:U:U '
    #cmdline += ' DS:avail:GAUGE:600:U:U '
    #cmdline += ' DS:use:GAUGE:600:U:U '
    #cmdline += ' RRA:AVERAGE:0.5:1:360 '
    #cmdline += ' RRA:AVERAGE:0.5:12:1008 '
    #cmdline += ' RRA:AVERAGE:0.5:288:2016 '
    #if debug: print "cmdline: " + cmdline
    #os.system(cmdline)

    data_sources=[ 'DS:size:GAUGE:600:U:U',
                   'DS:used:GAUGE:600:U:U',
                   'DS:avail:GAUGE:600:U:U',
                   'DS:use:GAUGE:600:U:U'
                 ]

    rrdtool.create( rrdfile, '--start', '0',
                             '--step', '300',
                    data_sources,
                    'RRA:AVERAGE:0.5:1:360',
                    'RRA:AVERAGE:0.5:12:1008',
                    'RRA:AVERAGE:0.5:288:2016' )
    return True

def psRRD(rrdfile=None):
#ps_rrdupdate = str(epochtime) + ':' + number_of_procs
#ps_rrdupdate += ':' + number_of_defunct
    #cmdline = 'rrdtool create ' + rrdfile
    #cmdline += ' --start 0 --step 300 '
    #cmdline += ' DS:procs:GAUGE:600:U:U '
    #cmdline += ' DS:defunct:GAUGE:600:U:U '
    #cmdline += ' RRA:AVERAGE:0.5:1:360 '
    #cmdline += ' RRA:AVERAGE:0.5:12:1008 '
    #cmdline += ' RRA:AVERAGE:0.5:288:2016 '
    #if debug: print "cmdline: " + cmdline
    #os.system(cmdline)

    data_sources=[ 'DS:procs:GAUGE:600:U:U',
                   'DS:defunct:GAUGE:600:U:U'
                 ]

    rrdtool.create( rrdfile, '--start', '0',
                             '--step', '300',
                    data_sources,
                    'RRA:AVERAGE:0.5:1:360',
                    'RRA:AVERAGE:0.5:12:1008',
                    'RRA:AVERAGE:0.5:288:2016' )
    return True

def mpstatRRD(rrdfile=None):
# mpstat
# 03:27:26 PM  CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest   %idle
# 03:27:26 PM  all    1.48    0.00    0.59    0.25    0.00    0.02    0.00    0.00   97.66
    #print "running rrdtool create"
    #cmdline = 'rrdtool create ' + rrdfile
    #cmdline += ' --start 0 --step 300 '
    #cmdline += ' DS:usr:GAUGE:600:U:U '
    #cmdline += ' DS:nice:GAUGE:600:U:U '
    #cmdline += ' DS:sys:GAUGE:600:U:U '
    #cmdline += ' DS:iowait:GAUGE:600:U:U '
    #cmdline += ' DS:irq:GAUGE:600:U:U '
    #cmdline += ' DS:soft:GAUGE:600:U:U '
    #cmdline += ' DS:steal:GAUGE:600:U:U '
    #cmdline += ' DS:guest:GAUGE:600:U:U '
    #cmdline += ' DS:idle:GAUGE:600:U:U '
    #cmdline += ' RRA:AVERAGE:0.5:1:360 '
    #cmdline += ' RRA:AVERAGE:0.5:12:1008 '
    #cmdline += ' RRA:AVERAGE:0.5:288:2016 '
    #if debug: print "cmdline: " + cmdline
    #os.system(cmdline)

    data_sources=[ 'DS:usr:GAUGE:600:U:U',
                   'DS:nice:GAUGE:600:U:U',
                   'DS:sys:GAUGE:600:U:U',
                   'DS:iowait:GAUGE:600:U:U',
                   'DS:irq:GAUGE:600:U:U',
                   'DS:soft:GAUGE:600:U:U',
                   'DS:steal:GAUGE:600:U:U',
                   'DS:guest:GAUGE:600:U:U',
                   'DS:idle:GAUGE:600:U:U'
                 ]

    rrdtool.create( rrdfile, '--start', '0',
                             '--step', '300',
                    data_sources,
                    'RRA:AVERAGE:0.5:1:360',
                    'RRA:AVERAGE:0.5:12:1008',
                    'RRA:AVERAGE:0.5:288:2016' )
    return True

# the round robin archive
#'RRA:AVERAGE:0.5:1:360'    Archive point is saved every 5min, archive is kept for 1day 6hour back.
#'RRA:AVERAGE:0.5:12:1008'  Archive point is saved every 1hour, archive is kept for 1month 11day back.
#'RRA:AVERAGE:0.5:288:2016' Archive point is saved every 1day, archive is kept for 5year 6month 8day back.

#def diskRRD(rrdfile=None):
def iostatRRD(rrdfile=None):
#iostat
#['dm-4', '342.73', '1670.65', '2661.46', '24692779871', '39337324729']
#Device:            tps   Blk_read/s   Blk_wrtn/s   Blk_read   Blk_wrtn
    #cmdline = 'rrdtool create ' + rrdfile
    #cmdline += ' --start 0 --step 300 '
    #cmdline += ' DS:tps:GAUGE:600:U:U '
    #cmdline += ' DS:blk_reads:GAUGE:600:U:U '
    #cmdline += ' DS:blk_wrtns:GAUGE:600:U:U '
    #cmdline += ' DS:blk_read:GAUGE:600:U:U '
    #cmdline += ' DS:blk_wrtn:GAUGE:600:U:U '
    #cmdline += ' RRA:AVERAGE:0.5:1:360 '
    #cmdline += ' RRA:AVERAGE:0.5:12:1008 '
    #cmdline += ' RRA:AVERAGE:0.5:288:2016 '
    #if debug: print "cmdline: " + cmdline
    #os.system(cmdline)

    data_sources=[ 'DS:tps:GAUGE:600:U:U',
                   'DS:blk_reads:GAUGE:600:U:U',
                   'DS:blk_wrtns:GAUGE:600:U:U',
                   'DS:blk_read:GAUGE:600:U:U',
                   'DS:blk_wrtn:GAUGE:600:U:U'
                 ]

    rrdtool.create( rrdfile, '--start', '0',
                             '--step', '300',
                    data_sources,
                    'RRA:AVERAGE:0.5:1:360',
                    'RRA:AVERAGE:0.5:12:1008',
                    'RRA:AVERAGE:0.5:288:2016' )
    return True




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

