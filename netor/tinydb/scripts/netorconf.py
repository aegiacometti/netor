#!/usr/bin/env python3

import os
import sys
import configparser
import fileinput
import tinydblogging


def netor_config():
    """
    It is used for updating the Neto home directory in the configuration files and scripts.

    This is useful, if you want to have 2 working installations of Neto in completely independent directories.

    It will update the ``NETOR_HOME_DIRECTORY`` variable in the ``netor.conf`` file,
    and also in the following Neto python scripts which then works with the TinyDB:
    # netor/tinydb/scripts/listdb.py
    # netor/tinydb/scripts/pushcustdb.py
    # netor/tinydb/scripts/worker.py
    # netor/tinydb/scripts/switchdb.py

    Later it will also update the ``hosts_file`` variable in the following bash scripts:
    # bin/netor-ping
    # bin/netor-traceroute

    :return: nothing
    """
    netor_home_directory = os.environ['HOME'] + "/netor"

    if os.path.isdir(netor_home_directory):
        answer = input("\nDefault \"$HOME/netor\" directory found, do you want to keep it (y/n): ").lower()
        if answer == "y":
            print("Keeping same configuration\n")
            sys.exit()
        elif answer == "n":
            new_netor_home_directory = input("Enter new Neto home directory (example: /full/path/netor/): ")
            if os.path.isdir(new_netor_home_directory):
                config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
                netor_config_path_name = new_netor_home_directory + "netor.config"
                config.read(netor_config_path_name)
                try:
                    config['Neto']['netor_home_directory'] = new_netor_home_directory
                except KeyError:
                    print("\nConfiguration files do no exist, clone the previous directory before start the changes\n")
                    sys.exit(1)
                with open(netor_config_path_name, 'w') as configfile:
                    config.write(configfile)
                tinydb_log_file = new_netor_home_directory + "netor/log/tinydb.log"
                update_config(tinydb_log_file, __file__, new_netor_home_directory)
            else:
                print("Invalid directory")
        else:
            print("Invalid option/n")
            sys.exit()
    else:
        print("\nDefault \"$HOME/netor\" NOT found")
        set_netor_home = input("Enter full path to /netor (example: /full/path/netor/): ")
        if os.path.isdir(set_netor_home) and os.path.isfile((set_netor_home + "netor/netor.config")):
            tinydb_log_file = set_netor_home + "netor/log/tinydb.log"
            update_config(tinydb_log_file, __file__, set_netor_home)
        else:
            print("\nInvalid directory or netor.config not found\n")
            sys.exit()


def update_config(tinydb_log_file, __file__, new_netor_home_directory):
    """
    Execute the actual updates in the files.

    :param tinydb_log_file: the filename to send the logging message after the operation is completed
    :param __file__: script name who is sending the message to log
    :param new_netor_home_directory: it is the actual new Neto home directory to be updated on files

    :return: nothing
    """
    replace_static_vars_scripts((new_netor_home_directory + "netor/tinydb/scripts/listdb.py"),
                                "NETOR_HOME_DIRECTORY = ", new_netor_home_directory)
    replace_static_vars_scripts((new_netor_home_directory + "netor/tinydb/scripts/pushcustdb.py"),
                                "NETOR_HOME_DIRECTORY = ", new_netor_home_directory)
    replace_static_vars_scripts((new_netor_home_directory + "netor/tinydb/scripts/worker.py"),
                                "NETOR_HOME_DIRECTORY = ", new_netor_home_directory)
    replace_static_vars_scripts((new_netor_home_directory + "netor/tinydb/scripts/switchdb.py"),
                                "NETOR_HOME_DIRECTORY = ", new_netor_home_directory)
    replace_static_vars_scripts((new_netor_home_directory + "netor/tinydb/scripts/importcsv.py"),
                                "NETOR_HOME_DIRECTORY = ", new_netor_home_directory)

    replace_static_vars_scripts((new_netor_home_directory + "bin/netor-ping"), "hosts_file=",
                                (new_netor_home_directory + "netor/ansible/hosts"))
    replace_static_vars_scripts((new_netor_home_directory + "bin/netor-traceroute"), "hosts_file=",
                                (new_netor_home_directory + "netor/ansible/hosts"))

    replace_static_vars_scripts((new_netor_home_directory + "bin/netor-db-customers"), "neto_home_directory=",
                                new_netor_home_directory)
    replace_static_vars_scripts((new_netor_home_directory + "bin/netor-db-devices"), "neto_home_directory=",
                                new_netor_home_directory)
    replace_static_vars_scripts((new_netor_home_directory + "bin/netor-db-export"), "neto_home_directory=",
                                new_netor_home_directory)
    replace_static_vars_scripts((new_netor_home_directory + "bin/netor-db-import"), "neto_home_directory=",
                                new_netor_home_directory)
    replace_static_vars_scripts((new_netor_home_directory + "bin/netor-db-list"), "neto_home_directory=",
                                new_netor_home_directory)
    replace_static_vars_scripts((new_netor_home_directory + "bin/netor-db-push"), "neto_home_directory=",
                                new_netor_home_directory)
    replace_static_vars_scripts((new_netor_home_directory + "bin/netor-db-sites"), "neto_home_directory=",
                                new_netor_home_directory)
    replace_static_vars_scripts((new_netor_home_directory + "bin/netor-db-switch"), "neto_home_directory=",
                                new_netor_home_directory)
    replace_static_vars_scripts((new_netor_home_directory + "bin/netor-config"), "neto_home_directory=",
                                new_netor_home_directory)

    replace_static_vars_scripts("/etc/systemd/system/multi-user.target.wants/salt-master.service", "--config-dir=",
                                (new_netor_home_directory + "netor/salt/config"))
    replace_static_vars_scripts("/etc/systemd/system/multi-user.target.wants/salt-minion.service", "--config-dir=",
                                (new_netor_home_directory + "netor/salt/config"))
    replace_static_vars_scripts("/etc/systemd/system/salt-proxy@.service", "--config-dir=",
                                (new_netor_home_directory + "netor/salt/config"))

    tinydblogging.log_msg(tinydb_log_file, __file__,
                          "Netconf executed. Neto.config and static vars in scripts updated. ")
    print("\nStatics vars in scripts replaced")
    print("\nYou can start using netor :)\n")


def replace_static_vars_scripts(filename, search, replace):
    """
    Replace line by line the ``NETOR_HOME_DIRECTORY`` static variable in scripts.

    :param filename: filename to review
    :param search: search pattern to look for
    :param replace: patter to replace

    :return: nothing
    """

    try:
        for line in fileinput.input(filename, inplace=True):
            if search in line:
                print((search + "\"" + replace + "\""), end="\n")
            else:
                print(line, end="")
    except FileNotFoundError:
        print("\nERROR File not found " + filename)
        print("Manually find systemd folder and file " + filename.split("/")[-1] +
              " and modify the --config-dir to point to " + replace + "\n")
    except PermissionError:
        print("\nERROR Permission denied to modify file " + filename)
        print("Manually modify the parameter --config-dir in the file to point to " + replace)


def check_netor_config(netor_home_directory):
    """
    Verifies if the ``netor.config`` file exists in the file tree.

    :param netor_home_directory: to verify if the netor home directory and file exists

    :return: nothing
    """
    if (os.path.isdir(netor_home_directory)) and (os.path.isfile((netor_home_directory + "netor/netor.config"))):
        return
    else:
        print("Neto home directory or config file not found.\nRun configuration script (netor-config).")
        sys.exit(1)


if __name__ == '__main__':
    netor_config()
    print()
