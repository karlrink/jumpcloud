
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

Some notes on this api...   


```
🎉 krink@Karls-MacBook-Pro jumpcloud % ./jumpcloud.py systeminsights_list_system_apps 5df3efcdf2d66c6f6a287136
[]
```
empty return [] means systeminsights is not enabled

----


### example 1
```
for i in `./jumpcloud.py list_systems_id 'Mac OS X'`;do echo $i;./jumpcloud.py list_systeminsights_apps $i;done

for i in `./jumpcloud.py list_systems_id Windows`;do echo $i;./jumpcloud.py list_systeminsights_programs $i;done
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



