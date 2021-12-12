#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""jumpcloud: reports."""

from __future__ import absolute_import

__version__ = '20211212-0'

import sys
import os
import json
from collections import defaultdict
import smtplib
import ssl

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import jumpcloud
except ModuleNotFoundError as error:
    print('ModuleNotFoundError ' + str(error))
    sys.exit(1)

def usage():
    """self: usage."""
    print("Usage: " + sys.argv[0] + " [option]")
    print("""
    options:

        report|send systems_root_ssh
        report|send systems_fde
        report|send|set_default systems_no_group
        report|send users_mfa
        report|send users
        report|send systems

    """)
        #check app_offenses
        #check username_policy


#import config
config = dict(
  smtp_host = os.environ.get('SMTP_HOST', '127.0.0.1'),
  smtp_port = os.environ.get('SMTP_PORT', '25'),
  smtp_user = os.environ.get('SMTP_USER', ''),
  smtp_pass = os.environ.get('SMTP_PASS', ''),
  smtp_from = os.environ.get('SMTP_FROM', ''),
  smtp_to   = os.environ.get('SMTP_TO', '')
)

blacklistsoftware = [ 'Slack', 'Skype'
]


def systems_no_group_report_text():
    """systems_no_group_report_text: return str."""
    report = ''
    systems_no_group = {}

    all_system_id = jumpcloud.get_systems_id()
    for system_id in all_system_id:
        #print(system_id)
        jdata = jumpcloud.get_systems_memberof_json(system_id)
        if not jdata:
            hostname = jumpcloud.get_systems_hostname(system_id)
            systems_no_group[system_id] = hostname

    report += 'The following systems are not identified. systems_no_group \n'
    report += json.dumps(systems_no_group, sort_keys=True, indent=4)
    return report


def send_systems_no_group():
    """send_systems_no_group: return True."""
    report = systems_no_group_report_text()
    if len(report) == 0:
        print('No report: systems_no_group_report_text')
        return False
    receivers = list([config['smtp_to']])
    subject = 'Compliance: Systems Unidentified (no group assignment)'
    send_ses_email(receivers, subject, report)
    return True


def systems_no_group_set_default():
    """systems_no_group_set_default: return True."""
    systems_no_group = get_systems_no_group_osdct()
    for _k,_v in systems_no_group.items():
        #print(k,v)

        if _v.startswith('Windows'): #5e5d64fe45886d6c2066520c "Windows Systems"
            set_group = jumpcloud.set_systems_memberof(_k, '5e5d64fe45886d6c2066520c')
            print('set Windows Systems ' + str(_k))

        elif _v.startswith('Mac'): #5e59922a232e115836375f67 "Mac Systems"
            set_group = jumpcloud.set_systems_memberof(_k, '5e59922a232e115836375f67')
            print('set Mac Systems ' + str(_k))

        elif _v.startswith('Linux'): #5e59921b232e115836375f63 "Linux Systems"
            set_group = jumpcloud.set_systems_memberof(_k, '5e59921b232e115836375f63')
            print('set Linux Systems ' + str(_k))
        elif _v.startswith('Ubuntu'):
            set_group = jumpcloud.set_systems_memberof(_k, '5e59921b232e115836375f63')
            print('set Linux Systems Ubuntu ' + str(_k))
        elif _v.startswith('RedHat'):
            set_group = jumpcloud.set_systems_memberof(_k, '5e59921b232e115836375f63')
            print('set Linux Systems RedHat ' + str(_k))
        elif _v.startswith('Amazon'):
            set_group = jumpcloud.set_systems_memberof(_k, '5e59921b232e115836375f63')
            print('set Linux Systems Amazon ' + str(_k))

        else:
            set_group = None
            print('unknown os ' + str(_v))
    print(set_group)
    return True


def get_systems_no_group_osdct():
    """get_systems_no_group_osdct: return dict."""
    systems_no_group = {}
    all_system_id = jumpcloud.get_systems_id()
    for system_id in all_system_id:
        jdata = jumpcloud.get_systems_memberof_json(system_id)
        if not jdata:
            _os = jumpcloud.get_systems_os(system_id, _print=False)
            systems_no_group[system_id] = _os
    return systems_no_group


