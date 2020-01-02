How to install
==============

Download the VM
***************

The easiest way is to use the VM from this link:

https://drive.google.com/open?id=14p02l8FkTLCYX_fkISyDAcEt-v7igCjU

With 2Gb of RAM, and 2 processor it should be OK.

userID: netor
password: password (change it! with ``passwd``)

Ansible do not require much power, is supper light, Salt is more less the same, except if you use Proxy Minions

The Salt proxy minion processes uses a little bit of power/memory.

I recommend you to read a little bit about Salt proxy minion, what they are and why they exist in the networking
environment. And later about **salt-sproxy**, a proxy-less approach. Follow Mircea Ulinic, this guy is a genius.


Linux bash installer
********************
This is a very simple copy&paste of the commands below in the format of a bash script.
Download it with in the directory you want to install Netor and it will create the home directory and install the
packages:

    ``wget https://raw.githubusercontent.com/aegiacometti/netor/master/bin/netor-install.sh``

    ``bash netor-install.sh``

Finally with root privileges add the following environment variable and restart the system.

    ```NETOR="/home/netor/netor/"```

Or follow the below instruction to go step by step with the commands.


Installation on Linux
*********************

**Requirements**

Read about these packages:

* setuptools
* python3
* tinydb
* ansible
* ansible network engine role
* salt (using the bootstrap installed, details below)
* salt-sproxy
* slack-client

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


9. Install Python Windows driver:

    ```sudo pip3 install "pywinrm>=0.3.0"```

10. Install Python Slack module:

    ```sudo pip3 install slackclient==1.3.2```

11. Download a base and clean ansible.cfg and copy it into your $HOME directory from GitHub:

    ``wget https://raw.githubusercontent.com/ansible/ansible/devel/examples/ansible.cfg -O $HOME/.ansible.cfg``


12. Now, for the first time, you have to configure netor by manually executing the python script:

    ``python3 [netor_home_directory]/netor/tinydb/scripts/netorconf.py``

In the future is you clone a new ``netor`` deployment for testing or to have 2 directories to work separately, you
will have to do this procedure again.


13. Add to your PATH environment the ``netor/bin`` directory for easy execution of scripts:

    ``vi $HOME/.profile``

and add at the end as an example ``PATH="$PATH:[netor_home_directory]/netor/bin/"``

14. Add the installation directory to the system environment:

    ```sudo vi /etc/environment```

Add the line at the end:

    ```NETOR="/home/adrian/netor-master/"```

15. Logoff session and login again:

If everything worked fine you can view the commands with tab autocomplete.

netor-db-list

netor-db-customer

etc

...


16. Install Salt:

The recommended way is to use the bootstrap:

    ``wget -O bootstrap-salt.sh https://bootstrap.Salt.com``

    ``sudo sh bootstrap-salt.sh -x python3 -M``

Now, Salt has a couple of bug which I corrected and ask to merge on the master repositories.
Since this could take a while to refresh, download these 2 files to replace them in your PC:

https://raw.githubusercontent.com/aegiacometti/salt/master/salt/runners/bgp.py
https://raw.githubusercontent.com/aegiacometti/salt/master/salt/runners/net.py

To find them on your PC use:

    ``sudo find /usr -name net.py``
    ``sudo find /usr -name bgp.py``

The ones under a directory called ``runners``

*For more information go to the project page, they have great documentation:*
https://docs.saltstack.com/en/latest/topics/tutorials/walkthrough.html
https://docs.saltstack.com/en/latest/topics/tutorials/walkthrough_macosx.html

Now, unlike Ansible, Salt uses daemons and the bootstrap add them to auto-start,
and we don't want that, we want to start them manually, just in case to not have them
running and searching for the devices when we don't want or when they are not even
reachable, as an example, if we are at home, another customer, or in a meeting!

In order to stop them and then disable them from auto-start we need to execute this
commands:

    ``netor-salt-stop``

    ``sudo systemctl disable salt-master.service``

    ``sudo systemctl disable salt-minion.service``

    ``netor-salt-start``


17. Copy Salt minion proxy to the systemd folder:

    ``sudo cp [netor_home_dir]/netor/salt/config/services/salt-proxy@.service /etc/systemd/system/``

*(this path could vary depending on the system)*


18. Backup the original Salt master and minion configuration files (so you can have
them as a reference), and create symbolic links to Salt new configuration files:

    ``sudo mv /etc/salt/master /etc/salt/master.bkp``

    ``sudo mv /etc/salt/minion /etc/salt/minion.bkp``

    ``sudo ln -s [netor_home_dir]/netor/salt/config/master /etc/salt/master``

    ``sudo ln -s [netor_home_dir]/netor/salt/config/minion /etc/salt/minion``

    ``sudo ln -s [netor_home_dir]/netor/salt/config/proxy /etc/salt/proxy``


