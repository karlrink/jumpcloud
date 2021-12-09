#!/usr/bin/env python2

import netsnmp
import json

import rrdtool
import os

import config

system_id = config.param['system_id']
dest_host = config.param['dest_host']

oid = netsnmp.VarList('IF-MIB::ifName','IF-MIB::ifOperStatus', 
        'IF-MIB::ifInOctets','IF-MIB::ifInUcastPkts','IF-MIB::ifInNUcastPkts',
        'IF-MIB::ifInDiscards','IF-MIB::ifInErrors',
        'IF-MIB::ifOutOctets','IF-MIB::ifOutUcastPkts','IF-MIB::ifOutNUcastPkts',
        'IF-MIB::ifOutDiscards','IF-MIB::ifOutErrors',
        'IF-MIB::ifInMulticastPkts','IF-MIB::ifInBroadcastPkts',
        'IF-MIB::ifOutMulticastPkts','IF-MIB::ifOutBroadcastPkts')

snmp_res = netsnmp.snmpwalk(oid, Version=1, DestHost=str(dest_host), Community='public')

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

returnList = chunks(snmp_res, 16)

rrDict = {}
rrList = []
for i in returnList:
    #print(i)
    ifName = str(i[0])
    #cleanup text, no '/'
    ifName = ifName.replace('/','')


    ifOperStatus = str(i[1])
    ifInOctets = str(i[2])
    ifInUcastPkts = str(i[3])
    ifInNUcastPkts = str(i[4])
    ifInDiscards = str(i[5])
    ifInErrors = str(i[6])
    ifOutOctets = str(i[7])
    ifOutUcastPkts = str(i[8])
    ifOutNUcastPkts = str(i[9])
    ifOutDiscards = str(i[10])
    ifOutErrors = str(i[11])
    ifInMulticastPkts = str(i[12])
    ifInBroadcastPkts = str(i[13])
    ifOutMulticastPkts = str(i[14])
    ifOutBroadcastPkts = str(i[15])

    rr = 'N:' + ifOperStatus
    rr += ':' + ifInOctets
    rr += ':' + ifInUcastPkts
    rr += ':' + ifInNUcastPkts
    rr += ':' + ifInDiscards
    rr += ':' + ifInErrors
    rr += ':' + ifOutOctets
    rr += ':' + ifOutUcastPkts
    rr += ':' + ifOutNUcastPkts
    rr += ':' + ifOutDiscards
    rr += ':' + ifOutErrors
    rr += ':' + ifInMulticastPkts
    rr += ':' + ifInBroadcastPkts
    rr += ':' + ifOutMulticastPkts
    rr += ':' + ifOutBroadcastPkts

    rrDict[ifName] = rr

def ifRRD(rrdfile=None):
    data_sources=[ 'DS:ifOperStatus:GAUGE:600:U:U',
                   'DS:ifInOctets:COUNTER:600:U:U',
                   'DS:ifInUcastPkts:COUNTER:600:U:U',
                   'DS:ifInNUcastPkts:COUNTER:600:U:U',
                   'DS:ifInDiscards:COUNTER:600:U:U',
                   'DS:ifInErrors:COUNTER:600:U:U',
                   'DS:ifOutOctets:COUNTER:600:U:U',
                   'DS:ifOutUcastPkts:COUNTER:600:U:U',
                   'DS:ifOutNUcastPkts:COUNTER:600:U:U',
                   'DS:ifOutDiscards:COUNTER:600:U:U',
                   'DS:ifOutErrors:COUNTER:600:U:U',
                   'DS:ifInMulticastPkts:COUNTER:600:U:U',
                   'DS:ifInBroadcastPkts:COUNTER:600:U:U',
                   'DS:ifOutMulticastPkts:COUNTER:600:U:U',
                   'DS:ifOutBroadcastPkts:COUNTER:600:U:U'
                 ]
    rrdtool.create(str(rrdfile), '--start', '0',
                                 '--step', '300',
                    data_sources,
                    'RRA:AVERAGE:0.5:1:360',
                    'RRA:AVERAGE:0.5:12:1008',
                    'RRA:AVERAGE:0.5:288:2016' )
    return True

##################################################################
for k,v in rrDict.items():
    #print(k,v)
    #rrdfile = '/data/rrd/' + system_id + '/if.' + str(k) +'.rrd'
    rrdfile = '/data/rrd/' + system_id + '/' + str(k) +'.rrd'
    print(rrdfile)
    if not os.path.isfile(rrdfile):
        ifRRD(rrdfile)
    else:
        rrdtool.update(str(rrdfile), str(v))

    #rrdata = {'rrd': 'if.' + str(k), 'val': v}
    rrdata = {'rrd': str(k), 'val': v, 'type': 'cisco.asa.if'}
    rrList.append(rrdata)

json_data = '{ "system_id":"' + str(system_id) + '",'
json_data += '"rrdata": ' + json.dumps(rrList)
json_data += '}'
#print(json.dumps(json.loads(json_data), indent=4))

#        {
#            "rrd": "if.inside1", 
#            "val": "N:1:4019517575:3085930203:5417172:7138227:0:4177909917:3896715867:206898:0:0:0:0:0:0"
#        }, 

######################################################################

jdata = None
system_id_json = '/data/rrd/' + system_id + '/' + system_id + '.json'
if not os.path.isfile(system_id_json):
    with open(system_id_json, 'w') as jsonfile:
        json.dump(json.loads(json_data), jsonfile, indent=4)
        jdata = json.load(jsonfile)
else:
    #print('check.for.state')
    with open(system_id_json, 'r') as jsonfile:
        jdata = json.load(jsonfile)

rr_data = jdata['rrdata']
#print(rr_data)
for line in rr_data:
    #print(line['val'])
    #valList = str(line['val']).split(':')
    #print(valList[1])
    OperStatus = str(line['val']).split(':')[1]
    print(OperStatus)


######################################################################


# the function snmpwalk returns a set of 4-tuples:
#   var.tag  (the object OID)
#   var.iid   (the index)
#   var.val  (the value)
#   var.type (the type)

#OID	1.3.6.1.2.1.2.2.1.8
#IF-MIB (CISCO)
#ifOperStatus
#The current operational state of the interface. The testing(3) state indicates that no operational packets can be passed. If ifAdminStatus is down(2) then ifOperStatus should be down(2). If ifAdminStatus is changed to up(1) then ifOperStatus should change to up(1) if the interface is ready to transmit and receive network traffic; it should change to dormant(5) if the interface is waiting for external actions (such as a serial line waiting for an incoming connection); it should remain in the down(2) state if and only if there is a fault that prevents it from going to the up(1) state; it should remain in the notPresent(6) state if the interface has missing (typically, hardware) components.
#Enumeration (1-up, 2-down, 3-testing, 4-unknown, 5-dormant, 6-notPresent, 7-lowerLayerDown)

#IF-MIB::ifOperStatus.2 = INTEGER: down(2)
#IF-MIB::ifOperStatus.3 = INTEGER: up(1)


