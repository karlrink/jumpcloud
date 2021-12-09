#!/usr/bin/env python2

__version__ = 'hypervisor.collector:001b'

import libvirt
#apt-get install -y python-libvirt

import sys
import json


class ListDomainsClass(object):
    def __init__(self, uri, host):
        self.uri = uri
        self.host = host

    def get(self):
        returnDict = {}
        uri_handle = str(self.uri) + str(self.host) + '/system'
        try:
            self.conn = libvirt.openReadOnly(uri_handle)
        except libvirt.libvirtError as e:
            return {"Error":str(e)}

        domains = self.conn.listAllDomains(0)
        if len(domains) != 0:
            for domain in domains:
                state = self.domstate(domain.name())
                returnDict[domain.name()] = str(state).lower()

        return returnDict

    def domstate(self,domName=None):
        dom = self.conn.lookupByName(domName)
        if dom == None:
            return str('NOTFOUND').lower()

        state, reason = dom.state()
        if state == libvirt.VIR_DOMAIN_NOSTATE:
            state='NOSTATE'
        elif state == libvirt.VIR_DOMAIN_RUNNING:
            state='RUNNING'
        elif state == libvirt.VIR_DOMAIN_BLOCKED:
            state='BLOCKED'
        elif state == libvirt.VIR_DOMAIN_PAUSED:
            state='PAUSED'
        elif state == libvirt.VIR_DOMAIN_SHUTDOWN:
            state='SHUTDOWN'
        elif state == libvirt.VIR_DOMAIN_SHUTOFF:
            state='SHUTOFF'
        elif state == libvirt.VIR_DOMAIN_CRASHED:
            state='CRASHED'
        elif state == libvirt.VIR_DOMAIN_PMSUSPENDED:
            state='PMSUSPENDED'
        else:
            state='UNKNOWN'

        return str(state).lower()

class ListDomainsDetailedClass(ListDomainsClass):
    def get(self):
        runningDict = {}
        uri_handle = str(self.uri) + str(self.host) + '/system'
        #print('uri_handle ' + uri_handle)
        try:
            self.conn = libvirt.openReadOnly(uri_handle)
        except libvirt.libvirtError as e:
            return {"Error":str(e)}

        hvm_type = str(self.conn.getType())
        hypervisor_type = hvm_type.lower()

        nodeinfo = self.conn.getInfo()
        hvm_model = str(nodeinfo[0])
        hvm_mem = str(nodeinfo[1])
        hvm_cpu = str(nodeinfo[2])
        stats = self.conn.getCPUStats(libvirt.VIR_NODE_CPU_STATS_ALL_CPUS)

        hypervisor_cpu = {
          'count': str(hvm_cpu),
          'type': str(hvm_model),
          'kernel': str(stats['kernel']),
          'idle': str(stats['idle']),
          'user': str(stats['user']),
          'iowait': str(stats['iowait'])
        }

#  "hypervisor": {
#    "cpu": {
#      "count": "24", 
#      "idle": "50414176940000000", 
#      "iowait": "558116710000000", 
#      "kernel": "794222650000000", 
#      "type": "x86_64", 
#      "user": "4615971910000000"
#    }, 

        hypervisor_cpu_rrd_val = 'N:' + str(hypervisor_cpu['count'])
        hypervisor_cpu_rrd_val += ':' + str(hypervisor_cpu['idle'])
        hypervisor_cpu_rrd_val += ':' + str(hypervisor_cpu['iowait'])
        hypervisor_cpu_rrd_val += ':' + str(hypervisor_cpu['kernel'])
        hypervisor_cpu_rrd_val += ':' + str(hypervisor_cpu['user'])
        hypervisor_cpu_rrd = {'rrd':'hypervisor.cpu', 'val': str(hypervisor_cpu_rrd_val)}

        memfree = self.conn.getFreeMemory()
        memfreeMB = memfree / 1024 / 1024
        memusedMB = int(hvm_mem) - int(memfreeMB)

        hypervisor_mem = {
          'total': str(hvm_mem),
          'used': str(memusedMB),
          'free': str(memfreeMB)
        }

