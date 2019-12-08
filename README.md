# Introduction

You will see amazing things that can be done with Ansible and Salt and in the OpenSource
environment. The community out there is amazing... Enjoy!

Project code at <https://github.com/aegiacometti/netor>

Project documentation at <https://readthedocs.org/projects/netor/>


# Purpose of the project

This is a very simple compilation of several OpenSource packages, which
by using custom scripts help to start the journey of network
automation and orchestration, without having to learn from the very
beginning how to configure every detail, so i will be using basic standard
configurations.

Why? Because I believe that the most important factor in the adoption of
any new methodology is to make it easier to start using them.

The scripts won't be nice coding, they are very simple and they work fine,
in fact, they are very easy to read. They catch some typing errors but
pay attention when you write. Anyway, do not worry, you won't break
anything.

The tools that integrate at the moment are:

  - Ansible
  - Salt
  - TinyDB

As I move forward I will try to integrate other packages and
functionalities.

But, remember, this project is only to help start using Ansible and
Salt, in order to see what you can get out of them, and after that,
you should start learning about those two projects which are amazing.


## Motivation

https://netor.readthedocs.io/en/latest/introduction.html#motivation


# How to install

## Download a ready to use VirtualBox VM

https://netor.readthedocs.io/en/latest/how_to_install.html#virtualbox-vm


## Installation on Linux using the install script

https://netor.readthedocs.io/en/latest/how_to_install.html#linux-bash-installer


## Installation on Linux

https://netor.readthedocs.io/en/latest/how_to_install.html#installation-on-linux


## Installation on MacOS

https://netor.readthedocs.io/en/latest/how_to_install.html#installation-on-macos


## Updates

In order to update with the latest changes, just CD into your netor directory and pull the changes with:

    ``git pull origin master``


# Important comments

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


# How to use

## Functionalities

https://netor.readthedocs.io/en/latest/how_to_use.html#functionalities


## First Steps

https://netor.readthedocs.io/en/latest/how_to_use.html#first-steps


# Use cases (examples)

https://netor.readthedocs.io/en/latest/usecases.html


# TODOs

  - ADD ENCRYPTION TO STORE THE USER ID PASSWORD IN TINYDB
  - Redo netorconf.py.
  - Auto testing.
  - Upload to PyPi and work in adapting de structure.
  - Reformat code to make it reusable and with less repeated code.
  - Work on bash or python scripts to mirror common Ansible and
    Salt operations in order to make it easier to use and start
    learning about them Ansible and Salt.


# Limitations

  - Tested on Linux and macOS. Don't support Windows, since Ansible and
    Salt do not support them.
  - Only supports Python 3.
  - If you change you `netor_home_directory` you have to update the PATH
environment variable in order to look for the scripts in the correct
folder.


# Thank you notes

These passionate individuals that are always there to help, teach and
guide us.

  - Python3 for network engineers: with Kirk's online trainings I started this journey of 
    learning Python, with network orientation: Kirk Byers <ktbyers@twb-tech.com>
  - NAPALM: David Barroso <dbarrosop@dravetech.com>, Mircea Ulinic
    <ping@mirceaulinic.net>, and Kirk Byers <ktbyers@twb-tech.com>
  - TinyDB: Markus Siemens markus@m-siemens.de
  - The authors of these great books which helped my a lot:

    - Network Programmability and Automation (Jason Edelman, Scott S. Lowe and Matt Oswalt)
    - Network Automation at Scale (Mircea Ulinic and Seth House)
  - Ansible and Salt teams
  - OpenSource community in general
  