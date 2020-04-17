#!/usr/bin/env python2

__version__ = '0000.001'

import sys
sys.dont_write_bytecode = True

import json
import subprocess

import config
ipmi_user = config.param['ipmi_user']
ipmi_pass = config.param['ipmi_pass']
url = config.param['url']

import urllib2
import ssl
import os
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


import rrdtool

def usage():
    print("Usage: " + sys.argv[0] + " host [option]" + """

        --disable-post
        --write-local
    """)
    sys.exit(0)

def collect_ipmi(host):

    collect='/usr/bin/ipmitool -I lanplus -U ' + ipmi_user + '  -P ' + ipmi_pass + ' -H ' + host + ' sdr'
    p = subprocess.Popen(collect, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, err = p.communicate()

    exit_code = p.wait()
    if (exit_code != 0):
        print('Error: ' + str(err) + ' ' + str(output))
        #return chronyc_data, chronyc_alert
        #return False
        #sys.exit(exit_code)
        return {}

    multilines = output.splitlines()

    DDict = {}
    for line in multilines:
        line = line.split('|')
        #print(line)
        #column0 = line[0]
        #print(len(line)) #3
        column0 = line[0]
        column1 = line[1]
        column2 = line[2]

        #print(column0, column1, column2)

        column0 = column0.strip()
        #column0 = column0.replace(' ', '_')
        column0 = column0.replace(' ', '')

        column0 = column0.replace('Temperature', 'Temp')
        column0 = column0.replace('%', '_P')
        column0 = column0.replace('+', '')
        column0 = column0.replace('.', '-')

        #print(len(column0))
        #print(column0)

        #Note: A ds-name must be 1 to 19 characters [a-zA-Z0-9_]
        if len(column0) > 19:
            column0 = column0[:19]

        #print column0

        column1 = column1.strip()
        #print(column0 + ' ' + column1)

        column2 = column2.strip()
        #print(column0 + ' ' + column2)

        #if column2 == 'ns':
        #    print(column0 + ' ' + column2)
        #if column2 != 'ok':
        #    print(column0 + ' ' + column2)

        #print(column0 + '|' + column1 + '|' + column2)

        column1 = column1.split(' ')

        #if column1[1]:
        #    if column1[1] == 'Watts':
        #        column0 = column0 + 'Watts'

        try:
            if column1[1] == 'CFM':
                column0 = column0 + '_CFM'
            if column1[1] == 'RPM':
                column0 = column0 + '_RPM'
            if column1[1] == 'Watts':
                column0 = column0 + '_Wtts'
            #if column1[1] == 'Volts':
            #    column0 = column0 + 'Volts'
            if column1[1] == 'degrees':
                #column0 = column0 + column1[2]
                #column0 = column0 + 'Celsius'
                column0 = column0 + '_C'

        except IndexError as e:
            pass

        if len(column0) > 19:
            column0 = column0[:19]

        DDict[column0] = column1[0]


    #for k,v in DDict.items():
    #    if v == '0x00':
    #        continue
    #    if v == 'no reading':
    #        continue
    #    print(v)

    for k,v in DDict.items():
        #print('VAL - ' + v)
        if v == '0x00':
            del DDict[k]
        #if v == 'no reading':
        if v == 'no':
            del DDict[k]
        if v == 'disabled':
            del DDict[k]

    #print(DDict)
    return DDict

def ipmiRRD(rrdfile, data_dict):

    data_sources = []
    for k,v in c.items():
        #print(k, v)
        ds = 'DS:' + str(k) + ':GAUGE:600:U:U'
        data_sources.append(ds)
    print(str(data_sources))

    #data_sources=[ 'DS:total:GAUGE:600:U:U',
    #               'DS:used:GAUGE:600:U:U',
    #               'DS:free:GAUGE:600:U:U',
    #               'DS:shared:GAUGE:600:U:U',
    #               'DS:buffers:GAUGE:600:U:U',
    #               'DS:cached:GAUGE:600:U:U' ]

#  File "./collect.ipmi.py", line 135, in ipmiRRD
#    'RRA:AVERAGE:0.5:288:2016' )
#rrdtool.OperationalError: invalid DS format



    rrdtool.create(str(rrdfile), '--start', '0',
                                 '--step', '300',
                    data_sources,
                    'RRA:AVERAGE:0.5:1:360',
                    'RRA:AVERAGE:0.5:12:1008',
                    'RRA:AVERAGE:0.5:288:2016')
    return True

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




if __name__ == "__main__":
    disable_post = write_local = False
    if sys.argv[1:]:
        for arg in sys.argv[1:]:
            host = sys.argv[1]
            if arg == '--disable-post':
                disable_post = True
            if arg == '--write-local':
                write_local = True
    else:
        usage()

    try:
        system_id = config.hosts[host]
    except KeyError as e:
        print('Host Not Found: ' + str(e))
        sys.exit(1)

    c = collect_ipmi(host)
    #hdr = 'N'
    #val = 'N'
    #for k,v in c.items():
    #    hdr += ':' + str(k)
    #    val += ':' + str(v)

    rrd = {'rrd': 'ipmi', 'val': c, 'type': 'json'}
    #rrd = {'rrd': 'ipmi.json', 'val': c} 
    rrdList = [ rrd ]

    json_data  = '{ "system_id": "' + str(system_id) + '",'
    json_data += '"rrdata": ' + str(json.dumps(rrdList))
    json_data += '}'

    print(json.dumps(json.loads(json_data), sort_keys=True, indent=4))
    if not disable_post:
        response = post(system_id, json.dumps(json_data))
        try:
            print(json.dumps(json.loads(response)))
        except Exception as e:
            print(response)

    sys.exit(1)

#    for host, system_id in config.hosts.items():
#        #print(system_id)
#        c = collect_ipmi(host)
#        
#        #print(c)
#        #sys.exit(99)
#
#        val = 'N'
#        rrdfile = str(host) + '.rrd'
#        if not os.path.isfile(rrdfile):
#            ipmiRRD(rrdfile, c)
#        else:
#            for k,v in c.items():
#                val += ':' + str(v)
#
#            try:
#                rrdtool.update(str(rrdfile), str(val))
#            except Exception as e:
#                print(e)
#
#        #rrd = {'rrd': str(domain.name()) + '.' + str(item), 'val': rrd_val, 'type': 'ipmi.json'}
#        rrd = {'rrd': 'ipmi.json', 'val': val, 'type': 'ipmi.json'}
#        #print(rrd)
#
#        rrdList = [rrd]
#
#        #system_id = '1234'
#
#        json_data  = '{ "system_id": "' + str(system_id) + '",'
#        json_data += '"rrdata": ' + str(json.dumps(rrdList))
#        json_data += '}'
#
#        print(json.dumps(json.loads(json_data), sort_keys=True, indent=4))


