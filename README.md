# Introduction

Yes yes, i know... I'm very very original with the name of this project! ;)

Anyway, after +20 years in a network enterprise environment, i got tired of having to learn different command lines each
time a vendor decides to put something new on the market, and of course, management platforms that only work with
their devices, but the new ones! because the old one "you need to replace them"... you all know this story.

And don't get me wrong... I love to learn, in fact, if I am not learning something new, I behave like a kid who doesn't
have something to play with, for me this is a kind of work but with passion.

So, i decided to start "playing" with all of this new toys and in the way i found my self wanting to start a developing
path to integrate networking and coding worlds. I already kind of know about networking, ok, now let's go to the
developing/programming world with words like: Linux, Python, Pycharm, Ansible, SaltStack, event-bus, git, gitHub,
markdown, reStructuredText, auto-documentation, readTheDocs, TinyDB, Tox, Jenkins, Napalm, and every day two new toys...

This project aims to make it easier to play with the network, and excuse me if I offend someone, but since I enjoy this
so much, sometimes I like to use the work play instead of work. My objective is to use this compilation of tools
in a personal way, for your PC, for your use, nothing commercial nor enterprise.

You will see amazing things that can be done in the OpenSource environment without having to marry any vendor. The 
community out there is amazing... Enjoy!


# Purpose of the project

This is a very simple compilation of several OpenSource packages, which
by using scripts custom scripts help to start the journey of network
automation and orchestration, without having to learn from the very
beginning how to configure all of them.

Because I think that this is the most important thing in the adoption of
any new thing ... make it easier to start using them.

So, the scripts won't be nice, they are very simple and they work fine,
in fact, they are very easy to read. They catch some typing errors but
pay attention when you write. Anyway, do not worry, you won't break
anything at this point.

The tools that integrate at the moment are:

  - Ansible
  - SaltStack
  - TinyDB

As I move forward I will try to integrate other packages and
functionalities.

But, remember, this project is only to help start using Ansible and
SaltStack, in order to see what you can get out of them, and after that,
you should start learning about those two projects which are amazing.

Project code at <https://github.com/aegiacometti/netor>

Project documentation at <https://readthedocs.org/projects/netor/>


## Motivation

After trying several network tools that claim to be essentials to
networking, as you already may know, there is no tool that will really
work as you need, or even as they claim. They may be useful for some
tasks, but at some point, I always ended quitting after hours of trying
and talking with the official support. Every tool is beautiful in the
PPTs and demos, but then when you deploy it is when the adventure
starts.

Having real support from providers is so slow and even sometimes you
don't have time to wait and you do it on your own. (THIS TOOL WILL NOT
BE DIFFERENT, but at least is fun to learn and develop in an OpenSource
environment) :)

A couple of years ago I started to learn Python and I love it, I used it
to create a couple of scripts that helped me a lot to support several
network-related projects deployments.

Later on, I learned about Ansible and it was "wow" I really love this\!

In the path of learning network automation and orchestration with
Ansible and SaltStack, I found my self having to configure different
files in different locations and in a completely different manner. There
are great tutorials on how to lear and use them, but nothing to help you
to integrate them, in order to make it easier to start "playing".

Because to be honest, both Ansible and SaltStack are great. Ansible is
simple to start using it for simple things, but SaltStack from my point
of view is incredible, has similar functions and a lot of very cool
capabilities but it is very hard to start using it.

So, as I love to learn and to build things, I decided to start this
adventure of learning and develop a personal tool using Python, in an
OpenSource manner.


# How to install


## Installation on Linux


**Requirements**

Read about these packages:

  - setuptools
  - tinydb
  - ansible
  - ansible network engine role
  - saltstack (using the bootstrap installed, details below)
  - salt-sproxy


**Installation**

1.  Update apt package list:
    
    `sudo apt-get update`


2.  Install pip3 (we will use Python3):
    
    `sudo apt-get install python3-pip`


3.  Upgrade setuptools:
    
    `sudo pip3 install setuptools --upgrade`


4.  Install TinyDB:
    
    `sudo pip3 install tinydb`

*For reference:*
https://tinydb.readthedocs.io/en/latest/getting-started.html


5.  Install git:
    
    `sudo apt-get install git`


6.  Clone `netor` project repository:

Create a directory for the clone of the repository or do the clone
directly at you home directory, this will be the project home.

    `git clone https://github.com/aegiacometti/netor.git`


7. Install NAPALM:
    
    `sudo pip3 install napalm`

*For reference:*
https://napalm.readthedocs.io/en/latest/


8. Install Ansible:
    
    `sudo pip3 install ansible`
    
    `ansible-galaxy install ansible-network.network-engine`

*For more detail refer to installation guides at:*
https://docs.ansible.com/ansible/latest/installation\_guide/intro\_installation.html
https://galaxy.ansible.com/ansible-network/network-engine

9. Download a base and clean ansible.cfg and copy it into your $HOME
    directory from GitHub:
    
    `wget https://raw.githubusercontent.com/ansible/ansible/devel/examples/ansible.cfg -O $HOME/.ansible.cfg`


