
from flask import Flask
from flask import request
from flask import jsonify
import logging
import json

import config

app = Flask(__name__)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)

#app.logger.setLevel(logging.DEBUG)
#app.logger.debug('this will show in the log')

datadir = '/data/fim'
x_api_key_file = '/data/x-api-key.txt'

@app.route("/fim", methods=['GET','PUT','POST']) #fim?system_id=5e30c0b9890a7a4766268b59
def fim():

    headers_api_key = request.headers.getlist("x-api-key", None)
    headers_notify  = request.headers.getlist("x-notify", None)
    if not headers_api_key:
        return jsonify('{x-api-key:None}'), 200, {'Content-Type': 'application/json; charset=utf-8'}

    #x_api_key_file = '/data/fim/x-api-key.txt'
    api_key = ''.join(headers_api_key)
    found_api_key = False
    with open(x_api_key_file, 'r') as filehandle:
        filedata = filehandle.readlines()
        for line in filedata:
            if api_key in line:
                found_api_key = True

    if not found_api_key:
        return jsonify('{x-api-key:NotFound}'), 200, {'Content-Type': 'application/json; charset=utf-8'}

    system_id = request.args.get("system_id", None)
    if not system_id:
        return jsonify('{system_id:None}'), 200, {'Content-Type': 'application/json; charset=utf-8'}

    if request.method == 'GET':
        return get_request(system_id)
    elif request.method == 'PUT':
        return put_request(system_id)
    elif request.method == 'POST':
        if headers_notify:
            return notify_request(system_id)
        else:
            return post_request(system_id)
    else:
        return ''

def get_request(system_id):
    #headers_api_key = request.headers.getlist("x-api-key")
    system_id_file = datadir + '/' + str(system_id) + '.json'
    #jdata = open(system_id_file).read()
    #with open('/tmp/no.txt', 'r') as system_file:
    try:
        #with open('/tmp/no.txt', 'r') as system_file:
        with open(system_id_file, 'r') as system_file:
            jdata = system_file.read()
    except FileNotFoundError:
        jdata = '{"FileNotFoundError":"' + str(system_id_file) + '"}'
    return jdata

def put_request(system_id):
    system_id_file = datadir + '/' + str(system_id) + '.json'
    post = request.get_json()
    #app.logger.info(str(post))
    for k,v in post.items():
        #app.logger.info('k ' + k + ' v ' + v)
        _k = str(k)
        _v = str(v)

    with open(system_id_file, 'r') as jsonfile:
        jdata = json.load(jsonfile)

    #tmp = jdata[_k]
    jdata[_k] = _v

    with open(system_id_file, 'w+') as jsonfile:
        json.dump(jdata, jsonfile)

    return jsonify('{add:OK}'), 200, {'Content-Type': 'application/json; charset=utf-8'}

def post_request(system_id):
    system_id_file = datadir + '/' + str(system_id) + '.json'
    post = request.get_json()

    with open(system_id_file, 'w+') as jsonfile:
        json.dump(post, jsonfile)

    return jsonify('{post:OK}'), 200, {'Content-Type': 'application/json; charset=utf-8'}

def notify_request(system_id):
    post = request.get_json()
    receivers = list([config.ses['smtp_to']])
    subject = 'FIM: The following files changed for ' + str(system_id)
    message =  subject + '\r\n'
    message += json.dumps(post, sort_keys=False, indent=4)
    send_ses_email(receivers, subject, message)
    return jsonify('{notify:OK}'), 200, {'Content-Type': 'application/json; charset=utf-8'}


def send_ses_email(receivers, subject, message):
    import smtplib, ssl
    sender_email = config.ses['smtp_from']
    smtp_server  = config.ses['smtp_host']
    port         = config.ses['smtp_port']
    smtp_user    = config.ses['smtp_user']
    smtp_pass    = config.ses['smtp_pass']

    header =  ("From: %s\r\nTo: %s\r\n"
            % (sender_email, ",".join(receivers)))
    header += ("Subject: %s\r\n\r\n" % (subject))
    msg = header + message

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(smtp_user, smtp_pass)
        server.sendmail(sender_email, receivers, msg)
    print('emailto: ' + str(receivers))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

