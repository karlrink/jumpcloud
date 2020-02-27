
```
Usage: ./fim.py [list|check|add|gen|post]

        list
        check
        add /path/file
        gen /path/infile /path/out.json
        post /path/file.json

        check-threading
        check-multiprocessing
    

```

Example
```
♒ karl.rink@Karl-MacBook-Pro fim % time sudo ./fim.py check          
/opt/jc/policies/VERSION CHANGED
/opt/jc/agent.db CHANGED
/opt/jc/policies/REVISION CHANGED
/opt/jc/policyConf.json CHANGED
/opt/jc/bin/sysadminkludge CHANGED
/opt/jc/bin/jumpcloud-agent CHANGED
/usr/local/lib/security/libpam_jcagent.so CHANGED
/opt/jc/bin/genpassword CHANGED
/opt/jc/jumpcloud-agent.pkg CHANGED
/opt/jc/version.txt CHANGED
/opt/jc/policies/whitelist.json CHANGED
/opt/jc/policies/jumpcloud-policies.tgz CHANGED
/opt/jc/bin/jccli CHANGED
sudo ./fim.py check  4.71s user 4.81s system 13% cpu 1:08.62 total
♒ karl.rink@Karl-MacBook-Pro fim % time sudo ./fim.py check-threading
/opt/jc/policies/VERSION CHANGED
/opt/jc/agent.db CHANGED
/opt/jc/policies/REVISION CHANGED
/opt/jc/policyConf.json CHANGED
/opt/jc/bin/sysadminkludge CHANGED
/opt/jc/bin/jumpcloud-agent CHANGED
/usr/local/lib/security/libpam_jcagent.so CHANGED
/opt/jc/bin/genpassword CHANGED
/opt/jc/jumpcloud-agent.pkg CHANGED
/opt/jc/version.txt CHANGED
/opt/jc/policies/whitelist.json CHANGED
/opt/jc/policies/jumpcloud-policies.tgz CHANGED
/opt/jc/bin/jccli CHANGED
sudo ./fim.py check-threading  15.68s user 11.60s system 70% cpu 38.428 total
♒ karl.rink@Karl-MacBook-Pro fim % time sudo ./fim.py check-multiprocessing
/opt/jc/policies/VERSION CHANGED
/opt/jc/agent.db CHANGED
/opt/jc/policies/REVISION CHANGED
/opt/jc/policyConf.json CHANGED
/opt/jc/bin/sysadminkludge CHANGED
/opt/jc/bin/jumpcloud-agent CHANGED
/usr/local/lib/security/libpam_jcagent.so CHANGED
/opt/jc/bin/genpassword CHANGED
/opt/jc/jumpcloud-agent.pkg CHANGED
/opt/jc/version.txt CHANGED
/opt/jc/policies/whitelist.json CHANGED
/opt/jc/policies/jumpcloud-policies.tgz CHANGED
/opt/jc/bin/jccli CHANGED
sudo ./fim.py check-multiprocessing  91.46s user 117.45s system 311% cpu 1:07.06 total
♒ karl.rink@Karl-MacBook-Pro fim % sudo ./fim.py list | wc -l
   47821
♒ karl.rink@Karl-MacBook-Pro fim %
```
---

Profile a system.  create a list of files
```
if [ `uname` == "Darwin" ]; then

  find /bin -type f
  find /usr -type f
  find /opt -type f

  find /private/etc -type f
  find /private/var/root -type f

  find /Library -type f
  find /System/Applications -type f
  find /System/Library -type f

fi


if [ `uname` == "Linux" ]; then
 
  find /boot/ -type f 
  find /bin/ -type f
  find /usr/ -type f
  find /etc/ -type f
  find /opt/ -type f
  find /root/ -type f

fi 
```

---

generate a json list of files with sha1

```
sudo ./fim.py gen mac.files.txt mac.files.txt.json
```

---

upload the json file (create new/over write)
```
sudo ./fim.py post mac.files.txt.json
```