10.  Now, for the first time, you have to configure netor by manually
    executing the python script:
    
    `python3 [netor_home_directory]/netor/tinydb/scripts/netorconf.py`


In the future is you clone a new `netor` deployment for testing or to
have 2 directories to work separately, you will have to do this
procedure again.


11.  Add to your PATH environment the `netor/bin` directory for easy
    execute of scripts:
    
    `vi $HOME/.profile`
     
and add at the end `PATH="$PATH:$HOME/netor/bin/"`


12.  Logoff session and login again:

If everything worked fine you can view the commands with tab
autocompletion

netor-db-list

netor-db-customer

etc

...
    
    
13. Install SaltStack:

The recommended way is to use the bootstrap:

    `wget -O bootstrap-salt.sh https://bootstrap.saltstack.com`
    `sudo sh bootstrap-salt.sh -x python3 -M -g https://github.com/aegiacometti/salt.git git master`

As you can see, the bootstrap is pointing to a fork of mine from SaltStack's repo. I did this because I have fixed
of couple of lines of code, and I have requested the merge with the master branch of SaltStack, but since this could
take a while I prefer to offer something that works out of the box in these beginnings, instead of telling you which
files you have to manually modify. If you want just ask me I will give those file so you can install SaltStack from
it's true repo source.

On the other hand my repo could be loosing advancements of the community, but meanwhile i prefer something that works,
maybe there is way to install SaltStack and after update it with my corrected files, i don't know yet if it is possible.

*For more information go to the project page, they have great
documentation:*
https://docs.saltstack.com/en/latest/topics/tutorials/walkthrough.html
https://docs.saltstack.com/en/latest/topics/tutorials/walkthrough\_macosx.html

Now, unlike Ansible, SaltStack uses daemons and the bootstrap add them
to auto-start, and we don't want that, we want to start them manually,
just in case to not have them running and searching for the devices when
we don't want or when they are not even reachable, as an example, if we
are at home, another customer, or in a meeting\!

In order to stop them and then disable them from auto-start we need to execute this
commands:

    `netor-salt-stop`
    `sudo systemctl disable salt-master`
    `sudo systemctl disable salt-minion`


14. Copy SaltStack minion proxy to the systemd folder:
    
    `sudo cp
    [netor_home_dir]/netor/salt/config/services/salt-proxy@.service
    /etc/systemd/system/`

*(this path could vary depending on the system)*


15. Backup original SaltStack master and minion configuration files (so you can have
them as a reference), and create symbolic links to SaltStack new configuration files:

    `sudo mv /etc/salt/master /etc/salt/master.bkp`

    `sudo mv /etc/salt/minion /etc/salt/minion.bkp`

    `sudo ln -s [netor_home_dir]/netor/salt/config/master /etc/salt/master`

    `sudo ln -s [netor_home_dir]/netor/salt/config/minion /etc/salt/minion`

    `sudo ln -s [netor_home_dir]/netor/salt/config/proxy /etc/salt/proxy`


16. Run `netor-db-push` generate Ansible and SaltStack configuration
    files.


17. Restart SaltStack daemons:
    
    `netor-salt-restart`


18. done\!


# Installation on MacOS

**Requirements**

Read about these packages:

  - setuptools
  - tinydb
  - ansible
  - ansible network engine role
  - saltstack (using the bootstrap installed, details below)
  - salt-sproxy

**Installation**


# Important comments

There are a couple of security configuration settings from Ansible and SaltStack that are not recommended
to use, but for learning purposes I let them open.

For Ansible:
* $HOME/.ansible.cfg: host_key_checking = False
* $HOME/.ansible.cfg: host_key_auto_add = True

For SaltStack:

* /etc/salt/master and /etc/salt/minion
open_mode: True
auto_accept: True



# How to use

## Functionalities

The following sections will contain a review of how to use the scripts.

All the scripts are located at the /bin directory of your netor install
directory or home directory.

They are written in BASH (i just wanted to try BASH :) ), but in the
future and in order to make it easier to start using Ansible and
SaltStack features, I will add some other scripts in python (so much
easier :) ). And why adding those script to use Ansible and SaltStack?
Because as you will see, lear the syntaxis of both is very very tedious
when you are just starting to learn about them.

The main idea is to have an inventory DB, and then use that inventory to
configure the inventories of Ansible and SaltStack. This would be useful
because both configure their inventories in a completely different
manner and using several different files.

As a quick example, Ansible in its basic form uses a "hosts" file and
that it (of course there are more advanced ways for configuring its
inventory), and SaltStack uses in its basic form uses several files, one
top.sls and one .sls file per each device. So, as you can imagine this
setup will be tedious to start using both tools at the same time to see
what you can do in your learning journey.


## First Steps

