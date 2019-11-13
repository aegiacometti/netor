How to use / functionalities
============================

The following sections will contain a review of how to use the scripts.

All the scripts are located at the /bin directory of you netor install directory or home directory.

They are written in BASH (i just wanted to try BASH :) ), but in the future and in order to make it easier to start
 using Ansible ans SaltStack features, i will add some other scripts in python (so much easier :) ). And why adding
those script to use Ansible and SaltStack?   Because as you will see, lear the sintaxis of both is very very tedious
when you are just starting to learn about them.

The main idea is to have an inventory DB, and then use that inventory to configure the inventories of Ansible and SaltStack.
This would be useful because both configure their inventories in a complete different manner and files.

As an quick example, Ansible in its basic form uses a "hosts" file and that it (of course there are more advanced
ways for configuring its inventory), and SaltStack uses in its basic form uses several files, one top.sls and one
.sls file per each device. So, as you can imagine this setup will be tedious to start using both tools at the same time
to see what you can do in your learning journey.


How it works / First Steps
**************************

1. If you haven't done yet, run the script ``netor-config``for setting up you Netor home directory. And verify
that you have the $PATH environment variable set ``echo $PATH`` should show you your PATH to the Neto home directory.

You should be able to use tab autocomplete. Try writing netor- and the press tab.


2. Now try to look at what do you have in the DB with ``netor-db-list``. And where is located the filename of the DB.


3. You can try to list, add, edit and modify each of the DB tables (customers, sites and devices), by using the scripts
``netor-db-customers``, ``netor-db-sites`` and ``netor-db-devices``.


4. Once you have seen how it works, you can try to setup your own DB with ``netor-db-switch``, and start adding data to
it, always starting with customer -> site -> devices.

This script could be useful if you want to have different DBs for different purposes. Lets say, production and development,
site 1 and site 2, core switches and access switches, routers, firewalls, project 1 and project 2, etc etc etc....

Use any combination that is useful to what you have to do.


5. Now push your new DB to Ansible and SaltStack inventories with ``netor-db-push``.

When you do this the configuration files of Ansible and SaltStack will be completely replaced.

In this process you will be able to choose if you want to push the whole DB, or use a filter to chose with devices
you want to push, based on a RedEx expression. You will have to confirm so don't hesitate to play with the filer.

The push to Ansible will work right away, but for the push to SaltStack to take effect you will need to restart its
daemons with ``netor-salt-restart``

You also have available commands to stop and start SaltStack, with ``netor-salt-stop`` and ``netor-salt-start``.


6. Since you could have devices with the same name at different sites, or at different customer, the ``netor-db-push``
will generate hostnames bases on the join of the customer name, site name, and devices name. This will assure the
uniqueness of the hostname in Ansible and SaltStack.

And a very important feature is that you don't need to be able to resolve their FQDN names, because i very probable that
you or the customer don't have them on the DNS, and if they do, you could end up with conflicting names between customers
or sites.

So then next interesting step is using the commands ``netor-ping`` and ``netor-traceroute``. This two commands will run
using this new naming convention and without the need of have their names in your local machine hosts file or in a
external DNS.

Just remember, the netor hostname to use with this two commands, will be the conjunction of customer, site, and device
using an underscore "_".

Lets make it easy with an example:

``
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
``

7. At some point, you could want to import or export the DB to/from CSV format. The export could be useful to work with
the DB in another program, and then import it again, or if you go to a customer, just ask for the inventory to work with
in CSV format, and then import it to Netor.

The respectively commands are: ``netor-db-export`` and ``netor-db-import``.

Only take into consideration this format that you need to respect:

``
customer,site,dev_name,dev_ip,os,userid,passwd,salt_proxy_required
``


8.- That is it. Now start "playing" with Ansible and SaltStack. I will create some other netor-* scripts in order to
make it easier to use them. Just as a mask, because at the end you should know how to work directly with them.

Ansible is very easy and straight forward, but SaltStack is very hard to get use to the sintaxis.

