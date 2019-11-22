Important comments
==================

Remember to create your own database and push it to Ansible and Salt, is super easy, follow the guide at **How to use** section.

All of this software is Open Source, which means that is free and community maintained.

There are a couple of security configuration settings from Ansible and Salt that are not recommended
to use, but for learning purposes I let them open.

**For Ansible:**

File $HOME/.ansible.cfg

``host_key_checking = False``

File $HOME/.ansible.cfg

``host_key_auto_add = True``


For Salt:

File /etc/salt/master and /etc/salt/minion

``open_mode: True``

``auto_accept: True``


When you restart Salt, give a couple of minutes to synchronise, it will
look like not working... wait... and if you want you can check the logs of the
daemons with:

``sudo tail -f /var/log/salt/*``