#    "mem": {
#      "free": "195", 
#      "total": "32116", 
#      "used": "31921"
#    }, 

        hypervisor_mem_rrd_val = 'N:' + str(hypervisor_mem['free'])
        hypervisor_mem_rrd_val += ':' + str(hypervisor_mem['total'])
        hypervisor_mem_rrd_val += ':' + str(hypervisor_mem['used'])
        hypervisor_mem_rrd = {'rrd':'hypervisor.mem', 'val': str(hypervisor_mem_rrd_val)}


        hypervisor = {
          'type': hypervisor_type,
          'cpu': hypervisor_cpu,
          'mem': hypervisor_mem
        }

        runningDict['hypervisor'] = hypervisor

#####################################################################################################
        def domStatus(domName=None):
            runningStatus = {}

            dom = self.conn.lookupByName(domName)
            if dom == None:
                print json.dumps({"Error":"Failed to find domain " + str(domName)}, indent=2)
                #sys.exit(1)
                return False

            state = self.domstate(domName)

            state_lower_case = str(state).lower()
            runningStatus['state'] = state_lower_case

            active = dom.isActive()
            if active == True:
                ok=1
            else:
                return {'state': state}

            cpus = dom.maxVcpus() #dom cpu count
            if cpus != -1:
                pass
            else:
                print json.dumps({"Error":"major error getting dom.Vcpus()"}, indent=2)
                #sys.exit(1)
                return False

            cpu_stats = dom.getCPUStats(True)
            cpu_time = str(cpu_stats[0]['cpu_time'])
            system_time = str(cpu_stats[0]['system_time'])
            user_time = str(cpu_stats[0]['user_time'])

            dom_cpu = {
              'count': str(cpus),
              'cpu_time': cpu_time,
              'system_time': system_time,
              'user_time': user_time
            }

            runningStatus['cpu'] = dom_cpu

            mem = dom.maxMemory()
            if mem > 0:
                pass
            else:
                print json.dumps({"Error":"major error getting dom.maxMemory()"}, indent=2)
                #sys.exit(1)
                return False

            dom_mem = {}
            mem_stats  = dom.memoryStats()

            for name in mem_stats:
                if name:
                    dom_mem[name] = str(mem_stats[name])

            runningStatus['mem'] = dom_mem

            from xml.dom import minidom
            raw_xml = dom.XMLDesc(0)
            #print(str(raw_xml))
#  <devices>
#    <emulator>/usr/bin/kvm</emulator>
#    <disk type='file' device='disk'>
#      <driver name='qemu' type='raw'/>
#      <source file='/ssd/data/appserv-sturm/hda.raw'/>
#      <backingStore/>
#      <target dev='hda' bus='virtio'/>
#      <alias name='virtio-disk0'/>
#      <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
#    </disk>

            xml = minidom.parseString(raw_xml)

            diskTypes = xml.getElementsByTagName('disk')
            diskDict = {}
            source = ''

            for diskType in diskTypes:
                diskNodes = diskType.childNodes
                for diskNode in diskNodes:
                    if diskNode.nodeName[0:1] != '#':
                        if diskNode.nodeName == 'source':
                            for attr in diskNode.attributes.keys():
                                #print('NAME ' + str(diskNode.attributes[attr].name))
                                #print('VALUE ' + str(diskNode.attributes[attr].value))
                                if diskNode.attributes[attr].name == 'dev':
                                    source = str(diskNode.attributes[attr].value)
                                elif diskNode.attributes[attr].name == 'file':
                                    source = str(diskNode.attributes[attr].value)
                                else:
                                    source = 'Unknown'
                        if diskNode.nodeName == 'target':
                            for attr in diskNode.attributes.keys():
                                if diskNode.attributes[attr].name == 'dev':
                                    target = str(diskNode.attributes[attr].value)
                                    rd_req, rd_bytes, wr_req, wr_bytes, err = dom.blockStats(source)

                                    diskDict[target] = {
                                      'device': str(source),
                                      'read_requests_issued': str(rd_req),
                                      'bytes_read': str(rd_bytes),
                                      'write_requests_issued': str(wr_req),
                                      'bytes_written': str(wr_bytes),
                                      'number_of_errors': str(err)
                                    }
            runningStatus['disk'] = diskDict

            netDict = {}
            interfaceTypes = xml.getElementsByTagName('interface')
            count = 0
            for interfaceType in interfaceTypes:
                netname = 'eth' + str(count)
                count = count + 1
                ifaceDict = {}
                interfaceNodes = interfaceType.childNodes
                for interfaceNode in interfaceNodes:
                    if interfaceNode.nodeName[0:1] != '#':
                        for attr in interfaceNode.attributes.keys():
                            if interfaceNode.attributes[attr].name == 'address':
                                mac = str(interfaceNode.attributes[attr].value)
                                ifaceDict['mac'] = mac

                            if interfaceNode.attributes[attr].name == 'bridge':
                                bridge = str(interfaceNode.attributes[attr].value)
                                ifaceDict['bridge'] = bridge

                            if interfaceNode.attributes[attr].name == 'dev':
                                iface = str(interfaceNode.attributes[attr].value)

                                stats = dom.interfaceStats(iface)

                                ifaceDict['read_bytes'] = str(stats[0])
                                ifaceDict['read_packets'] = str(stats[1])
                                ifaceDict['read_errors'] = str(stats[2])
                                ifaceDict['read_drops'] = str(stats[3])
                                ifaceDict['write_bytes'] = str(stats[4])
                                ifaceDict['write_packets'] = str(stats[5])
                                ifaceDict['write_errors'] = str(stats[6])
                                ifaceDict['write_drops'] = str(stats[7])
                    netDict[netname] = ifaceDict
            runningStatus['net'] = netDict

            return runningStatus
