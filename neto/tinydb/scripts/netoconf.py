#!/usr/bin/env python3

import os
import sys
import configparser
import fileinput
import tinydblogging


def neto_config():
    """
    It is used for updating the Neto home directory in the configuration files and scripts.

    This is useful, if you want to have 2 working installations of Neto in completely independent directories.

    It will update the ``NETO_HOME_DIRECTORY`` variable in the ``neto.conf`` file,
    and also in the following Neto python scripts which then works with the TinyDB:
    # tinydb/scripts/listdb.py
    # tinydb/scripts/pushcustdb.py
    # tinydb/scripts/worker.py
    # tinydb/scripts/switchdb.py

    Later it will also update the ``hosts_file`` variable in the following bash scripts:
    # scripts/pingneto
    # scripts/tracerouteneto

    :return: nothing
    """
    neto_home_directory = os.environ['HOME'] + "/neto"

    if os.path.isdir(neto_home_directory):
        answer = input("\nDefault \"$HOME/neto\" directory found, do you want to keep it (y/n): ").lower()
        if answer == "y":
            print("Keeping same configuration\n")
            sys.exit()
        elif answer == "n":
            new_neto_home_directory = input("Enter new Neto home directory (example: /full/path/neto/): ")
            if os.path.isdir(new_neto_home_directory):
                config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
                neto_config_path_name = new_neto_home_directory + "neto.config"
                config.read(neto_config_path_name)
                try:
                    config['Neto']['neto_home_directory'] = new_neto_home_directory
                except KeyError:
                    print("\nConfiguration files do no exist, clone the previous directory before start the changes\n")
                    sys.exit(1)
                with open(neto_config_path_name, 'w') as configfile:
                    config.write(configfile)
                tinydb_log_file = new_neto_home_directory + "log/tinydb.log"
                update_config(tinydb_log_file, __file__, new_neto_home_directory)
            else:
                print("Invalid directory")
        else:
            print("Invalid option/n")
            sys.exit()
    else:
        print("\nDefault \"$HOME/neto\" NOT found")
        set_neto_home = input("Enter full path to /neto (example: /full/path/neto/): ")
        if os.path.isdir(set_neto_home) and os.path.isfile((set_neto_home + "/neto.config")):
            tinydb_log_file = set_neto_home + "log/tinydb.log"
            update_config(tinydb_log_file, __file__, set_neto_home)
        else:
            print("\nInvalid directory or neto.config not found\n")
            sys.exit()


def update_config(tinydb_log_file, __file__, new_neto_home_directory):
    """
    Execute the actual updates in the files.

    :param tinydb_log_file: the filename to send the logging message after the operation is completed
    :param __file__: script name who is sending the message to log
    :param new_neto_home_directory: it is the actual new Neto home directory to be updated on files

    :return: nothing
    """
    replace_static_vars_scripts((new_neto_home_directory + "tinydb/scripts/listdb.py"), "NETO_HOME_DIRECTORY = ",
                                new_neto_home_directory)
    replace_static_vars_scripts((new_neto_home_directory + "tinydb/scripts/pushcustdb.py"), "NETO_HOME_DIRECTORY = ",
                                new_neto_home_directory)
    replace_static_vars_scripts((new_neto_home_directory + "tinydb/scripts/worker.py"), "NETO_HOME_DIRECTORY = ",
                                new_neto_home_directory)
    replace_static_vars_scripts((new_neto_home_directory + "tinydb/scripts/switchdb.py"), "NETO_HOME_DIRECTORY = ",
                                new_neto_home_directory)
    replace_static_vars_scripts((new_neto_home_directory + "tinydb/scripts/importcsv.py"), "NETO_HOME_DIRECTORY = ",
                                new_neto_home_directory)
    replace_static_vars_scripts((new_neto_home_directory + "scripts/pingneto"), "hosts_file=",
                                (new_neto_home_directory + "ansible/hosts"))
    replace_static_vars_scripts((new_neto_home_directory + "scripts/tracerouteneto"), "hosts_file=",
                                (new_neto_home_directory + "ansible/hosts"))
    tinydblogging.log_msg(tinydb_log_file, __file__,
                          "Netconf executed. Neto.config and static vars in scripts updated. ")
    print("\nStatics vars in scripts replaced")
    print("\nYou can start using neto :)\n")


def replace_static_vars_scripts(filename, search, replace):
    """
    Replace line by line the ``NETO_HOME_DIRECTORY`` static variable in scripts.

    :param filename: filename to review
    :param search: search pattern to look for
    :param replace: patter to replace

    :return: nothing
    """
    for line in fileinput.input(filename, inplace=True):
        if search in line:
            print((search + "\"" + replace + "\""), end="\n")
        else:
            print(line, end="")


def check_neto_config(neto_home_directory):
    """
    Verifies if the ``neto.config`` file exists in the file tree.

    :param neto_home_directory: to verify if the neto home directory and file exists

    :return: nothing
    """
    if (os.path.isdir(neto_home_directory)) and (os.path.isfile((neto_home_directory + "/neto.config"))):
        return
    else:
        print("Neto home directory or config file not found.\nRun configuration script (netoconf).")
        sys.exit(1)


if __name__ == '__main__':
    neto_config()
    print()
