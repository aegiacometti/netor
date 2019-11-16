Important comments
==================

All of this software is Open Source, which means that is free and community maintained.

You don't need to pay a fortune for a vendor specify software, which are usually oriented to their OS and the you
have to figure out what to do with other devices from other vendors. We all know the drill...

There are a couple of security configuration settings from Ansible and SaltStack that are not recommended
to use, but for learning purposes I let them open.

For Ansible:
* $HOME/.ansible.cfg: host_key_checking = False
* $HOME/.ansible.cfg: host_key_auto_add = True

For SaltStack:

* /etc/salt/master and /etc/salt/minion

open_mode: True
auto_accept: True

When you restart SaltStack, give a couple of minutes to synchronise, it will
look like not working... wait... and if you want you can check the logs of the
daemons with:

``sudo tail -f /var/log/salt/*``
