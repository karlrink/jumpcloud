#!/usr/bin/env python3

__version__ = '0007'

import sys, os, json
sys.dont_write_bytecode = True

import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import jumpcloud

def usage():
    print("""Usage: {0} [option]

    options:

        report|send systems_root_ssh
        report|send systems_fde
        report|send systems_no_group
        report|send users_mfa
        report|send users
        report|send systems

    """.format(sys.argv[0]))

        #check app_offenses
        #check username_policy

#---------------------------------------------------------------------------
debug = False

def systems_no_group_report_text():
    report = ''
    systems_no_group = {}

    all_system_id = jumpcloud.get_systems_id()
    for system_id in all_system_id:
        #print(system_id)
        jdata = jumpcloud.get_systems_memberof_json(system_id)
        if not jdata:
            hostname = jumpcloud.get_systems_hostname(system_id)
            systems_no_group[system_id] = hostname

    report += 'The followig systems are not identified \n'
    report += json.dumps(systems_no_group, sort_keys=True, indent=4)
    report += '\r\n'
    report += """AICPA.org, Trust Services Criteria (TSC)
    Logical and Physical Access Controls
    CC6.1 - The entity implements logical access security software, infrastructure, and architectures 
    over protected information assets to protect them from security events to meet the entity's objectives.
      - Identifies and Manages the Inventory of Information Assets. The entity identifies, inventories, classifies, and manages information assets.
    """
    return report

def send_systems_no_group():
    report = systems_no_group_report_text()
    if len(report) == 0:
        print('No report: systems_no_group_report_text')
        return False
    receivers = list([config.ses['smtp_to']])
    subject = 'Compliance: Systems Unidentified (no group assignment)'
    send_ses_email(receivers, subject, report)
    return True


#---------------------------------------------------------------------------
def get_fde():
    systems_fde_dict = {}
    jdata = jumpcloud.get_systems_json()
    for data in jdata['results']:
        system_id = data.get('_id')
        hostname  = data.get('hostname')
        fde_json = json.dumps(data.get('fde', 'None'), sort_keys=True)
        systems_fde_dict[system_id] = fde_json
    return systems_fde_dict

def fde_report_text():
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
            keyPresent = json.dumps(active_json.get('keyPresent', 'None'))

            if active == 'false':
                systems_active_false[system_id] = fde_dict[system_id]
                continue

            if active == 'true' and keyPresent == 'false':
                systems_active_nokey[system_id] = fde_dict[system_id]
                continue

            if active == 'true' and keyPresent == 'true':
                systems_compliant[system_id] = fde_dict[system_id]
                continue


    report += 'The followig systems have FDE with recovery key managment \n'
    report += json.dumps(systems_compliant, sort_keys=True, indent=4)
    report += '\r\n'

    report += 'The followig sysytems have FDE, but no recovery key \n'
    report += json.dumps(systems_active_nokey, sort_keys=True, indent=4)
    report += '\r\n'

    report += 'The followig sysytems are "Unconfigured" \n'
    report += json.dumps(systems_none, sort_keys=True, indent=4)
    report += '\r\n'

    report += """AICPA.org, Trust Services Criteria (TSC)
    Logical and Physical Access Controls
    CC6.1 - The entity implements logical access security software, infrastructure, and architectures
    over protected information assets to protect them from security events to meet the entity's objectives.
      - Uses Encryption to Protect Data.  The entity uses encryption to supplement other measures used to protect data-at-rest,
                                          when such protections are deemed appropriate based on assessed risk.
      - Protects Encryption Keys.  Processes are in place to protect encryption keys during generation, storage, use, and destruction.
    """
    return report
    

def send_fde():
    report = fde_report_text()
    if len(report) == 0:
        print('No report: fde_report_text')
        return False
    
    receivers = list([config.ses['smtp_to']])
    subject = 'Compliance: Systems FDE (Full Disk Encryption)'
    send_ses_email(receivers, subject, report)
    return True

#---------------------------------------------------------------------------

def get_users_mfa():
    users_mfa_dict = {}
    jdata = jumpcloud.get_systemusers_json()
    for data in jdata['results']:
        user_id = data.get('_id')
        email  = data.get('email')
        mfa_json = json.dumps(data.get('mfa', 'None'), sort_keys=True)
        users_mfa_dict[user_id] = mfa_json
    return users_mfa_dict


def mfa_report_text():
    report = ''
    jdata = jumpcloud.get_systemusers_json()

    report += 'The followig users have MFA/2FA configured \n\r'
    report += '{ \n'
    for data in jdata['results']:
        user_id = data.get('_id')
        email  = data.get('email')
        mfa_dict = data.get('mfa', 'None')
        configured = mfa_dict['configured']
        exclusion  = mfa_dict['exclusion']
        if str(configured) == 'True':
            report += '    ' + user_id + ' ' + email + ' (MFA:' + str(configured) + ')\n'
    report += '} \n'

    report += 'The followig users DO NOT have MFA/2FA \n\r'
    report += '{ \n'
    for data in jdata['results']:
        user_id = data.get('_id')
        email  = data.get('email')
        mfa_dict = data.get('mfa', 'None')
        configured = mfa_dict['configured']
        exclusion  = mfa_dict['exclusion']
        if str(configured) == 'False':
            report += '    ' + user_id + ' ' + email + ' (MFA:' + str(configured) + ')\n'
    report += '} \n'

    report += """AICPA.org, Trust Services Criteria (TSC)
    Common Criteria Related to Logical and Physical Access Controls
    CC5.1 - External access by personnel is permitted only through a two-factor (for example, a swipe card and a password)
            encrypted virtual private network (VPN) connection. 
    CC5.3 - Two-factor authentication and use of encrypted VPN channels help to ensure that only valid external users 
            gain remote and local access to IT system components.
    CC5.4 - When possible, formal role-based access controls to limit access to the system and infrastructure components 
            are created and enforced by the access control system. When it is not possible, authorized user IDs with two-factor authentication are used.

    Multi-Factor authentication (MFA) means you need more than one credential to login to systems, applications, or other digital assets.  
    MFA, or sometimes referred to as 2FA or Two Factor Authentication, generally requires one of the credentials to be 
    something you know – like your username and password – and the second credential to be 
    something that you have – such as a code sent to your smartphone. 
    """
    return report

