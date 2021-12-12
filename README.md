# jumpcloud  

jumpcloud command for jumpcloud.com  

https://jumpcloud.com  
https://pypi.org/project/jumpcloud  
https://gitlab.com/krink/jumpcloud  

[![Package Version](https://img.shields.io/pypi/v/jumpcloud.svg)](https://pypi.python.org/pypi/jumpcloud/)  
[![Python Versions](https://img.shields.io/pypi/pyversions/pypistats.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/pypistats/)  

Run from source
```
./src/jumpcloud/jumpcloud.py
```

Install via pip
```
pip install jumpcloud
```

Run command
```
export JUMPCLOUD_API_KEY=XXXXXXXXXXX
jumpcloud --help
```

```
jumpcloud option
```

```
Usage: jumpcloud.py option 

    options:

      list-systems [json|os|os-version|hostname|serial|insights|state|fde|agent|root-ssh]
      list-systems-id
      get-systems-json [system_id]
      get-systems-remoteip [system_id]
      get-systems-os system_id
      get-systems-hostname [system_id]
      get-systems-users [system_id]
      get-systems-memberof [system_id]
      delete-system [system_id]

      list-users [json|suspended|locked|password-expired|not-activated|ldap-bind|mfa]
      get-user-email [user_id]

      list-usergroups [json]
      list-usergroups-members [group_id]
      list-usergroups-details [group_id]

      list-systemgroups [json]
      list-systemgroups-membership [group_id]
      get-systemgroups-name [group_id]

      set-systems-memberof system_id group_id
      set-users-memberof user_id system_id
      set-users-memberof_admin user_id system_id
      del-users-memberof user_id system_id

      list-systeminsights-hardware [json|csv]
      systeminsights-os-version [system_id]
      get-systeminsights-system-info [system_id]

      list-systeminsights-apps [system_id]
      list-systeminsights-programs [system_id]

      systeminsights-apps [system_id]
      systeminsights-programs [system_id]

      get-app [bundle_name]
      get-program [name]

      systeminsights-browser-plugins
      systeminsights-firefox-addons

      list-system-bindings [user_id]
      list-user-bindings [system_id]

      list-commands [json]
      get-command [command_id] [associations|systems|systemgroups]
      mod-command [command_id] [add|remove] [system_id]

      trigger [name]

      list-command-results [command_id]
      delete-command-results [command_id]

      update-system [system_id] [key] [value]

      add-systems-remoteip-awssg [system_id] [awssg_id] [port]

      events [startDate] [endDate]
      Note: Dates must be formatted as RFC3339: "2020-01-15T16:20:01Z"

Version: 2.0-🎄
```

---   

```
python3
>>> import jumpcloud
>>> jumpcloud.list_users()
```