def get_fde():
    """get_fde: return dict."""
    systems_fde_dict = {}
    jdata = jumpcloud.get_systems_json()
    for data in jdata['results']:
        system_id = data.get('_id')
        #hostname  = data.get('hostname')
        fde_json = json.dumps(data.get('fde', 'None'), sort_keys=True)
        systems_fde_dict[system_id] = fde_json
    return systems_fde_dict


def fde_report_text():
    """fde_report_text: return str."""
    report = ''
    fde_dict = get_fde()

    systems_none = {}
    systems_active_false = {}
    systems_active_nokey = {}
    systems_compliant = {}

    for system_id in fde_dict:
        if fde_dict[system_id] == '"None"':
            systems_none[system_id] = fde_dict[system_id]
        else:
            active_json = json.loads(fde_dict[system_id])
            active = json.dumps(active_json.get('active', 'None'))
            keypresent = json.dumps(active_json.get('keyPresent', 'None'))

            if active == 'false':
                systems_active_false[system_id] = fde_dict[system_id]
                continue

            if active == 'true' and keypresent == 'false':
                systems_active_nokey[system_id] = fde_dict[system_id]
                continue

            if active == 'true' and keypresent == 'true':
                systems_compliant[system_id] = fde_dict[system_id]
                continue


    report += 'The following systems have FDE with recovery key managment \n'
    report += json.dumps(systems_compliant, sort_keys=True, indent=4)
    report += '\n'

    report += 'The following sysytems have FDE, but no recovery key \n'
    report += json.dumps(systems_active_nokey, sort_keys=True, indent=4)
    report += '\n'

    report += 'The following sysytems are "Unconfigured" \n'
    report += json.dumps(systems_none, sort_keys=True, indent=4)
    return report


def send_fde():
    """send_fde: return True."""
    report = fde_report_text()
    if len(report) == 0:
        print('No report: fde_report_text')
        return False
    receivers = list([config['smtp_to']])
    subject = 'Compliance: Systems FDE (Full Disk Encryption)'
    send_ses_email(receivers, subject, report)
    return True


def get_users_mfa():
    """get_users_mfa: return dict."""
    users_mfa_dict = {}
    jdata = jumpcloud.get_systemusers_json()
    for data in jdata['results']:
        user_id = data.get('_id')
        #email  = data.get('email')
        mfa_json = json.dumps(data.get('mfa', 'None'), sort_keys=True)
        users_mfa_dict[user_id] = mfa_json
    return users_mfa_dict


def mfa_report_text():
    """mfa_report_text: return str."""
    report = ''
    jdata = jumpcloud.get_systemusers_json()

    report += 'The following users have MFA/2FA configured \n'
    report += '{ \n'
    for data in jdata['results']:
        user_id = data.get('_id')
        email  = data.get('email')
        mfa_dict = data.get('mfa', 'None')
        configured = mfa_dict['configured']
        #exclusion  = mfa_dict['exclusion']
        if str(configured) == 'True':
            report += '    ' + user_id + ' ' + email + ' (MFA:' + str(configured) + ')\n'
    report += '} \n'

    report += 'The following users DO NOT have MFA/2FA \n'
    report += '{ \n'
    for data in jdata['results']:
        user_id = data.get('_id')
        email  = data.get('email')
        mfa_dict = data.get('mfa', 'None')
        configured = mfa_dict['configured']
        #exclusion  = mfa_dict['exclusion']
        if str(configured) == 'False':
            report += '    ' + user_id + ' ' + email + ' (MFA:' + str(configured) + ')\n'
    report += '}'
    return report


def send_mfa():
    """send_mfa: return True."""
    report = mfa_report_text()
    receivers = list([config['smtp_to']])
    subject = 'Compliance: Users MFA/2FA status'
    send_ses_email(receivers, subject, report)
    return True


def report_systems_root_ssh():
    """report_systems_root_ssh: return str."""
    systems_root_ssh_dict = {}
    jdata = jumpcloud.get_systems_json()
    for data in jdata['results']:
        system_id = data.get('_id')
        hostname  = data.get('hostname')
        root_ssh = json.dumps(data.get('allowSshRootLogin'), sort_keys=True)
        if root_ssh == 'true':
            systems_root_ssh_dict[system_id] = str(hostname)

    report = 'The following systems ALLOW Root SSH Login \n'
    report += json.dumps(systems_root_ssh_dict, indent=4)
    return report


