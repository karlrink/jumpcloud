#!/usr/bin/env python2

__version__ = '003.1'

import sys
import json
import urllib2
import hashlib

def usage():
    print("""Usage: {0} [list|check|add|gen|post|notify]

        list
        check
        notify
        add /path/file
        gen /path/infile /path/out.json
        post /path/file.json

        check-threading
        check-multiprocessing
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

def check_file(_file,_val):
    with open(_file, 'r') as hashfile:
        hfile = hashfile.read()
        sha1 = hashlib.sha1(hfile).hexdigest()
        if _val != sha1:
            print(_file + ' CHANGED')
            return _file
    return None

def run_notify():
    jdata = {}
    jresponse = get_response()
    for _file,_val in jresponse.items():
        check = check_file(_file,_val)
        if check:
            jdata[_file] = 'CHANGED'

    if len(jdata) == 0:
        print('No Changes, thus no notice sent')
        return False

    system_id = get_system_id()
    fim_url = url + '?system_id=' + system_id
    request = urllib2.Request(fim_url)
    request.add_header('content-type','application/json')
    request.add_header('x-api-key',system_id)
    request.add_header('x-notify', 'True')
    post = json.dumps(jdata).encode('utf-8')
    response = urllib2.urlopen(request, post).read()
    print(response)
    return True

def run_check():
    jresponse = get_response()
    for _file,_val in jresponse.items():
        check = check_file(_file,_val)

def run_check_threading():
    import threading
    threads = list()
    jresponse = get_response()
    
    for k,v in jresponse.items():
        t = threading.Thread(target=check_file, args=(k,v))
        threads.append(t)
        t.start()

    for index, thread in enumerate(threads):
        thread.join()

def run_check_multiprocessing():
    import multiprocessing
    procs = list()
    jresponse = get_response()
   
    for k,v in jresponse.items():
        p = multiprocessing.Process(target=check_file, args=(k,v))
        procs.append(p)
        p.start()

    for index, proc in enumerate(procs):
        proc.join()


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
    with open(_file) as hashfile:
        hfile = hashfile.read()
        sha1 = hashlib.sha1(hfile).hexdigest()
        data = {_file : sha1}
    jdata = json.dumps(data).encode('utf-8')
    request = urllib2.Request(fim_url, data=jdata)
    request.get_method = lambda: 'PUT'
    request.add_header('content-type','application/json')
    request.add_header('x-api-key',system_id)
    response = urllib2.urlopen(request).read()
    print(response)

def create_json_file(_infile, _outfile):
    files_dict = {}
    with open(_infile, 'r') as filehandle:
        data = filehandle.read().splitlines()

    for line in data:
        with open(line, 'r') as hashfile:
            hfile = hashfile.read()
            sha1 = hashlib.sha1(hfile).hexdigest()
            files_dict[line] = sha1
            sys.stdout.write('.')
            sys.stdout.flush()

    with open(_outfile, 'w+') as outfile:
            json.dump(files_dict, outfile)
    print('\n' + _outfile)


def post_json_file(_file):
    with open(_file, 'r') as jsonfile:
        jdata = json.load(jsonfile)

    system_id = get_system_id()
    fim_url = url + '?system_id=' + system_id
    request = urllib2.Request(fim_url)
    request.add_header('content-type','application/json')
    request.add_header('x-api-key',system_id)
    post = json.dumps(jdata).encode('utf-8')
    response = urllib2.urlopen(request, post).read()
    print(response)

if __name__ == '__main__':
    if sys.argv[1:]:
        if sys.argv[1] == "list":
            print_list()
        elif sys.argv[1] == "check":
            run_check()
        elif sys.argv[1] == "notify":
            run_notify()
        elif sys.argv[1] == "check-threading":
            run_check_threading()
        elif sys.argv[1] == "check-multiprocessing":
            run_check_multiprocessing()
        elif sys.argv[2] and sys.argv[1] == "add":
            add_file(sys.argv[2])
        elif sys.argv[2] and sys.argv[1] == "post":
            post_json_file(sys.argv[2])
        elif sys.argv[3] and sys.argv[2] and sys.argv[1] == "gen":
            create_json_file(sys.argv[2], sys.argv[3])
        else:
            usage()
    else:
        usage()