def send_mfa():
    report = mfa_report_text()
    receivers = list([config.ses['smtp_to']])
    subject = 'Compliance: Users MFA/2FA status'
    send_ses_email(receivers, subject, report)
    return True


#---------------------------------------------------------------------------
def report_systems_root_ssh():
    report = 'The followig systems ALLOW Root SSH Login \n\r'

    systems_root_ssh_dict = {}
    jdata = jumpcloud.get_systems_json()
    for data in jdata['results']:
        system_id = data.get('_id')
        hostname  = data.get('hostname')
        root_ssh = json.dumps(data.get('allowSshRootLogin'), sort_keys=True)
        if root_ssh == 'true':
            systems_root_ssh_dict[system_id] = str(hostname)

    report += json.dumps(systems_root_ssh_dict, indent=4)
    report += '\n'
    report += """AICPA.org, Trust Services Criteria (TSC)
    Logical and Physical Access Controls
    CC6.1 - The entity implements logical access security software, infrastructure, and architectures 
    over protected information assets to protect them from security events to meet the entity's objectives.
      - Identifies and Authenticates Users.  Persons, infrastructure and software are identified and authenticated 
                                             prior to accessing information assets, whether locally or remotely.
    """
    return report


def send_systems_root_ssh():
    report = report_systems_root_ssh()
    receivers = list([config.ses['smtp_to']])
    subject = 'Compliance: Systems with allowSshRootLogin'
    send_ses_email(receivers, subject, report)
    return True


def systems_report():
    report = 'jumpcloud systems report. \n\r'
    jdata = jumpcloud.get_systems_json()
    totalCount = jdata['totalCount']
    report += '{\n'
    report += '    "Total Systems Count": ' + str(totalCount) + '\n'
    report += '}\n'

    report += 'The following Operating Systems counts  \n\r'
    osDict = jumpcloud.list_systems_os(_print=False)
    from collections import defaultdict
    dct = defaultdict(int)
    for k,v in osDict.items():
        dct[v] += 1

    report += json.dumps(dct, sort_keys=False, indent=4)
    return report

def send_systems_report():
    report = users_report()
    receivers = list([config.ses['smtp_to']])
    subject = 'Compliance: Jumpcloud SYSTEMS Report'
    send_ses_email(receivers, subject, report)
    return True


#---------------------------------------------------------------------------
def users_report():
    report = 'jumpcloud users report. \n\r'
    #totalCount
    jdata = jumpcloud.get_systemusers_json()
    #print(totalCount)
    totalCount = jdata['totalCount']
    report += '{\n'
    report += '    "Total Users Count": ' + str(totalCount) + '\n'
    report += '}\n'
    report += 'The following users are suspended \n\r'
    #report += str(jumpcloud.list_users_suspended())
    report += json.dumps(jumpcloud.list_users_suspended(_print=False), indent=4)
    report += '\nThe following users are locked \n\r'
    report += json.dumps(jumpcloud.list_users_locked(_print=False), indent=4)
    report += '\nThe following users are password_expired \n\r'
    report += json.dumps(jumpcloud.list_users_password_expired(_print=False), indent=4)
    report += '\nThe following users are not_activated \n\r'
    report += json.dumps(jumpcloud.list_users_not_activated(_print=False), indent=4)
    report += '\nThe following users are ldap_bind \n\r'
    report += json.dumps(jumpcloud.list_users_ldap_bind(_print=False), indent=4)
    report += '\n'
    #report += """AICPA.org, Trust Services Criteria (TSC)
    #Logical and Physical Access Controls
    #CC6.3 - The entity authorizes, modifies, or removes access to data, software, functions, and other protected information assets 
    #based on roles, responsibilities, or the system design and changes, giving consideration to the concepts of least privilege 
    #and segregation of duties, to meet the entity’s objectives.
    #  - Removes Access to Protected Information Assets.  Processes are in place to remove access to protected information assets
    #    when an individual no longer requires access.
    #"""
    return report

def send_users_report():
    report = users_report()
    receivers = list([config.ses['smtp_to']])
    subject = 'Compliance: Jumpcloud USERS Report'
    send_ses_email(receivers, subject, report)
    return True

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

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(smtp_user, smtp_pass)
        server.sendmail(sender_email, receivers, msg)
    print('emailto: ' + str(receivers))
    print('msg: ' + str(msg))
#---------------------------------------------------------------------------

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
        else:
            print('Unknown option')
    else:
        usage()

# check systems with root ssh
# check passwd for unauth users
# check group for sudoers

