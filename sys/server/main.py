
__version__ = '002.2'

from flask import Flask
from flask import request
from flask import jsonify
import logging
import json
import os
import hashlib

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

@app.route("/collector", methods=['POST', 'GET']) #POST collector?system_id=5e30c0b9890a7a4766268b59
def collector():                                  #GET  collector?alert_id=01413b9e26f16700301ad0333d470fcc27c3d768
    app.logger.debug('app.logger.debug')

    if request.method == 'POST':
        headers_api_key = request.headers.getlist("x-api-key", None)
        if not headers_api_key:
            app.logger.debug('no x-api-key')
            return jsonify('{"x-api-key":"None"}'), 200, {'Content-Type': 'application/json; charset=utf-8'}

        api_key = ''.join(headers_api_key)
        found_api_key = False
        with open(x_api_key_file, 'r') as filehandle:
            filedata = filehandle.readlines()
            for line in filedata:
                if api_key in line:
                    found_api_key = True

        if not found_api_key:
            return jsonify('{"x-api-key":"NotFound"}'), 200, {'Content-Type': 'application/json; charset=utf-8'}

        system_id = request.args.get("system_id", None)
        if not system_id:
            return jsonify('{"system_id":"None"}'), 200, {'Content-Type': 'application/json; charset=utf-8'}

        return post_request(system_id)

    if request.method == 'GET':
        alert_id = request.args.get("alert_id", None)
        if not alert_id:
            #return jsonify(''), 200, {'Content-Type': 'application/json; charset=utf-8'}
            return jsonify('{"alert_id":"None"}'), 200, {'Content-Type': 'application/json; charset=utf-8'}

        #return get_request(acknowledge_id)
        #try/check if alert...
        return get_request(alert_id)
        #return jsonify('{"alert_id":"Done"}'), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        return jsonify(''), 200, {'Content-Type': 'application/json; charset=utf-8'}


def get_request(alert_id):
    alert_file = '/data/alerts/' + str(alert_id) + '.json'
    if os.path.isfile(alert_file):

        try:
            with open(alert_file, 'r') as jsonfile:
                jdata = json.load(jsonfile)
        except Exception as e:
            print(str(e))
            return jsonify({'alert':'error'}), 200, {'Content-Type': 'application/json; charset=utf-8'}

        acknowledged = jdata.get('acknowledged', None)

        if acknowledged:
            return jsonify({'alert':'acknowledged'}), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            jdata['acknowledged'] = 'True'
            try:
                with open(alert_file, 'w+') as jsonfile:
                    json.dump(jdata, jsonfile)
            except Exception as e:
                return jsonify({'alert':'error'}), 200, {'Content-Type': 'application/json; charset=utf-8'}

            return jsonify({'alert':'updated'}), 200, {'Content-Type': 'application/json; charset=utf-8'}

        return jsonify({'alert':'true'}), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        #return jsonify('{"get":"none"}'), 200, {'Content-Type': 'application/json; charset=utf-8'}
        return jsonify(''), 200, {'Content-Type': 'application/json; charset=utf-8'}



