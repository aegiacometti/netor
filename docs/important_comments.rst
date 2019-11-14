Important comments
==================

There are a couple of security configuration settings from Ansible and SaltStack that are not recommended
to use, but for learning purposes I let them open.

For Ansible:
* $HOME/.ansible.cfg: host_key_checking = False
* $HOME/.ansible.cfg: host_key_auto_add = True

For SaltStack:

* /etc/salt/master and /etc/salt/minion
open_mode: True
auto_accept: True