def send_systems_root_ssh():
    """send_systems_root_ssh: return True."""
    report = report_systems_root_ssh()
    receivers = list([config['smtp_to']])
    subject = 'Compliance: Systems with allowSshRootLogin'
    send_ses_email(receivers, subject, report)
    return True


def systems_report():
    """systems_report: return str."""
    report = 'jumpcloud systems report. \n'
    jdata = jumpcloud.get_systems_json()
    totalcount = jdata['totalCount']
    report += '{\n'
    report += '    "Total Systems Count": ' + str(totalcount) + '\n'
    report += '}\n'

    report += 'The following Operating Systems counts  \n'
    osdict = jumpcloud.list_systems_os(_print=False)
    #from collections import defaultdict
    dct = defaultdict(int)
    #for k,v in osDict.items():
    for _v in osdict.values():
        dct[_v] += 1

    report += json.dumps(dct, sort_keys=False, indent=4)
    return report

def send_systems_report():
    """send_systems_report: return True."""
    report = systems_report()
    receivers = list([config['smtp_to']])
    subject = 'Compliance: Jumpcloud SYSTEMS Report'
    send_ses_email(receivers, subject, report)
    return True


def users_report():
    """users_report: return str."""
    report = 'jumpcloud users report. \n'
    #totalCount
    jdata = jumpcloud.get_systemusers_json()
    #print(totalCount)
    totalcount = jdata['totalCount']
    report += '{\n'
    report += '    "Total Users Count": ' + str(totalcount) + '\n'
    report += '}\n'
    report += 'The following users are suspended \n'
    #report += str(jumpcloud.list_users_suspended())
    report += json.dumps(jumpcloud.list_users_suspended(_print=False), indent=4)
    report += '\nThe following users are locked \n'
    report += json.dumps(jumpcloud.list_users_locked(_print=False), indent=4)
    report += '\nThe following users are password_expired \n'
    report += json.dumps(jumpcloud.list_users_password_expired(_print=False), indent=4)
    report += '\nThe following users are not_activated \n'
    report += json.dumps(jumpcloud.list_users_not_activated(_print=False), indent=4)
    report += '\nThe following users are ldap_bind \n'
    report += json.dumps(jumpcloud.list_users_ldap_bind(_print=False), indent=4)
    return report


def send_users_report():
    """send_users_report: return True."""
    report = users_report()
    receivers = list([config['smtp_to']])
    subject = 'Compliance: Jumpcloud USERS Report'
    send_ses_email(receivers, subject, report)
    return True


def send_ses_email(receivers, subject, message):
    """send_ses_email: return True."""
    sender_email = config['smtp_from']
    smtp_server  = config['smtp_host']
    port         = config['smtp_port']
    smtp_user    = config['smtp_user']
    smtp_pass    = config['smtp_pass']

    reciever_emails = ",".join(receivers)

    header = f"From: {sender_email}\r\nTo: {reciever_emails}\r\n"
    header += f"Subject: {subject}\r\n\r\n"
    msg = header + message

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(smtp_user, smtp_pass)
        server.sendmail(sender_email, receivers, msg)
    #print('emailto: ' + str(receivers))
    #print('msg: ' + str(msg))
    return True


def check_username_policy():
    """check_username_policy: not implemented."""
    pass


