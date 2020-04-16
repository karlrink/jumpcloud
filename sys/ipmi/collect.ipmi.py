#!/usr/bin/env python2

__version__ = '0000'

import sys
sys.dont_write_bytecode = True

import subprocess

import config
ipmi_user = config.param['ipmi_user']
ipmi_pass = config.param['ipmi_pass']

def collect_ipmi(host):

    collect='/usr/bin/ipmitool -I lanplus -U ' + ipmi_user + '  -P ' + ipmi_pass + ' -H ' + host + ' sdr'
    p = subprocess.Popen(collect, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, err = p.communicate()

    exit_code = p.wait()
    if (exit_code != 0):
        print('Error: ' + str(err) + ' ' + str(output))
        #return chronyc_data, chronyc_alert
        #return False
        sys.exit(exit_code)

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



    print(DDict)

if __name__ == "__main__":

    for host in config.hosts:
        #print(host)
        collect_ipmi(host)


    

