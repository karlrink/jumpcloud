
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
app.logger.setLevel(logging.DEBUG)

#app.logger.setLevel(logging.DEBUG)
#app.logger.debug('this will show in the log')

datadir = '/data/rrd'
x_api_key_file = datadir + '/x-api-key.txt'

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

                if os.path.isfile(rrdfile):
                    rrdtool.update(str(rrdfile), str(val))
                else:
                    app.logger.debug('missing ' + rrdfile)

                #try:
                #    rrdtool.update(str(rrdfile), str(val))
                #except rrdtool.error as e:
                #    print('rrdtool.error ' + str(e))

    system_id_file = datadir + '/' + str(system_id) + '.json'
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

    print(rrdfile)

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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

