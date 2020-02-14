
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


