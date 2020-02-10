#!/usr/bin/env -S python3 -B

__version__ = '0004'

import sys, os, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import jumpcloud
import config
debug = True

def usage():
    print("""Usage: {0} [option]

    options:

        check app_offenses
        check username_policy
        check|send systems_root_ssh
        check|send fde

    """.format(sys.argv[0]))


#---------------------------------------------------------------------------
def get_fde():
    systems_fde_dict = {}
    jdata = jumpcloud.get_systems_json()
    for data in jdata['results']:
        system_id = data.get('_id')
        hostname  = data.get('hostname')
        fde_json = json.dumps(data.get('fde', 'Empty'), sort_keys=True)
        #systems_fde_dict[system_id] = '{"hostname":' + str(hostname) + '},' + str(fde_json)
        #systems_fde_dict[system_id] = str(fde_json)
        systems_fde_dict[system_id] = fde_json
    return systems_fde_dict

def fde_report_text():
    fde_dict = get_fde()
    report = ''

    systems_none = {}
    for system_id in fde_dict:
        if fde_dict[system_id] == '"Empty"':
        systems_none[system_id] = fde_dict[system_id]




    report += 'the followig sysytems are none \n'
    report += json.dumps(systems_none, sort_keys=True, indent=4)


    return report
    

def send_fde():
    offenders = check_fde()
    if len(offenders) == 0:
        print('No offenders: check_fde')
    else:
        #print('Send SES email...')
        receivers = list([config.ses['smtp_to']])
        subject = 'Compliance: Systems FDE (Full Disk Encryption)'
        message ="""The following systems FDE report
       
        {0}
        
        These systems are out of compliance.
        """.format(json.dumps(offenders, sort_keys=True, indent=4))
        send_ses_email(receivers, subject, message)


#---------------------------------------------------------------------------
def check_systems_root_ssh():
    systems_root_ssh_dict = {}
    jdata = jumpcloud.get_systems_json()
    for data in jdata['results']:
        system_id = data.get('_id')
        hostname  = data.get('hostname')
        root_ssh = json.dumps(data.get('allowSshRootLogin'), sort_keys=True)
        if root_ssh == 'true':
            systems_root_ssh_dict[system_id] = str(hostname)
    return systems_root_ssh_dict

def send_systems_root_ssh():
    offenders = check_systems_root_ssh()
    if len(offenders) == 0:
        print('No offenders: check_systems_root_ssh')
    else:
        #print('Send SES email...')
        receivers = list([config.ses['smtp_to']])
        subject = 'Compliance: Systems with allowSshRootLogin'
        message ="""The following systems allowSshRootLogin
       
        {0}
        
        These systems are out of compliance.
        """.format(json.dumps(offenders, sort_keys=True, indent=4))
        send_ses_email(receivers, subject, message)

#---------------------------------------------------------------------------
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

    #msg = 'Subject: ' + str(subject) + '\r\n'
    #msg += str(message) + '\r\n'

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(smtp_user, smtp_pass)
        server.sendmail(sender_email, receivers, msg)
    print('emailto: ' + str(receivers))
    print('message: ' + str(message))

def check_username_policy():
    pass


