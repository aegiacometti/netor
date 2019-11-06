Purpose of the project
======================

This is a very simple compilation of several OpenSource packages, which by using scripts
aims to help integrating them to form a network platform to support networks, without
having to lear to configure all of them.
They scripts won't be nice, they are very simple as i learn Python, but they work fine,
in fact, they are very easy to read. They catch some typing errors, but pay attention
when you write. Anyway, do not worry, they won't break anything.

The tools that integrates at the moment are:

* Ansible
* SaltStack
* TinyDB

As i move forward i will try to integrate other packages and functionalities.

Requirements
************
Install and read about this packages:

* tinydb==3.15.0
* salt==2019.2.0
* salt-sproxy==2019.10.0
* ansible==2.8.6
* ntc-ansible==0.1.0``

How to install
**************

UNDER CONSTRUCTION
https://github.com/aegiacometti/neto

Add to the userID environment PATH, the folder with the BASH scripts. (Default ~/neto/scripts).

If you install the package in another directory or you change the NETO default directory,
you will need to update the environment PATH.


How to use / functionalities
****************************
TBD

Motivation
**********

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

TODOs
*****

* Add encryption to store the userID password in TinyDB.
* Ansible modify user configuration ./ansible/ and ./ansible.cfg
* After using "netoconf":  Modify ".ansible.cfg and Redirect Salt files (master, minion, proxy, etc) to new directory and restart SaltStack
* Work on bash scripts to mirror common Ansible and SaltStack operations in order to make it easier to use them and start learning about them

Limitations
***********
If you change you ``neto_home_directory`` you have to update the PATH environment variable
in order to look for the scripts in the correct folder.
Another option is to modify the ``hosts_file`` variable in the script to redirect to the
correct folder.

Thank you notes
***************
These passionate individuals that are always there to help.

* NAPALM: David Barroso, Mircea Ulinic and Kirk Byers
* TinyDB: Markus Siemens
* OpenSource community in general
