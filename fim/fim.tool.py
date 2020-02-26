#!/usr/bin/env python2

import sys
sys.dont_write_bytecode = True

import hashlib
import json
import urllib2
import fim

def usage():
    print("""Usage: {0} create|post file
    """.format(sys.argv[0]))

def create_json_file(_file):
    files_dict = {}
    with open(_file, 'r') as filehandle:
        data = filehandle.read().splitlines()

    for line in data:
        with open(line, 'r') as hashfile:
            hfile = hashfile.read()
            sha1 = hashlib.sha1(hfile).hexdigest()
            files_dict[line] = sha1
            sys.stdout.write('.')
            sys.stdout.flush()

    jsonfile = str(_file) + '.json'
    with open(jsonfile, 'w') as outfile:
            json.dump(files_dict, outfile)
    print('\n' + jsonfile)


def post_json_file(_file):
    with open(_file, 'r') as jsonfile:
        jdata = json.load(jsonfile)

    system_id = fim.get_system_id()
    fim_url = fim.url + '?system_id=' + system_id
    request = urllib2.Request(fim_url)
    request.add_header('content-type','application/json')
    request.add_header('x-api-key',system_id)
    post = json.dumps(jdata).encode('utf-8')
    response = urllib2.urlopen(request, post).read()
    print(response)

if __name__ == '__main__':
    if sys.argv[1:]:
        if sys.argv[2] and sys.argv[1] == "create":
            create_json_file(sys.argv[2])
        elif sys.argv[2] and sys.argv[1] == "post":
            post_json_file(sys.argv[2])
        else:
            usage()
    else:
        usage()