19. Install salt-sproxy:

    ``sudo pip3 install salt-sproxy``


20. Run ``netor-db-push`` generate Ansible and Salt configuration files.


21. Restart Salt daemons:

    ``netor-salt-restart``


22. done!


Installation on MacOS
*********************

I have tested the software on Linux and Mac. I was able to install it on Mac.

Ansible works just fine, but Salt not so good, it is not officially supported, but since it is a kind of Unix,
in this case FreeBSD, it work, but not quiet well. So bellow you have the install procedure, but if want to go
for sure and you have a Mac, i would download the VM and after i know how Salt works, just then i would try
Salt on Mac directly.

**Requirements**

Read about this packages:

* xcode-select developer
* homebrew
* python3
* ansible network engine role
* saltstack
* salt-sproxy
* slack-client

**Installation**

1. Install xcode-select for command line developer tools:

    ``xcode-select --install``


2. Install Homebrew package manager:

    ``/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"``


3.- Install Python 3:

    ``brew install python3``


4. Install TinyDB:

    ``sudo pip3 install tinydb``

*For reference:*
https://tinydb.readthedocs.io/en/latest/getting-started.html


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


9. Install Python Windows driver:

    ```sudo pip3 install "pywinrm>=0.3.0"```


11. Install Python Slack module:

    ```sudo pip3 install slackclient==1.3.2```

12. Download a base and clean ansible.cfg and copy it into your $HOME directory from GitHub:

    ``curl https://raw.githubusercontent.com/ansible/ansible/devel/examples/ansible.cfg -o $HOME/.ansible.cfg``


13. Now, for the first time, you have to configure netor by manually executing the python script:

    ``python3 [netor_home_directory]/netor/tinydb/scripts/netorconf.py``

In the future is you clone a new ``netor`` deployment for testing or to have 2 directories to work separately, you
will have to do this procedure again.


14. Add to your PATH environment the ``netor/bin`` directory for easy execution of scripts:

    ``sudo nano /etc/paths``

and add at the end ``[netor_home_directory]/bin/``

If everything worked fine you can view the commands with tab autocomplete.

netor-db-list

netor-db-customer

etc

...


15. Install Salt:

    ``brew install saltstack``

Now, Salt has a couple of bug which I corrected and ask to merge on the master repositories.
Since this could take a while to refresh, download these 2 files to replace them in your PC:

https://raw.githubusercontent.com/aegiacometti/salt/master/salt/runners/bgp.py
https://raw.githubusercontent.com/aegiacometti/salt/master/salt/runners/net.py

To find them on your PC use:

    ``sudo find /usr -name net.py``
    ``sudo find /usr -name bgp.py``

The ones under a directory called ``runners``

*For more information go to the project page, they have great documentation:*
https://docs.saltstack.com/en/latest/topics/tutorials/walkthrough.html
https://docs.saltstack.com/en/latest/topics/tutorials/walkthrough_macosx.html

Now, we need to add the service files to launchd to be able to start the daemons:

    ``sudo cp [full_netor_home_dir]/netor/salt/config/services/com.saltstack.master.plist /Library/LaunchDaemons/``
    ``sudo cp [full_netor_home_dir]/netor/salt/config/services/com.saltstack.minion.plist /Library/LaunchDaemons/``

And we will start or stop or restart them with:

    ``netor-salt-start``
    ``netor-salt-stop``
    ``netor-salt-restart``

16. Verify ``maxfiles`` parameters at OS level:

    ``sudo launchctl limit``

If they are lower than 100000, you will need to change this. Usually happens on old MacOS versions.

    ``sudo cp [full_netor_home_dir]/netor/salt/config/services/limit.maxfiles.plist /Library/LaunchDaemons``

Adjust the values after the line ``maxfiles``, add it to the launchd.

    ``sudo launchctl load -w /Library/LaunchDaemons/limit.maxfiles.plist``

Restart the computer for this change to take effect.


17. Salt master and minion configuration files:

For your reference you can find clean samples at ``/user/local/etc/saltstack``

Create these links to use as defaults, these files will by the updated ones from Netor:

    ``sudo ln -s [full_netor_home_dir]/netor/salt/config/master /etc/salt/master``

    ``sudo ln -s [full_netor_home_dir]/netor/salt/config/minion /etc/salt/minion``

    ``sudo ln -s [full_netor_home_dir]/netor/salt/config/proxy /etc/salt/proxy``


18. Install salt-sproxy:

    ``sudo pip3 install salt-sproxy``


19. Run ``netor-db-push`` generate Ansible and Salt configuration files.


20. Restart Salt daemons:

    ``netor-salt-restart``


21. done!


Updates
*******

In order to update with the latest changes, just CD into your netor directory and pull the changes with:

    ``git pull origin master``
