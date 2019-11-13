# Purpose of the project

This is a very simple compilation of several OpenSource packages, which by using scripts 
custom scripts help to start the journey of network automation and orchestration, without
having to learn from the very beginning how to configure all of them.

The tools that integrates at the moment are:

- Ansible
- SaltStack
- TinyDB

As i move forward i will try to integrate other packages and functionalities.

They scripts won't be nice, they are very simple as i learn Python, but they work fine,
in fact, they are very easy to read. They catch some typing errors, but pay attention
when you write. Anyway, do not worry, they won't break anything.

But, remember, this project is only to help start using Ansible and SaltStack, in order
to see what you can get out of them, after you should start learning about those two
projects which are amazing.

Project code at https://github.com/aegiacometti/netor

Project documentation at https://readthedocs.org/projects/netor/


## Motivation

After trying several network tools that claim to be essentials to networking, as you already
may know, there is no tool that will really work as you need, or even as they claim. They
may be useful for some tasks, but at some point i always ended quiting after hours of trying
and talking with the official support. Every tool is beautiful in the PPTs and demos, but
then when you deploy it is when the adventure starts.

Having real support from providers is so slow and even sometimes you don't have time to wait
and you do it by your own. (THIS TOOL WILL NOT BE DIFFERENT, but at least is fun to learn
and develop in an OpenSource environment) :)

A couple of years ago i started to learn Python and i love it, i used it to create a couple
of scripts that helped my a lot to support several network related projects deployments.

Later on, i learnt about Ansible and it was "wow" i really love this!

In the path of learning network automation and orchestration with Ansible and SaltStack,
i found my self having to configure different files in different locations and in a
completely different manner. There are great tutorials on how to lear and use them, but
nothing to help you to integrate them, in order to make it easier to start "playing".

Because to be honest, both Ansible and SaltStack are great. Ansible is simple to start using
it for simple things, but SaltStack from my point of view is incredible, has similar functions
and a lot of very cool capabilities but it is very hard to start using it.

So, as i love to learn and to build things, i decided to start this adventure of learning
and develop a personal tool using Python, in an OpenSource manner.


## Requirements

Read about this packages:

* setuptools
* tinydb
* ansible
* ansible network engine role
* saltstack (using the bootstrap installed, details below)
* salt-sproxy


## How to install

1. Update apt package list

    ``sudo apt-get update``


2. Install pip3 (we will use Python3)

    ``sudo apt-get install python3-pip``


3. Upgrade setuptools

    ``sudo pip3 install setuptools --upgrade``


4. Install TinyDB

    ``sudo pip3 install -r [netor_home_directory]/requirements.txt``

    For reference:
    https://tinydb.readthedocs.io/en/latest/getting-started.html


5. Install Ansible

    ``sudo pip3 install ansible``

    ``ansible-galaxy install ansible-network.network-engine``

    For more detail refer to installation guides at:
    https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html


6. Download a sample ansible.cfg and copy it into your $HOME directory from github

    ``wget https://raw.githubusercontent.com/ansible/ansible/devel/examples/ansible.cfg -O $HOME/.ansible.cfg``


7. Install git

    ``sudo apt-get install git``


8. Clone ``netor`` project repository

    Create a directory for the clone of the repository or do the clone directly at you home directory, this will be the 
    project home.

    ``git clone https://github.com/aegiacometti/netor.git``


9. Now, for the first time, you have to configure netor by manually executing the python script

    ``python3 [netor_home_directory]/netor/tinydb/scripts/netorconf.py``


    In the future is you clone a new ``netor`` deployment for testing or to have 2 directory to work separately, you 
    will have to do this procedure again.


10. Install NAPALM

    ``sudo pip3 install napalm``


11. Install SaltStack

    The recommended way is to use the bootstrap

    ``wget -O bootstrap-salt.sh https://bootstrap.saltstack.com``

    ``sudo sh bootstrap-salt.sh -x python3 -M -g https://github.com/aegiacometti/salt.git git master``

    For more information go to the project page, they have great documentation:

    https://docs.saltstack.com/en/latest/topics/tutorials/walkthrough.html
    https://docs.saltstack.com/en/latest/topics/tutorials/walkthrough_macosx.html


12. Copy SaltStack minion proxy to the systemd folder *(this could vary depending on the system)*

    ``sudo cp [netor_home_dir]/netor/salt/config/services/salt-proxy@.service /etc/systemd/system/``


13. Create symbolic links to SaltStack new configuration files

    ``sudo ln -s [netor_home_dir]/netor/salt/config/master /etc/salt/master``

    ``sudo ln -s [netor_home_dir]/netor/salt/config/minion /etc/salt/minion``

    ``sudo ln -s [netor_home_dir]/netor/salt/config/proxy /etc/salt/proxy``


14. Run ``netor-db-push`` generate Ansible and SaltStack configuration files


15. Add to your PATH environment the ``netor/bin`` directory for easy execute of scripts

    ``vi $HOME/.profile``

    add at the end ``PATH="$PATH:[netor_home_directory]/netor/bin/"``


16. Logoff session and login again


17. Restart SaltStack daemons

    ``netor-salt-restart``


18. done!


If everything worked fine you can view the commands with tab autocompletion

netor-db-list

netor-db-customer

etc

...


## How to use / functionalities

TBD

* Imagine if you go to your customer and in 5 minutes you have all the information of the network
in order to be able to know where is each IP located.
* Or if you have to deploy some new configuration you take a backup in 2 minutes and start working
* etc


## TODOs

* Re do netorconf.py.
* Auto testing.
* Upload to PyPi and work in adapting de structure.
* Reformat code to make it reusable and with less repeated code.
* Add encryption to store the userID password in TinyDB.
* Work on bash or python scripts to mirror common Ansible and SaltStack operations in order to make it
 easier to use and start learning about them Ansible and SaltStack.


## Limitations

* Only tested on Linux.
* If you change you ``netor_home_directory`` you have to update the PATH environment variable
in order to look for the scripts in the correct folder.


## Thank you notes

These passionate individuals that are always there to help, teach and gide us.

* NAPALM: David Barroso dbarrosop@dravetech.com, Mircea Ulinic ping@mirceaulinic.net and Kirk Byers ktbyers@twb-tech.com
* TinyDB: Markus Siemens markus@m-siemens.de
* OpenSource community in general
