
system_id=5e30c0b9890a7a4766268b59
system_id2=605eb2d2ab90bb18714e2a5f

../src/jumpcloud/jumpcloud.py list-systems

for i in json os os-version hostname serial insights state fde agent root-ssh
do
  ../src/jumpcloud/jumpcloud.py list-systems $i
done

../src/jumpcloud/jumpcloud.py list-systems-id

for i in get-systems-json get-systems-remoteip get-systems-os get-systems-hostname get-systems-users get-systems-memberof
do
  ../src/jumpcloud/jumpcloud.py $i $system_id
done

../src/jumpcloud/jumpcloud.py list-users

user_id=5de99ca25045a9513ca0dafa

for i in json suspended locked password-expired not-activated ldap-bind mfa
do
  ../src/jumpcloud/jumpcloud.py list-users $i
done

../src/jumpcloud/jumpcloud.py get-user-email $user_id

../src/jumpcloud/jumpcloud.py list-system-bindings $user_id


../src/jumpcloud/jumpcloud.py list-usergroups

group_id=5e5ec19a45886d6c2067223f

for i in list-usergroups-members list-usergroups-details
do
  ../src/jumpcloud/jumpcloud.py $i $group_id
done

../src/jumpcloud/jumpcloud.py list-systemgroups

group_id=5e59921b232e115836375f63

for i in list-systemgroups-membership get-systemgroups-name
do
  ../src/jumpcloud/jumpcloud.py $i $group_id
done

../src/jumpcloud/jumpcloud.py systeminsights-browser-plugins

../src/jumpcloud/jumpcloud.py systeminsights-firefox-addons

../src/jumpcloud/jumpcloud.py list-system-bindings $user_id

../src/jumpcloud/jumpcloud.py list-user-bindings $system_id

../src/jumpcloud/jumpcloud.py list-commands

command_id=5f7f48839982a479a6f8efd7

../src/jumpcloud/jumpcloud.py get-command $command_id associations
../src/jumpcloud/jumpcloud.py get-command $command_id systems
../src/jumpcloud/jumpcloud.py get-command $command_id systemgroups

../src/jumpcloud/jumpcloud.py systeminsights-programs $system_id2


