Scripts
=======

I will create some other netor-* scripts in order to make it easier to use them. Just as a mask, because at the end
you should know how to work directly with them.

Ansible is very easy and straight forward, but Salt is very hard to get use to the sintaxis.

* ``netor-config`` to configure neto_home_directory.
* ``netor-db-customers`` to operate on customer table.
* ``netor-db-devices`` to operate on dbdevices.
* ``netor-db-export`` to import a CSV file to the current DB (same as ``dblist -e``)
* ``netor-db-import`` to import a CSV file to the current DB.
* ``netor-db-list`` to list full BD or to export to .CSV if only the '-e' parameter is used.
* ``netor-db-push`` to push DB content to Ansible, Salt and bash scripts.
* ``netor-db-sites`` to operate on dbsites.
* ``netor-db-switch`` to switch DB in use in scripts.
* ``netor-ping`` to resolve name->ip using Ansible hosts inventory file.
* ``netor-salt-restart`` to restart Salt daemons.
* ``netor-salt-start`` to start Salt daemons.
* ``netor-salt-stop`` to stop Salt daemons.
* ``netor-traceroute`` to resolve name->ip using Ansible hosts inventory file.
* ``netor-salt-view-event-bus`` shortcut to execute native salt command to view event bus.
