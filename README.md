
jumpcloud - wrapper script around jcapiv1, jcapiv2, and console rest api

----
usage:

export JUMPCLOUD_API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

./jumpcloud.py

----

# setup/install...    

python3    
pip3 install urllib3    

----

```
pip install jumpcloud
```
https://pypi.org/project/jumpcloud

---

jumpcloud --help

Usage: jumpcloud option

    options:

      list_systems [json|os|os_version|hostname|serial|insights|state|fde|agent|root_ssh]
      list_systems_id
      get_systems_json [system_id]
      get_systems_remoteIP [system_id]
      add_systems_remoteIP_awsSG [system_id] [awsSG_id]
      get_systems_os system_id
      get_systems_hostname [system_id]
      get_systems_users [system_id]
      get_systems_memberof [system_id]
      delete_system [system_id]

      list_users [json|suspended|locked|password_expired|not_activated|ldap_bind|mfa]
      list_usergroups [json]
      list_usergroups_members [group_id]
      list_usergroups_details [group_id]
      list_systemgroups [json]
      list_systemgroups_membership [group_id]
      get_systemgroups_name [group_id]
      get_user_email [user_id]

      set_systems_memberof system_id group_id
      set_users_memberof user_id system_id
      set_users_memberof_admin user_id system_id
      del_users_memberof user_id system_id

      list_systeminsights_hardware [json|csv]
      systeminsights_os_version [system_id]
      get_systeminsights_system_info [system_id]

      list_systeminsights_apps [system_id]
      list_systeminsights_programs [system_id]

      systeminsights_apps [system_id]
      systeminsights_programs [system_id]

      get_app [bundle_name]
      get_program [name]

      systeminsights_browser_plugins
      systeminsights_firefox_addons

      list_system_bindings [user_id]
      list_user_bindings [system_id]

      list_commands [json]
      get_command [command_id] [associations|systems|systemgroups]
      mod_command [command_id] [add|remove] [system_id]

      trigger [name]

      list_command_results [command_id]
      delete_command_results [command_id]

      update_system [system_id] [key] [value]

      events [startDate] [endDate]
      Note: Dates must be formatted as RFC3339: "2020-01-15T16:20:01Z"


Version: 1.1.1


---

Some notes on this api...   


```
🎉 krink@Karls-MacBook-Pro jumpcloud % ./jumpcloud.py systeminsights_list_system_apps 5df3efcdf2d66c6f6a287136
[]
```
empty return [] means systeminsights is not enabled

----


### example 1
```
for i in `./jumpcloud.py list_systems_id`;do echo $i;./jumpcloud.py list_systeminsights_apps $i;done

for i in `./jumpcloud.py list_systems_id`;do echo $i;./jumpcloud.py list_systeminsights_programs $i;done
```

### example 2
```
for i in `./jumpcloud.py list_systems_id`;do ./jumpcloud.py get_systems_memberof $i;done
```

---

### example 3
JumpCloud triggers do not like under_scores or dashes either...
```
♒ krink@Karls-MacBook-Pro jumpcloud % ./jumpcloud.py list_commands
5e58586ff71cb16e21ca31ef fim.profile.host (linux) ["manual"]
5e586dfd4bd1666d649c319a fim.check (linux) ["trigger"]
♒ krink@Karls-MacBook-Pro jumpcloud % ./jumpcloud.py trigger fim.check
{"triggered":[]}
♒ krink@Karls-MacBook-Pro jumpcloud % ./jumpcloud.py list_commands
5e58586ff71cb16e21ca31ef fim.profile.host (linux) ["manual"]
5e586dfd4bd1666d649c319a fimcheck (linux) ["trigger"]
♒ krink@Karls-MacBook-Pro jumpcloud % ./jumpcloud.py trigger fimcheck
{"triggered":["fimcheck"]}
♒ krink@Karls-MacBook-Pro jumpcloud %
```

---

### example 4
Add a system to a trigger and run the trigger
```
♒ krink@Karls-MacBook-Pro jumpcloud % ./jumpcloud.py list_commands
5e58586ff71cb16e21ca31ef fim.profile.host (linux) ["manual"]
5e586dfd4bd1666d649c319a FIMcheck (linux) ["trigger"]
♒ krink@Karls-MacBook-Pro jumpcloud % ./jumpcloud.py get_command 5e586dfd4bd1666d649c319a associations
[]
♒ krink@Karls-MacBook-Pro jumpcloud % ./jumpcloud.py list_systems | grep sftp-
5e42f4885826553ee6383aa4 "sftp-us-west-1c" (sftp-us-west-1c) Amazon 2 x86_64
♒ krink@Karls-MacBook-Pro jumpcloud % ./jumpcloud.py mod_command 5e586dfd4bd1666d649c319a add 5e42f4885826553ee6383aa4
b'{"op": "add", "type": "system", "id": "5e42f4885826553ee6383aa4"}'
204

♒ krink@Karls-MacBook-Pro jumpcloud % ./jumpcloud.py get_command 5e586dfd4bd1666d649c319a associations
[
    {
        "attributes": null,
        "to": {
            "attributes": null,
            "id": "5e42f4885826553ee6383aa4",
            "type": "system"
        }
    }
]
♒ krink@Karls-MacBook-Pro jumpcloud % ./jumpcloud.py trigger FIMcheck
{"triggered":["FIMcheck"]}
♒ krink@Karls-MacBook-Pro jumpcloud %
```

/opt/jc/jcagent.conf
```
{"agentInstallDir":"/opt/jc/","agentLogDir":"/var/log/jcagent.log","agentServerGoPort":443,"agentServerHost":"agent.jumpcloud.com","agentServerPort":443,"automaticServiceAccountCreation":false,"caCrt":"/opt/jc/ca.crt","certuuid":"6ca1d31c01a045175810db7ec81169fa","clientCrt":"/opt/jc/client.crt","clientKey":"/opt/jc/client.key","heartbeatInterval":60000,"ipCheckUrl":"https://kickstart.jumpcloud.com/ip","osPlugin":"agent-darwin","passwordSyncEA":true,"returnCmdOutput":false,"systemKey":"5e30c0b9890a7a4766268b60","systemToken":"XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX","tls":true,"userMgmt":{"ldap_domain":"5cdc7f3c95a60d5c14488d5f.jumpcloud.com","local_ldap_auth_dn":"5e30c0b9890a7a4766268b59","local_ldap_bind_pwd":"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX","local_ldap_bind_uid":"5e30c0b9890a7a4766268b59","sshd_service":"ssh"}}
```



for i in $(./jumpcloud.py list_systems | grep Windows | awk '{print $1}')
do
 echo $i
 ./jumpcloud list_systeminsights_programs $i

done



