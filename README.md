# Purpose of the project

This is a very simple compilation of several OpenSource packages, which by using scripts
aims to help integrating them to form a network platform to support networks, without
having to learn to configure all of them.
They scripts won't be nice, they are very simple as i learn Python, but they work fine,
in fact, they are very easy to read. They catch some typing errors, but pay attention
when you write. Anyway, do not worry, they won't break anything.

The tools that integrates at the moment are:

- Ansible
- SaltStack
- TinyDB

As i move forward i will try to integrate other packages and functionalities.

Project code at https://github.com/aegiacometti/netor

Project documentation at https://readthedocs.org/projects/netor/

## Motivation

After trying several network tools that claim to be essentials to networking, as you already
may know, there is no tool that will really work as you need, or even as they claim. They
may be useful for some tasks, but at some point i always ended quiting after hours of trying
and talking with the official support. Every tool is beautiful in the PPTs and demos, but
then when you deploy it the adventure starts.

Having real support from providers is so slow and even sometimes you don't have time to wait
and you do it by your own. (THIS TOOL WILL NOT BE DIFFERENT, but at least is fun to learn
and develop in an OpenSource environment) :)

A couple of years ago i started to learn Python and i love it, i used it to create a couple
of scripts that helped my a lot as support for several network related projects deployment.
Later on, i learnt about Ansible and it was "wow" i really love this!

In the path of learning network automation and orchestration with Ansible and SaltStack,
i found my self having to configure different files in different locations and in a
completely different manner. There are great tutorials on how to lear and use them, but
nothing to help you to integrate them.

Because to be honest, both Ansible and SaltStack are great. Ansible is simple to start using
it for simple things, but SaltStack from my point of view is incredible, has similar functions
and a lot of very cool capabilities.

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
* Ansible modify user configuration ./ansible/ and ./ansible.cfg
* After using "netorconf":  Modify ".ansible.cfg and Redirect Salt files (master, minion, proxy, etc) to new directory
 and restart SaltStack
* Work on bash scripts to mirror common Ansible and SaltStack operations in order to make it easier to use them and
 start learning about them

## Limitations

If you change you ``netor_home_directory`` you have to update the PATH environment variable
in order to look for the scripts in the correct folder.
Another option is to modify the ``hosts_file`` variable in the script to redirect to the
correct folder.

## Thank you notes

These passionate individuals that are always there to help, teach and gide us.

* NAPALM: David Barroso dbarrosop@dravetech.com, Mircea Ulinic ping@mirceaulinic.net and Kirk Byers ktbyers@twb-tech.com
* TinyDB: Markus Siemens markus@m-siemens.de
* OpenSource community in general
