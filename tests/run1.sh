
system_id=5e30c0b9890a7a4766268b59

#../src/jumpcloud/jumpcloud.py list-systems

#for i in json os os-version hostname serial insights state fde agent root-ssh
#do
#  ../src/jumpcloud/jumpcloud.py list-systems $i
#done

#../src/jumpcloud/jumpcloud.py list-systems-id

#for i in get-systems-json get-systems-remoteip get-systems-os get-systems-hostname get-systems-users get-systems-memberof
#do
#  ../src/jumpcloud/jumpcloud.py $i $system_id
#done

user_id=5de99ca25045a9513ca0dafa

#../src/jumpcloud/jumpcloud.py list-users

#for i in json suspended locked password-expired not-activated ldap-bind mfa
#do
#  ../src/jumpcloud/jumpcloud.py list-users $i
#done

#../src/jumpcloud/jumpcloud.py get-user-email $user_id

#../src/jumpcloud/jumpcloud.py list-system-bindings $user_id

group_id=''

../src/jumpcloud/jumpcloud.py list-usergroups




