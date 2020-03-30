#!/usr/bin/env python2

import netsnmp

oid = netsnmp.VarList('IF-MIB::ifName','IF-MIB::ifOperStatus', 
        'IF-MIB::ifInOctets','IF-MIB::ifInUcastPkts','IF-MIB::ifInNUcastPkts',
        'IF-MIB::ifInDiscards','IF-MIB::ifInErrors',
        'IF-MIB::ifOutOctets','IF-MIB::ifOutUcastPkts','IF-MIB::ifOutNUcastPkts',
        'IF-MIB::ifOutDiscards','IF-MIB::ifOutErrors',
        'IF-MIB::ifInMulticastPkts','IF-MIB::ifInBroadcastPkts',
        'IF-MIB::ifOutMulticastPkts','IF-MIB::ifOutBroadcastPkts')

#oid = netsnmp.VarList('IF-MIB::ifName','IF-MIB::ifOperStatus')

snmp_res = netsnmp.snmpwalk(oid, Version=1, DestHost='216.34.200.142', Community='public')
#for x in range(2):
#    #print "snmp_res:: ", x.iid, " = ", x.val
#    print(ifName.val)
#    print(ifOperStatus.val)
#for x in oid:
#print(snmp_res)

#print(type(snmp_res))
#print(snmp_res)

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

#returnList = list(chunks(snmp_res, 16))
returnList = chunks(snmp_res, 16)

for i in returnList:
    print(i)


#netsnmp.Varbind('1.3.6.1.4.1.9.9.109.1.1.1.1.3.', ''))
#'1.3.6.1.4.1.9.9.109.1.1.1.1.3.')

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

















#session = netsnmp.Session(DestHost='216.34.200.142', Version=1, Community='public')
#vars = netsnmp.VarList(netsnmp.Varbind('ifIndex',), netsnmp.Varbind('ifDescr',), netsnmp.Varbind('ifOperStatus',))
#print(session.getbulk(0, 48, vars))

#var = netsnmp.Varbind('sysDescr.0')
#res = netsnmp.snmpget(var, Version = 1, DestHost = '216.34.200.142', Community='public')
#print(res)

#oid = netsnmp.Varbind('sysDescr')
#result = netsnmp.snmpwalk(oid, Version = 1, DestHost="216.34.200.142",Community="public")
#print(result)

#var =  netsnmp.VarList(netsnmp.Varbind('ifDescr'))
#var =  netsnmp.Varbind('ifDescr')
#res = netsnmp.snmpget(var, Version = 1, DestHost = '216.34.200.142', Community='public')
#for v in var:
#    print(v)
#print(res)


