#!/usr/bin/env python2

__version__ = '001'

import sys
import json
import urllib2
import hashlib

def usage():
    print("""Usage: {0} [list|check|add]

        list
        check
        add /path/file
    """.format(sys.argv[0]))

url = 'https://monitor.nationsinfocorp.com:443/fim'

import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)): 
    ssl._create_default_https_context = ssl._create_unverified_context

def get_system_id():
    jcagent_conf = '/opt/jc/jcagent.conf'
    with open(jcagent_conf, 'r') as jcconf:
        jdata = json.load(jcconf)
    system_id = jdata['systemKey']
    return str(system_id)

def get_response():
    system_id = get_system_id()
    fim_url = url + '?system_id=' + system_id
    request = urllib2.Request(fim_url)
    request.add_header('content-type','application/json')
    request.add_header('x-api-key',system_id)

    response = urllib2.urlopen(request).read()
    jresponse = json.loads(response)
    return jresponse

def run_check():
    jresponse = get_response()
    for k,v in jresponse.items():
        #print(k, v)
        with open(k, 'r') as hashfile:
            hfile = hashfile.read()
            sha1 = hashlib.sha1(hfile).hexdigest()
            #print(sha1)
            if v != sha1:
                print(k + ' CHANGED')

def run_create():
    jresponse = get_response()
    count = len(jresponse)
    print('{')
    for k,v in jresponse.items():
        count -= 1
        with open(k, 'r') as hashfile:
            hfile = hashfile.read()
            sha1 = hashlib.sha1(hfile).hexdigest()
            if count:
                print('    "' + str(k) + '":"' + str(sha1) + '",')
            else:
                print('    "' + str(k) + '":"' + str(sha1) + '"')
    print('}')

def print_list():
    system_id = get_system_id()
    fim_url = url + '?system_id=' + system_id
    request = urllib2.Request(fim_url)
    request.add_header('content-type','application/json')
    request.add_header('x-api-key',system_id)
    jresponse = get_response()
    print(json.dumps(jresponse, sort_keys=False, indent=4))

def add_file(_file):
    system_id = get_system_id()
    fim_url = url + '?system_id=' + system_id
    request = urllib2.Request(fim_url)
    request.add_header('content-type','application/json')
    request.add_header('x-api-key',system_id)
    with open(_file) as hashfile:
        hfile = hashfile.read()
        sha1 = hashlib.sha1(hfile).hexdigest()
        data = {_file : sha1}
    post = json.dumps(data).encode('utf-8')
    response = urllib2.urlopen(request, post).read()
    print(response)

if __name__ == '__main__':
    if sys.argv[1:]:
        if sys.argv[1] == "list":
            print_list()
        elif sys.argv[1] == "check":
            run_check()
        elif sys.argv[2] and sys.argv[1] == "add":
            add_file(sys.argv[2])
        else:
            usage()
    else:
        usage()


