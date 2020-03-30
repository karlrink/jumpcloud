#!/usr/bin/env python2

import netsnmp
import json
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

for k,v in rrDict.items():
    #print(k)
    #print(v)
    rrdata = {'rrd': 'if.' + str(k), 'val': v}
    rrList.append(rrdata)

#print(json.dumps(rrDict, sort_keys=True, indent=4))

json_data = '{ "system_id":"' + str(system_id) + '",'
#json_data += '"rrdata": [' + str(json.dumps(json.loads(rrdata))) + ']'
json_data += '"rrdata": ' + json.dumps(rrList)
json_data += '}'
print(json.dumps(json.loads(json_data), indent=4))


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