def check_app_offenses():

    #app = 'Slack'
    #jdata = jumpcloud.get_app(app)
    #for line in jdata:
    #    print(line['system_id'])

    #app_offenses = {}
    app_offenses = []
    for app in config.blacklistsoftware:
        if debug: print(app)
        jdata = jumpcloud.get_app(app)
        for line in jdata:
            #print(line['system_id'] + ' ' + line['name'])
            system_id = str(line['system_id'])
            app_offenses.extend([system_id, app])

    #print(app_offenses)
    systems_users_dict = {}

    for i in range(0, len(app_offenses), 2):
        system_id = app_offenses[i]
        app_name  = app_offenses[i + 1]
        if debug: print(str(system_id) + ' ' + str(app_name))

        
        #get_systems_users 5d9e267e546c544ad994f8cb
        systems_users_jdata  = jumpcloud.get_systems_users_json(system_id)
        if debug: print('----------------------------------------------------')
        if debug: print('systems_users_jdata ' + str(systems_users_jdata))
        if debug: print(str(type(systems_users_jdata)))
        if not systems_users_jdata:
            if debug: print('Empty ' + str(systems_users_jdata))
            systems_users_dict[system_id] = 'Empty'
        else:
            for line in systems_users_jdata:
                if debug: print('systems_users are... ' + str(line['id']))
                systems_users_dict[system_id] = str(line['id'])
        
        #for line in systems_users_jdata:
        #    print('systems_users ' + str(line['id']))
        #for line in systems_users_jdata:
        #    print('systems_users ' + str(line['id']))
        
    if debug: print(str(systems_users_dict))
    #{'5cf93ad2bd31ec75de452bcd': '5cdc8042aedcce77afcdb670', '5d9e267e546c544ad994f8cb': '5cdc7fad683a41781ec39845', '5e30c0b9890a7a4766268b59': '5de99ca25045a9513ca0dafa', '5d9e204c22874c28abece3a1': '5cdc8042d72cb377b72c5b36', '5ddda45d484f9c5b7ff5721c': 'Empty', '5ddda49b0c35306c77d09072': 'Empty', '5ddf112c2e34784cb7e24c41': '5cdc80416e59bc2c5bbe63ef', '5de97e3a82fdd020a161042b': 'Empty', '5de99b62fe8d195bababe9a3': 'Empty', '5df3efcdf2d66c6f6a287136': 'Empty'}

    systems_users_email_dict = {}
    for system_id, user_id in systems_users_dict.items():
        if debug: print(system_id, '->', user_id)
        if user_id == 'Empty':
            if debug: print(str(system_id) + ' is Empty')
            systems_users_email_dict[system_id] = 'Empty'
        else:
            #get_user_email 5cdc8042d72cb377b72c5b36
            user_email = jumpcloud.get_user_email(user_id)
            if debug: print(user_email)
            systems_users_email_dict[system_id] = user_email

    return systems_users_email_dict
        
    #5ddf112c2e34784cb7e24c41 Skype
    #systems_users_jdata [{'id': '5cdc80416e59bc2c5bbe63ef', 'type': 'user', 'compiledAttributes': {'sudo': {'withoutPassword': False, 'enabled': True}}, 'paths': [[{'attributes': {'sudo': {'withoutPassword': False, 'enabled': True}}, 'to': {'attributes': None, 'id': '5cdc80416e59bc2c5bbe63ef', 'type': 'user'}}]]}]
    #----------------------------------------------------
    #5de97e3a82fdd020a161042b Skype
    #systems_users_jdata []
    #----------------------------------------------------

if __name__ == "__main__":
    if sys.argv[1:]:
        if sys.argv[1] == "check" and sys.argv[2] == "app_offenses":
            offenders = check_app_offenses()
            #print(str(offenders))
            print(json.dumps(offenders, sort_keys=True, indent=4))
        elif sys.argv[1] == "check" and sys.argv[2] == "systems_root_ssh":
            offenders = check_systems_root_ssh()
            print(json.dumps(offenders, sort_keys=True, indent=4))
        elif sys.argv[1] == "send" and sys.argv[2] == "systems_root_ssh":
            offenders = send_systems_root_ssh()
        elif sys.argv[1] == "check" and sys.argv[2] == "fde":
            report = fde_report_text()
            print(report)


            #for system_id in report:
            #    if report[system_id] == '"Empty"':
            #        print('yes, Empty')
#
#                print(system_id + ' ' + report[system_id])
            #print(report)
            #systems = check_fde()
            #for system_id in systems:
            #    print(str(system_id) + ' ' + str(systems[system_id]))
        else:
            print('Unknown option')
    else:
        usage()

# check systems with root ssh
# check passwd for unauth users
# check group for sudoers