#####################################################################################################

        rrdList = []
        domDict = {}
        domains = self.conn.listAllDomains(0)
        if len(domains) != 0:
            for domain in domains:
                status = domStatus(domain.name())
                domDict[domain.name()] = status

                if status['state'] == 'running':
                    mem = status.get('mem', None)
                    if mem:
                        #mem_actual = status['mem']['XXactual']
                        actual = status.get('mem').get('actual', 0)
                        available = status.get('mem').get('available', 0)
                        major_fault = status.get('mem').get('major_fault', 0)
                        minor_fault = status.get('mem').get('minor_fault', 0)
                        rss = status.get('mem').get('rss', 0)
                        swap_in = status.get('mem').get('swap_in', 0)
                        swap_out = status.get('mem').get('swap_out', 0)
                        unused = status.get('mem').get('unused', 0)

                        rrd_val = 'N:' + str(actual)
                        rrd_val += ':' + str(available)
                        rrd_val += ':' + str(major_fault)
                        rrd_val += ':' + str(minor_fault)
                        rrd_val += ':' + str(rss)
                        rrd_val += ':' + str(swap_in)
                        rrd_val += ':' + str(swap_out)
                        rrd_val += ':' + str(unused)
                        rrd = {'rrd': str(domain.name()) + '.mem', 'val': rrd_val}
                        rrdList.append(rrd)

#      "mem": {
#        "actual": "2097152", 
#        "available": "2044968", 
#        "major_fault": "0", 
#        "minor_fault": "0", 
#        "rss": "871248", 
#        "swap_in": "0", 
#        "swap_out": "0", 
#        "unused": "1930192"
#      }, 

#      "mem": {
#        "actual": "10485760", 
#        "rss": "10304984"
#      }, 

                    cpu = status.get('cpu', None)
                    if cpu:
                        count = status.get('cpu').get('count', 0)
                        cpu_time = status.get('cpu').get('cpu_time', 0)
                        system_time = status.get('cpu').get('system_time', 0)
                        user_time = status.get('cpu').get('suser_time', 0)

                        rrd_val = 'N:' + str(count)
                        rrd_val += ':' + str(cpu_time)
                        rrd_val += ':' + str(system_time)
                        rrd_val += ':' + str(user_time)
                        rrd = {'rrd': str(domain.name()) + '.cpu', 'val': rrd_val}
                        rrdList.append(rrd)

