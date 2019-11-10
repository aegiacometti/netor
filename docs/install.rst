Requirements
************
Read about this packages:

* setuptools
* tinydb
* ansible
* ansible network engine role
* saltstack (using the bootstrap installed, details below)
* salt-sproxy

How to install
**************

1. Update apt package list

    ``sudo apt-get update``

2. Install pip3 (we will use Python3)

    ``sudo apt-get install python3-pip``

3. Upgrade setuptools

    ``sudo pip3 install setuptools --upgrade``

4. Install SaltStack

The recommended way is to use the bootstrap

    ``wget -O bootstrap-salt.sh https://bootstrap.saltstack.com``
    ``sudo sh bootstrap-salt.sh  -x python3 -M``

For more information go to the project page, they have great documentation:

https://docs.saltstack.com/en/latest/topics/tutorials/walkthrough.html
https://docs.saltstack.com/en/latest/topics/tutorials/walkthrough_macosx.html

5. Install git

    ``sudo apt-get install git``

6. Clone ``netor`` project repository

Create a directory for the clone of the repository or do the clone directly at you home directory, this will be the
project home.

    ``git clone https://github.com/aegiacometti/netor.git``

7. Install some requirements

    ``sudo pip3 install -r *netor_home_directory*/requirements.txt``

8. Install Ansible network engine role

    ``ansible-galaxy install ansible-network.network-engine``

9. Copy Ansible configuration file

    ``sudo cp /etc/ansible/ansible.cfg $HOME``

10. Now, for the first time, you have to configure netor by manually executing the python script

    ``python3 *netor_home_directory*/netor/tinydb/scripts/netorconf.py``

In the future is you clone a new ``netor`` deployment for testing or to have 2 directory to work separately, you
will have to do this procedure again.

11. Copy SaltStack minion proxy to the systemd folder *(this could vary depending on the system)*

    ``sudo cp "netor_install_dir"/netor/salt/services/salt-proxy@.service /etc/systemd/system/``

12. Modify the SaltSatck start service, to add the custom configuration files directory

Usually located at: *(this could vary depending on the system)*

    file: ``/etc/systemd/system/multi-user.target.wants/salt-master.service``
    add: ``ExecStart=/usr/bin/salt-master *--config-dir=**[netor_home_directory]**/netor/salt/config/*``

    file: ``/etc/systemd/system/multi-user.target.wants/salt-minion.service``
    add: ``ExecStart=/usr/bin/salt-minion *--config-dir=**[netor_home_directory]**/netor/salt/config/*``

13. Add to your PATH environment the ``netor/bin`` directory for easy execute of scripts

    ``vi $HOME/.profile``

    add at the end ``PATH="$PATH:**[netor_home_directory]**/netor/bin/"``

14. Logoff the session and login again

15. done!

If everything worked fine you can view the commands with tab autocompletion

netor-db-list
netor-db-customer
...