1. If you haven't done yet, run the script `python3
[netor_home_directory]/netor/tinydb/scripts/netorconf.py`. And verify
that you have the $PATH environment variable set `echo $PATH` should
show you your PATH to the Neto home directory.

You should be able to use the tab autocomplete. Try writing netor- and
then press tab.

*(From now on you can use \`\`netor-config\`\`for setting a new Netor
home directory, since you should already have it in your $PATH)*


2. Now try to look at what do you have in the DB with `netor-db-list`.
    And where is located the filename of the DB.


3. You can try to list, add, edit and modify each of the DB tables
(customers, sites and devices), by using the scripts
`netor-db-customers`, `netor-db-sites` and `netor-db-devices`.


4. Once you have seen how it works, you can try to set up your own DB
with `netor-db-switch`, and start adding data to it, always starting
with customer -\> site -\> devices.

This script could be useful if you want to have different DBs for
different purposes. Let's say, production and development, site 1 and
site 2, core switches and access switches, routers, firewalls, project 1
and project 2, etc, etc, etc....

Use any combination that is useful to what you have to do.


5. Now push your new DB to Ansible and SaltStack inventories with
    `netor-db-push`.

When you do this the configuration files of Ansible and SaltStack will
be completely replaced.

In this process, you will be able to choose if you want to push the
whole DB, or use a filter to chose with devices you want to push, based
on a RedEx expression. You will have to confirm so don't hesitate to
play with the filer.

The push to Ansible will work right away, but for the push to SaltStack
to take effect you will need to restart its daemons with
`netor-salt-restart`

You also have available commands to stop and start SaltStack, with
`netor-salt-stop` and `netor-salt-start`.


6. Since you could have devices with the same name at different sites,
or at a different customer, the `netor-db-push` will generate hostnames
bases on the join of the customer name, site name, and device name. This
will assure the uniqueness of the hostname in Ansible and SaltStack.

And a very important feature is that you don't need to be able to
resolve their FQDN names because it is very probable that you or the
customer don't have them on the DNS, and if they do, you could end up
with conflicting names between customers or sites.

So then, the next interesting step is using the commands `netor-ping`
and `netor-traceroute`. This two commands will run using this new naming
convention and without the need of having their names in your local
machine hosts file or in a external DNS.

Just remember, the netor hostname to use with these two commands, will
be the conjunction of customer, site, and device using an underscore
"\_".

Let's make it easy with an example:

    nadrian@adrian-VirtualBox:~$ netor-db-list
    
    Using default DB File: /home/adrian/netor-master/netor/tinydb/data/db.json
    
    LIST DATABASE
    
    ...
    
    List Devices
    
    Customer Name          Site Name              Device Name          Device IP         Device OS   User Name            Password             Salt Proxy Req
    c1                     s1                     co-1                 10.100.12.2       ios         cisco                cisco                y
    c1                     s1                     cpe                  10.0.12.2         ios         cisco                cisco                y
    c1                     s1                     ua-1                 10.100.200.2      ios         cisco                cisco                y
    
    Full DB listed: /home/adrian/netor/netor/tinydb/data/db.json
    
    adrian@adrian-VirtualBox:~$ netor-ping c1_s1_cpe
    /home/adrian/netor-master/bin/netor-ping: line 8: 10.0.12.2: command not found
    PING 10.0.12.2 (10.0.12.2) 56(84) bytes of data.
    64 bytes from 10.0.12.2: icmp_seq=1 ttl=253 time=28.9 ms
    64 bytes from 10.0.12.2: icmp_seq=2 ttl=253 time=30.1 ms


7. At some point, you could want to import or export the DB to/from CSV
format. The export could be useful to work with the DB in another
program, and then import it again, or if you go to a customer, just ask
for the inventory to work with in CSV format, and then import it to
Netor.

The respectively commands are: `netor-db-export` and `netor-db-import`.

Only take into consideration this format that you need to respect:

    customer,site,dev_name,dev_ip,os,userid,passwd,salt_proxy_required


8. All the scripts log on screen and also on a logging file located at ``./netor/log``


9. That is it. Now start "playing" with Ansible and SaltStack.


# TODOs

  - ADD ENCRYPTION TO STORE THE USER ID PASSWORD IN TINYDB
  - Redo netorconf.py.
  - Auto testing.
  - Upload to PyPi and work in adapting de structure.
  - Reformat code to make it reusable and with less repeated code.
  - Work on bash or python scripts to mirror common Ansible and
    SaltStack operations in order to make it easier to use and start
    learning about them Ansible and SaltStack.


# Limitations

  - Tested on Linux and macOS. Don't support Windows, since Ansible and
    SaltStack do not support them.
  - Only supports Python 3.
  - If you change you `netor_home_directory` you have to update the PATH
environment variable in order to look for the scripts in the correct
folder.


# Thank you notes

These passionate individuals that are always there to help, teach and
guide us.

  - NAPALM: David Barroso <dbarrosop@dravetech.com>, Mircea Ulinic
    <ping@mirceaulinic.net>, and Kirk Byers <ktbyers@twb-tech.com>
  - TinyDB: Markus Siemens <markus@m-siemens.de>
  - Ansible and SaltStack teams
  - OpenSource community in general
  