def check_app_offenses():
    """check_app_offenses: return dict."""
    #app = 'Slack'
    #jdata = jumpcloud.get_app(app)
    #for line in jdata:
    #    print(line['system_id'])

    #app_offenses = {}
    app_offenses = []
    for app in blacklistsoftware:
        jdata = jumpcloud.get_app(app)
        for line in jdata:
            #print(line['system_id'] + ' ' + line['name'])
            system_id = str(line['system_id'])
            app_offenses.extend([system_id, app])

    #print(app_offenses)
    systems_users_dict = {}

    for i in range(0, len(app_offenses), 2):
        system_id = app_offenses[i]
        #app_name  = app_offenses[i + 1]

        #get_systems_users 5d9e267e546c544ad994f8cb
        systems_users_jdata  = jumpcloud.get_systems_users_json(system_id)
        if not systems_users_jdata:
            systems_users_dict[system_id] = 'Empty'
        else:
            for line in systems_users_jdata:
                systems_users_dict[system_id] = str(line['id'])
        #for line in systems_users_jdata:
        #    print('systems_users ' + str(line['id']))
        #for line in systems_users_jdata:
        #    print('systems_users ' + str(line['id']))
    #{'5cf93ad2bd31ec75de452bcd': '5cdc8042aedcce77afcdb670', '5d9e267e546c544ad994f8cb':
    #'5cdc7fad683a41781ec39845', '5e30c0b9890a7a4766268b59': '5de99ca25045a9513ca0dafa',
    #'5d9e204c22874c28abece3a1': '5cdc8042d72cb377b72c5b36', '5ddda45d484f9c5b7ff5721c':
    #'Empty', '5ddda49b0c35306c77d09072': 'Empty', '5ddf112c2e34784cb7e24c41':
    #'5cdc80416e59bc2c5bbe63ef', '5de97e3a82fdd020a161042b': 'Empty', '5de99b62fe8d195bababe9a3':
    #'Empty', '5df3efcdf2d66c6f6a287136': 'Empty'}

    systems_users_email_dict = {}
    for system_id, user_id in systems_users_dict.items():
        if user_id == 'Empty':
            systems_users_email_dict[system_id] = 'Empty'
        else:
            #get_user_email 5cdc8042d72cb377b72c5b36
            user_email = jumpcloud.get_user_email(user_id)
            systems_users_email_dict[system_id] = user_email

    return systems_users_email_dict
    #5ddf112c2e34784cb7e24c41 Skype
    #systems_users_jdata [{'id': '5cdc80416e59bc2c5bbe63ef', 'type': 'user', 'compiledAttributes':
    #{'sudo': {'withoutPassword': False, 'enabled': True}}, 'paths': [[{'attributes': {'sudo':
    #{'withoutPassword': False, 'enabled': True}}, 'to': {'attributes': None, 'id':
    #'5cdc80416e59bc2c5bbe63ef', 'type': 'user'}}]]}]
    #----------------------------------------------------
    #5de97e3a82fdd020a161042b Skype
    #systems_users_jdata []
    #----------------------------------------------------


def main():
    """main: app."""
    if sys.argv[1:]:
        if sys.argv[1] == "report" and sys.argv[2] == "app_offenses":
            offenders = check_app_offenses()
            #print(str(offenders))
            print(json.dumps(offenders, sort_keys=True, indent=4))
        elif sys.argv[1] == "report" and sys.argv[2] == "systems_root_ssh":
            report = report_systems_root_ssh()
            #print(json.dumps(report, sort_keys=True, indent=4))
            print(report)
        elif sys.argv[1] == "send" and sys.argv[2] == "systems_root_ssh":
            email = send_systems_root_ssh()
            print(email)
        elif sys.argv[1] == "report" and sys.argv[2] == "systems_fde":
            report = fde_report_text()
            print(report)
        elif sys.argv[1] == "send" and sys.argv[2] == "systems_fde":
            email = send_fde()
        elif sys.argv[1] == "report" and sys.argv[2] == "users_mfa":
            report = mfa_report_text()
            print(report)
        elif sys.argv[1] == "send" and sys.argv[2] == "users_mfa":
            email = send_mfa()
        elif sys.argv[1] == "report" and sys.argv[2] == "users":
            report = users_report()
            print(report)
        elif sys.argv[1] == "send" and sys.argv[2] == "users":
            email = send_users_report()
        elif sys.argv[1] == "report" and sys.argv[2] == "systems":
            report = systems_report()
            print(report)
        elif sys.argv[1] == "send" and sys.argv[2] == "systems":
            email = send_systems_report()
        elif sys.argv[1] == "report" and sys.argv[2] == "systems_no_group":
            report = systems_no_group_report_text()
            print(report)
        elif sys.argv[1] == "send" and sys.argv[2] == "systems_no_group":
            email = send_systems_no_group()
        elif sys.argv[1] == "set_default" and sys.argv[2] == "systems_no_group":
            set_default = systems_no_group_set_default()
            print(set_default)
        else:
            print('Unknown option')
    else:
        usage()


# check systems with root ssh
# check passwd for unauth users
# check group for sudoers
if __name__ == '__main__':
    main()
