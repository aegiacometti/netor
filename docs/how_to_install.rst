How to install
==============


Installation on Linux
*********************

**Requirements**

Read about these packages:

* setuptools
* tinydb
* ansible
* ansible network engine role
* saltstack (using the bootstrap installed, details below)
* salt-sproxy

**Installation**

1. Update apt package list:

    ``sudo apt-get update``


2. Install pip3 (we will use Python3):

    ``sudo apt-get install python3-pip``


3. Upgrade setuptools:

    ``sudo pip3 install setuptools --upgrade``


4. Install TinyDB:

    ``sudo pip3 install tinydb``

*For reference:*
https://tinydb.readthedocs.io/en/latest/getting-started.html


5. Install git:

    ``sudo apt-get install git``


6. Clone ``netor`` project repository:

Create a directory for the clone of the repository or do the clone directly at you home directory, this will be the
project home:

    ``git clone https://github.com/aegiacometti/netor.git``


7. Install NAPALM:

    ``sudo pip3 install napalm``

*For reference:*
https://napalm.readthedocs.io/en/latest/


8. Install Ansible:

    ``sudo pip3 install ansible``

    ``ansible-galaxy install ansible-network.network-engine``

*For more detail refer to installation guides at:*
https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html
https://galaxy.ansible.com/ansible-network/network-engine


9. Download a base and clean ansible.cfg and copy it into your $HOME directory from GitHub:

    ``wget https://raw.githubusercontent.com/ansible/ansible/devel/examples/ansible.cfg -O $HOME/.ansible.cfg``


10. Now, for the first time, you have to configure netor by manually executing the python script:

    ``python3 [netor_home_directory]/netor/tinydb/scripts/netorconf.py``

In the future is you clone a new ``netor`` deployment for testing or to have 2 directories to work separately, you
will have to do this procedure again.


11. Add to your PATH environment the ``netor/bin`` directory for easy execute of scripts:

    ``vi $HOME/.profile``

and add at the end ``PATH="$PATH:$HOME/netor/bin/"``


12. Logoff session and login again:

If everything worked fine you can view the commands with tab autocomplete.

netor-db-list

netor-db-customer

etc

...


13. Install SaltStack:

The recommended way is to use the bootstrap:

    ``wget -O bootstrap-salt.sh https://bootstrap.saltstack.com``

    ``sudo sh bootstrap-salt.sh -x python3 -M -g https://github.com/aegiacometti/salt.git git master``

As you can see, the bootstrap is pointing to a fork of mine from SaltStack's repo. I did this because I have fixed
of couple of lines of code, and I have requested the merge with the master branch of SaltStack, but since this could
take a while I prefer to offer something that works out of the box in these beginnings, instead of telling you which
files you have to manually modify. If you want just ask me I will give those file so you can install SaltStack from
it's true repo source.

On the other hand my repo could be loosing advancements of the community, but meanwhile i prefer something that works,
maybe there is way to install SaltStack and after update it with my corrected files, i don't know yet if it is possible.

*For more information go to the project page, they have great documentation:*
https://docs.saltstack.com/en/latest/topics/tutorials/walkthrough.html
https://docs.saltstack.com/en/latest/topics/tutorials/walkthrough_macosx.html

Now, unlike Ansible, SaltStack uses daemons and the bootstrap add them to auto-start,
and we don't want that, we want to start them manually, just in case to not have them
running and searching for the devices when we don't want or when they are not even
reachable, as an example, if we are at home, another customer, or in a meeting!

In order to stop them and then disable them from auto-start we need to execute this
commands:

    ``netor-salt-stop``
    ``sudo systemctl disable salt-master``
    ``sudo systemctl disable salt-minion``


14. Copy SaltStack minion proxy to the systemd folder:

    ``sudo cp [netor_home_dir]/netor/salt/config/services/salt-proxy@.service /etc/systemd/system/``

*(this path could vary depending on the system)*


15. Backup original SaltStack master and minion configuration files (so you can have
them as a reference), and create symbolic links to SaltStack new configuration files:

    ``sudo mv /etc/salt/master /etc/salt/master.bkp``

    ``sudo mv /etc/salt/minion /etc/salt/minion.bkp``

    ``sudo ln -s [netor_home_dir]/netor/salt/config/master /etc/salt/master``

    ``sudo ln -s [netor_home_dir]/netor/salt/config/minion /etc/salt/minion``

    ``sudo ln -s [netor_home_dir]/netor/salt/config/proxy /etc/salt/proxy``


16. Run ``netor-db-push`` generate Ansible and SaltStack configuration files.


17. Restart SaltStack daemons:

    ``netor-salt-restart``


18. done!


Installation on MacOS
*********************

**Requirements**

Read about this packages:

* setuptools
* tinydb
* ansible
* ansible network engine role
* saltstack (using the bootstrap installed, details below)
* salt-sproxy

**Installation**