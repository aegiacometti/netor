Bash scripts
============

Available BASH scripts to add to userID PATH in order to quick access python scripts

* ``netoconf`` to configure neto_home_directory.
* ``dblist`` to list full BD or to export to .CSV if only the '-e' parameter is used.
* ``dbexport`` to import a CSV file to the current DB (same as ``dblist -e``)
* ``dbimport`` to import a CSV file to the current DB.
* ``dbcustomers`` to operate on customer table.
* ``dbsites`` to operate on dbsites.
* ``dbdevices`` to operate on dbdevices.
* ``dbswitch`` to switch DB in use in scripts.
* ``dbpush`` to push DB content to Ansible, Salt and bash scripts.
* ``pingneto`` to resolve name->ip using Ansible hosts inventory file.
* ``tracerouteneto`` to resolve name->ip using Ansible hosts inventory file.

Motivation
**********

Simple learn about using BASH.

Limitations
***********
If you change you ``neto_home_directory`` you have to update the PATH environment variable in order to look for the scripts in the correct folder.
Another option is to modify the ``hosts_file`` variable in the script to redirect to the correct folder.