def post_request(system_id):

    return_data = {'post':'ok'}

    jdata = request.get_json()

    #rrdList = jdata['rrdata']
    #print(type(rrdList))
    #for rr in rrdList:
    #    print(rr)
    #    print(type(rr))
    rrdList = jdata.get('rrdata', None)

    #alert = jdata['alert']
    alert = jdata.get('alert', None)
    if alert:
        acknowledged = None
        send_alert = True

        alert_hash = hashlib.sha1(str(system_id) + str(alert)).hexdigest()
        #acknowledged = get_alert(alert_hash)

        #print(str(alert_hash))
        #print(type(alert))

        alert_file = '/data/alerts/' + str(alert_hash) + '.json'

        #acknowledged_alert_file = alert_file + '.acknowledged'
        #if os.path.isfile(acknowledged_alert_file):
        #if os.path.isfile(alert_file + '.ack'):
        #    print('yes.alert_file ' + alert_file)
        #    app.logger.debug('yes.alert_file ' + alert_file)
        #    return_data = '{"alert":"acknowledged"}'
        #else:
        #    if not os.path.isfile(alert_file):
        #        with open(alert_file, 'w+') as filehandle:
        #            #print(type(alert))
        #            filehandle.write('{"system_id":"' + str(system_id) + '", \n')
        #            filehandle.write(' "alert": \n')
        #            filehandle.write(json.dumps(alert, indent=4))
        #            filehandle.write('}')

        if os.path.isfile(alert_file):
            try:
                with open(alert_file, 'r') as jsonfile:
                    alert_jdata = json.load(jsonfile)
                    #print(alert_jdata.get('acknowledged', False))
                    acknowledged = alert_jdata.get('acknowledged', None)
            except ValueError as e:
                print(str(e))
                app.logger.debug('ValueError with json ' + str(e))
                send_alert = False
                return_data = {'alert':'Fail','Error':'ValueError with json'}
            except Exception as e:
                print(str(e))
                app.logger.debug('Error ' + str(e))
                send_alert = False
                #return_data = {'alert':'Fail','Error': str(e) } #watch-out
                return_data = {'alert':'Fail','Error':'True' }
        else:
            with open(alert_file, 'w+') as filehandle:
                filehandle.write('{"system_id":"' + str(system_id) + '", \n')
                filehandle.write(' "alert": \n')
                filehandle.write(json.dumps(alert, indent=4))
                filehandle.write('}\n')

        if acknowledged:
            #print('acknowledged')
            app.logger.debug('acknowledged')
            return_data = {'alert':'acknowledged'}
            send_alert = False

        if send_alert:

            receivers = list([config.param['smtp_to']])
            subject = 'Alert: system ' + str(system_id) + ' has encountered an error'
            message = str(json.dumps(alert, indent=4))

            #acknowledge_link='https://monitor.nationsinfocorp.com/collector?acknowledge=' + str(alert_hash)
            acknowledge_link= config.param['url'] + '/collector?alert_id=' + str(alert_hash)
            message += '\n' + str(acknowledge_link)

            send_ses_email(receivers, subject, message)
            #print('SEND_SES_EMAIL DISABLED. NO EMAIL SENT')
            #return_data = '{"alert":"sent","alert_id":"' + str(acknowledge_link) +  '"}'
            return_data = {'alert':'sent','alert_id': str(acknowledge_link) }

    if not rrdList:
        return jsonify({'rrd':'None'}), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif len(rrdList) == 0:
        return jsonify({'rrd':'Zero'}), 200, {'Content-Type': 'application/json; charset=utf-8'}
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

                if rrd == 'sbm' and not os.path.isfile(rrdfile):
                    sbmRRD(rrdfile)
                    continue

                if rrd == 'mysql' and not os.path.isfile(rrdfile):
                    mysqlRRD(rrdfile)
                    continue

                if rrd == 'chrony' and not os.path.isfile(rrdfile):
                    chronyRRD(rrdfile)
                    continue



                if os.path.isfile(rrdfile):
                    try:
                        rrdtool.update(str(rrdfile), str(val))
                    except Exception as e:
                        app.logger.debug(str(e))
                else:
                    app.logger.debug('missing ' + rrdfile)

                #try:
                #    rrdtool.update(str(rrdfile), str(val))
                #except rrdtool.error as e:
                #    print('rrdtool.error ' + str(e))

    system_id_file = datadir + '/' + str(system_id) + '/' + str(system_id) + '.json'
    with open(system_id_file, 'w+') as jsonfile:
        json.dump(jdata, jsonfile)

    return jsonify(return_data), 200, {'Content-Type': 'application/json; charset=utf-8'}


