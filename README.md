# jumpcloud 

jumpcloud command for jumpcloud.com

https://gitlab.com/krink/jumpcloud

https://pypi.org/project/jumpcloud/

---

```
pip install jumpcloud
export JUMPCLOUD_API_KEY=XXXXXXXXXXX
jumpcloud --help
```

```
jumpcloud option

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
```