#      "cpu": {
#        "count": "1", 
#        "cpu_time": "3128286556798", 
#        "system_time": "736360000000", 
#        "user_time": "36310000000"
#      }, 


                    net = status.get('net', None)
                    if net:
                        for item in net:
                            #print(item) #eth0
                            read_bytes = status.get('net').get(item).get('read_bytes', 0)
                            read_drops = status.get('net').get(item).get('read_drops', 0)
                            read_errors = status.get('net').get(item).get('read_errors', 0)
                            read_packets = status.get('net').get(item).get('read_packets', 0)
                            write_bytes = status.get('net').get(item).get('write_bytes', 0)
                            write_drops = status.get('net').get(item).get('write_drops', 0)
                            write_errors = status.get('net').get(item).get('write_errors', 0)
                            write_packets = status.get('net').get(item).get('write_packets', 0)

                            rrd_val = 'N:' + str(read_bytes)
                            rrd_val += ':' + str(read_drops)
                            rrd_val += ':' + str(read_errors)
                            rrd_val += ':' + str(read_packets)
                            rrd_val += ':' + str(write_bytes)
                            rrd_val += ':' + str(write_drops)
                            rrd_val += ':' + str(write_errors)
                            rrd_val += ':' + str(write_packets)

                            rrd = {'rrd': str(domain.name()) + '.' + str(item), 'val': rrd_val}
                            rrdList.append(rrd)

#      "net": {
#        "eth0": {
#          "bridge": "br0", 
#          "mac": "52:54:00:a2:14:5b", 
#          "read_bytes": "74962610801", 
#          "read_drops": "0", 
#          "read_errors": "0", 
#          "read_packets": "46391059", 
#          "write_bytes": "51867066125", 
#          "write_drops": "0", 
#          "write_errors": "0", 
#          "write_packets": "38797256"
#        }
#      }, 

                      
                    disk = status.get('disk', None)
                    if disk:
                        for item in disk:
                            #print(item) #hda
                            bytes_read = status.get('disk').get(item).get('bytes_read', 0)
                            bytes_written = status.get('disk').get(item).get('bytes_written', 0)
                            read_requests_issued = status.get('disk').get(item).get('read_requests_issued', 0)
                            write_requests_issued = status.get('disk').get(item).get('write_requests_issued', 0)

                            rrd_val = 'N:' + str(bytes_read)
                            rrd_val += ':' + str(bytes_written)
                            rrd_val += ':' + str(read_requests_issued)
                            rrd_val += ':' + str(write_requests_issued)
                            
                            rrd = {'rrd': str(domain.name()) + '.' + str(item), 'val': rrd_val}
                            rrdList.append(rrd)

#      "disk": {
#        "hda": {
#          "bytes_read": "2884285952", 
#          "bytes_written": "14652522496", 
#          "device": "/data/prod-proxy/hda.qcow2", 
#          "number_of_errors": "-1", 
#          "read_requests_issued": "91544", 
#          "write_requests_issued": "498427"
#        }
#      }, 
      
                            



        runningDict['domains'] = domDict

        #rrd1 = {'rrd':'appserv-sturm.cpu', 'val': 'N:8:563909918600212:42132930000000:393180000000'}
        #rrd2 = {'rrd':'appserv-sturm.cpu', 'val': 'N:8:563909918600212:42132930000000:393180000000'}
        #runningDict['rrdata'] = [ rrd1, rrd2]

        #hypervisor_cpu
        #hypervisor_cpu_rrd = {'rrd':'hypervisor.cpu', 'val': 'N:' + str(hypervisor_cpu['count'])}

        #runningDict['rrdata'] = [ hypervisor_cpu_rrd, hypervisor_mem_rrd, rrdList ]

        #mergedList = hypervisor_cpu_rrd + hypervisor_mem_rrd + rrdList
        #runningDict['rrdata'] = [ mergedList ]

        #rrDict.extend(hypervisor_cpu_rrd)
        #rrDict.extend(hypervisor_mem_rrd)
        #rrDict.update(rrdList)

        #runningDict['rrdata'] = [ hypervisor_cpu_rrd, hypervisor_mem_rrd, rrDict ]
        rrdList.append(hypervisor_cpu_rrd)
        rrdList.append(hypervisor_mem_rrd)
        runningDict['rrdata'] =  rrdList 

        self.conn.close()
        return runningDict

if __name__ == "__main__":

    #uri = 'qemu+tcp://'
    uri = 'qemu://'
    host = ''
    runningDict = ListDomainsDetailedClass(uri, host).get()
    print json.dumps(runningDict, indent=2, sort_keys=True)



