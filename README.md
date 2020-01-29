
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


