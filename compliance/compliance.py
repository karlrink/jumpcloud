#!/usr/bin/env -S python3 -B

__version__ = '0005.3'

import sys, os, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import jumpcloud
import config
debug = True

def usage():
    print("""Usage: {0} [option]

    options:

        check|send systems_root_ssh
        check|send fde
        check|send systems_no_group

    """.format(sys.argv[0]))

        #check app_offenses
        #check username_policy

#---------------------------------------------------------------------------

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


    report += 'The followig systems are Compliant \n'
    report += json.dumps(systems_compliant, sort_keys=True, indent=4)
    report += '\r\n'

    report += 'The followig sysytems have FDE, but no recovery key \n'
    report += json.dumps(systems_active_nokey, sort_keys=True, indent=4)
    report += '\r\n'

    report += 'The followig sysytems are "Unconfigured" \n'
    report += json.dumps(systems_none, sort_keys=True, indent=4)
    report += '\r\n'

    return report
    

def send_fde():
    report = fde_report_text()
    if len(report) == 0:
        print('No report: fde_report_text')
        return False
    
    receivers = list([config.ses['smtp_to']])
    subject = 'Compliance: Systems FDE (Full Disk Encryption)'
    message = 'The following systems FDE report \r\n{0}\r\n'.format(report)
    message += """AICPA.org, Trust Services Criteria (TSC)
    Logical and Physical Access Controls
    CC6.1 - The entity implements logical access security software, infrastructure, and architectures 
    over protected information assets to protect them from security events to meet the entity's objectives.
      - Uses Encryption to Protect Data.  The entity uses encryption to supplement other measures used to protect data-at-rest, 
                                          when such protections are deemed appropriate based on assessed risk.
      - Protects Encryption Keys.  Processes are in place to protect encryption keys during generation, storage, use, and destruction.
    """
    send_ses_email(receivers, subject, message)
    return True


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
        return False
    receivers = list([config.ses['smtp_to']])
    subject = 'Compliance: Systems with allowSshRootLogin'
    message = 'The following systems allowSshRootLogin \r\n{0}\r\n'.format(json.dumps(offenders, sort_keys=True, indent=4))
    message += """AICPA.org, Trust Services Criteria (TSC)
    Logical and Physical Access Controls
    CC6.1 - The entity implements logical access security software, infrastructure, and architectures 
    over protected information assets to protect them from security events to meet the entity's objectives.
      - Identifies and Authenticates Users.  Persons, infrastructure and software are identified and authenticated 
                                             prior to accessing information assets, whether locally or remotely.
    """
    send_ses_email(receivers, subject, message)
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
            email = send_systems_root_ssh()
        elif sys.argv[1] == "check" and sys.argv[2] == "fde":
            report = fde_report_text()
            print(report)
        elif sys.argv[1] == "send" and sys.argv[2] == "fde":
            email = send_fde()
        elif sys.argv[1] == "check" and sys.argv[2] == "systems_no_group":
            report = systems_no_group_report_text()
            print(report)
        else:
            print('Unknown option')
    else:
        usage()

# check systems with root ssh
# check passwd for unauth users
# check group for sudoers