def send_ses_email(receivers, subject, message):
    import smtplib
    sender_email = config.param['smtp_from']
    smtp_server  = config.param['smtp_host']
    port         = config.param['smtp_port']
    smtp_user    = config.param['smtp_user']
    smtp_pass    = config.param['smtp_pass']

    header =  ("From: %s\r\nTo: %s\r\n"
            % (sender_email, ",".join(receivers)))
    header += ("Subject: %s\r\n\r\n" % (subject))
    msg = header + message

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(sender_email, receivers, msg)
    except Exception as e:
        #print('smtplib.SMTP.Error ' + str(e))
        app.logger.info('smtplib.SMTP.Error ' + str(e))
        return False

    return True

    #python3
    #context = ssl.create_default_context()
    #with smtplib.SMTP(smtp_server, port) as server:
    #    server.ehlo()
    #    server.starttls(context=context)
    #    server.ehlo()
    #    server.login(smtp_user, smtp_pass)
    #    server.sendmail(sender_email, receivers, msg)
    #with smtplib.SMTP(smtp_server, port) as server:
    #AttributeError: SMTP instance has no attribute '__exit__'

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

    rrdtool.create(str(rrdfile), '--start', '0',
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

    rrdtool.create(str(rrdfile), '--start', '0',
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

    rrdtool.create(str(rrdfile), '--start', '0',
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

    rrdtool.create(str(rrdfile), '--start', '0',
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

    rrdtool.create(str(rrdfile), '--start', '0',
                                 '--step', '300',
                    data_sources,
                    'RRA:AVERAGE:0.5:1:360',
                    'RRA:AVERAGE:0.5:12:1008',
                    'RRA:AVERAGE:0.5:288:2016' )
    return True


def chronyRRD(rrdfile=None):

    data_sources=[ 'DS:Stratum:GAUGE:600:U:U',
                   'DS:System:GAUGE:600:U:U',
                   'DS:RMS:GAUGE:600:U:U',
                   'DS:Frequency:GAUGE:600:U:U',
                   'DS:Skew:GAUGE:600:U:U',
                   'DS:Root_delay:GAUGE:600:U:U',
                   'DS:Root_dispersion:GAUGE:600:U:U',
                   'DS:Update:GAUGE:600:U:U'
                 ]

    rrdtool.create(str(rrdfile), '--start', '0',
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

    rrdtool.create(str(rrdfile), '--start', '0',
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

    rrdtool.create(str(rrdfile), '--start', '0',
                                 '--step', '300',
                    data_sources,
                    'RRA:AVERAGE:0.5:1:360',
                    'RRA:AVERAGE:0.5:12:1008',
                    'RRA:AVERAGE:0.5:288:2016' )
    return True

def sbmRRD(rrdfile=None):
    #name = 'sbm'
    #cmdline = 'rrdtool create ' + rrdfile
    #cmdline += ' --start 0 --step 300 '
    #cmdline += ' DS:%s:GAUGE:600:0:U ' % name
    #cmdline += ' RRA:AVERAGE:0.5:1:360 '
    #cmdline += ' RRA:AVERAGE:0.5:10:1008 '
    #if debug: print "cmdline: " + cmdline
    #os.system(cmdline)

    data_sources=[ 'DS:sbm:GAUGE:600:U:U'
                 ]

    rrdtool.create(str(rrdfile), '--start', '0',
                                 '--step', '300',
                    data_sources,
                    'RRA:AVERAGE:0.5:1:360',
                    'RRA:AVERAGE:0.5:12:1008',
                    'RRA:AVERAGE:0.5:288:2016' )
    return True

#Note: A ds-name must be 1 to 19 characters [a-zA-Z0-9_]
def mysqlRRD(rrdfile=None):
    #__name__ = 'mysql'
    #print "running rrdtool create"
    #cmdline = 'rrdtool create ' + rrdfile
    #cmdline += ' --start 0 --step 300 '
    #cmdline += ' DS:AbortedClients:GAUGE:600:U:U '
    #cmdline += ' DS:AbortedConnects:GAUGE:600:U:U '
    #cmdline += ' DS:AccessDeniedErrors:GAUGE:600:U:U '
    #cmdline += ' DS:BytesReceived:GAUGE:600:U:U '
    #cmdline += ' DS:BytesSent:GAUGE:600:U:U '
    #cmdline += ' DS:Connections:GAUGE:600:U:U '
    #cmdline += ' DS:CreatedTMPFiles:GAUGE:600:U:U '
    #cmdline += ' DS:InnoBufPoolPgsData:GAUGE:600:U:U '
    #cmdline += ' DS:InnoBufPoolBytsData:GAUGE:600:U:U '
    #cmdline += ' DS:InnoBufPoolBytsDrty:GAUGE:600:U:U '
    #cmdline += ' DS:InnoBufPoolPgsFlshd:GAUGE:600:U:U '
    #cmdline += ' DS:InnoBufPoolPgsFree:GAUGE:600:U:U '
    #cmdline += ' DS:InnoBufPoolPgsTotal:GAUGE:600:U:U '
    #cmdline += ' DS:InnoBufPoolReads:GAUGE:600:U:U '
    #cmdline += ' DS:InnoDataPendFsyncs:GAUGE:600:U:U '
    #cmdline += ' DS:InnoDataPendReads:GAUGE:600:U:U '
    #cmdline += ' DS:InnoDataPendWrites:GAUGE:600:U:U '
    #cmdline += ' DS:InnoDataReads:GAUGE:600:U:U '
    #cmdline += ' DS:InnoDataWrites:GAUGE:600:U:U '
    #cmdline += ' DS:InnoDblWrites:GAUGE:600:U:U '
    #cmdline += ' DS:InnoRowLockCurrWait:GAUGE:600:U:U '
    #cmdline += ' DS:InnoRowLockTime:GAUGE:600:U:U '
    #cmdline += ' DS:InnoRowLockTimeAvg:GAUGE:600:U:U '
    #cmdline += ' DS:InnoRowLockTimeMax:GAUGE:600:U:U '
    #cmdline += ' DS:InnoNumOpenFiles:GAUGE:600:U:U '
    #cmdline += ' DS:InnoRowLockWaits:GAUGE:600:U:U '
    #cmdline += ' DS:InnoRowsRead:GAUGE:600:U:U '
    #cmdline += ' DS:InnoRowsUpdated:GAUGE:600:U:U '
    #cmdline += ' DS:InnoRowsDeleted:GAUGE:600:U:U '
    #cmdline += ' DS:InnoRowsInserted:GAUGE:600:U:U '
    #cmdline += ' DS:MaxUsedConnections:GAUGE:600:U:U '
    #cmdline += ' DS:MemoryUsed:GAUGE:600:U:U '
    #cmdline += ' DS:OpenFiles:GAUGE:600:U:U '
    #cmdline += ' DS:OpenTables:GAUGE:600:U:U '
    #cmdline += ' DS:OpenedFiles:GAUGE:600:U:U '
    #cmdline += ' DS:Opene_tables:GAUGE:600:U:U '
    #cmdline += ' DS:QcacheHits:GAUGE:600:U:U '
    #cmdline += ' DS:Queries:GAUGE:600:U:U '
    #cmdline += ' DS:Questions:GAUGE:600:U:U '
    #cmdline += ' DS:SlaveConnections:GAUGE:600:U:U '
    #cmdline += ' DS:SlavesConnected:GAUGE:600:U:U '
    #cmdline += ' DS:SlowQueries:GAUGE:600:U:U '
    #cmdline += ' DS:ThreadsConnected:GAUGE:600:U:U '
    #cmdline += ' DS:ThreadsRunning:GAUGE:600:U:U '
    #cmdline += ' DS:Uptime:GAUGE:600:U:U '
    #cmdline += ' RRA:AVERAGE:0.5:1:360 '
    #cmdline += ' RRA:AVERAGE:0.5:12:1008 '
    #cmdline += ' RRA:AVERAGE:0.5:288:2016 '
    #if debug: print "cmdline: " + cmdline
    #os.system(cmdline)

    data_sources=[ 'DS:AbortedClients:GAUGE:600:U:U',
                   'DS:AbortedConnects:GAUGE:600:U:U',
                   'DS:AccessDeniedErrors:GAUGE:600:U:U',
                   'DS:BytesReceived:GAUGE:600:U:U',
                   'DS:BytesSent:GAUGE:600:U:U',
                   'DS:Connections:GAUGE:600:U:U',
                   'DS:CreatedTMPFiles:GAUGE:600:U:U',
                   'DS:InnoBufPoolPgsData:GAUGE:600:U:U',
                   'DS:InnoBufPoolBytsData:GAUGE:600:U:U',
                   'DS:InnoBufPoolBytsDrty:GAUGE:600:U:U',
                   'DS:InnoBufPoolPgsFlshd:GAUGE:600:U:U',
                   'DS:InnoBufPoolPgsFree:GAUGE:600:U:U',
                   'DS:InnoBufPoolPgsTotal:GAUGE:600:U:U',
                   'DS:InnoBufPoolReads:GAUGE:600:U:U',
                   'DS:InnoDataPendFsyncs:GAUGE:600:U:U',
                   'DS:InnoDataPendReads:GAUGE:600:U:U',
                   'DS:InnoDataPendWrites:GAUGE:600:U:U',
                   'DS:InnoDataReads:GAUGE:600:U:U',
                   'DS:InnoDataWrites:GAUGE:600:U:U',
                   'DS:InnoDblWrites:GAUGE:600:U:U',
                   'DS:InnoRowLockCurrWait:GAUGE:600:U:U',
                   'DS:InnoRowLockTime:GAUGE:600:U:U',
                   'DS:InnoRowLockTimeAvg:GAUGE:600:U:U',
                   'DS:InnoRowLockTimeMax:GAUGE:600:U:U',
                   'DS:InnoNumOpenFiles:GAUGE:600:U:U',
                   'DS:InnoRowLockWaits:GAUGE:600:U:U',
                   'DS:InnoRowsRead:GAUGE:600:U:U',
                   'DS:InnoRowsUpdated:GAUGE:600:U:U',
                   'DS:InnoRowsDeleted:GAUGE:600:U:U',
                   'DS:InnoRowsInserted:GAUGE:600:U:U',
                   'DS:MaxUsedConnections:GAUGE:600:U:U',
                   'DS:MemoryUsed:GAUGE:600:U:U',
                   'DS:OpenFiles:GAUGE:600:U:U',
                   'DS:OpenTables:GAUGE:600:U:U',
                   'DS:OpenedFiles:GAUGE:600:U:U',
                   'DS:Opene_tables:GAUGE:600:U:U',
                   'DS:QcacheHits:GAUGE:600:U:U',
                   'DS:Queries:GAUGE:600:U:U',
                   'DS:Questions:GAUGE:600:U:U',
                   'DS:SlaveConnections:GAUGE:600:U:U',
                   'DS:SlavesConnected:GAUGE:600:U:U',
                   'DS:SlowQueries:GAUGE:600:U:U',
                   'DS:ThreadsConnected:GAUGE:600:U:U',
                   'DS:ThreadsRunning:GAUGE:600:U:U',
                   'DS:Uptime:GAUGE:600:U:U'
                 ]

    rrdtool.create(str(rrdfile), '--start', '0',
                                 '--step', '300',
                    data_sources,
                    'RRA:AVERAGE:0.5:1:360',
                    'RRA:AVERAGE:0.5:12:1008',
                    'RRA:AVERAGE:0.5:288:2016' )
    return True


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)


