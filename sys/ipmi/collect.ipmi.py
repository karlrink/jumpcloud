#!/usr/bin/env python2

__version__ = '0000.0'

import sys
sys.dont_write_bytecode = True

import subprocess
import os

import config
ipmi_user = config.param['ipmi_user']
ipmi_pass = config.param['ipmi_pass']

import rrdtool

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
        column0 = column0.replace('.', '')

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


if __name__ == "__main__":

    for host in config.hosts:
        #print(host)
        c = collect_ipmi(host)
        #print(c)

        rrdfile = str(host) + '.rrd'
        if not os.path.isfile(rrdfile):
            ipmiRRD(rrdfile, c)
        else:
            val = 'N'
            for k,v in c.items():
                val += ':' + str(v)
            rrdtool.update(str(rrdfile), str(val))

        #rr_val = 'N:' +
        #rrdtool.update(str(rrdfile), str(val))


