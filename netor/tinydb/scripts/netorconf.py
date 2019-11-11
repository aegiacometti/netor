#!/usr/bin/env python3

import os
import sys
import configparser
import fileinput
import tinydblogging
import datetime
from shutil import copyfile


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
    netor_home_directory = os.environ['HOME'] + "/netor/"

    if os.path.isdir(netor_home_directory):
        answer = input("\nDefault \"$HOME/netor\" directory found, do you want to keep it (y/n): ").lower()
        if answer == "y":
            print("Keeping same configuration\n")

            config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
            netor_config_path_name = netor_home_directory + "netor/netor.config"
            config.read(netor_config_path_name)
            try:
                config['Netor']['netor_home_directory'] = netor_home_directory
            except KeyError:
                print("\nConfiguration files do no exist, clone the previous directory before start the changes\n")
                sys.exit(1)
            with open(netor_config_path_name, 'w') as configfile:
                config.write(configfile)
            update_ansible(netor_home_directory)
            tinydb_log_file = netor_home_directory + "netor/log/tinydb.log"
            update_config(tinydb_log_file, __file__, netor_home_directory)
            sys.exit()
        elif answer == "n":
            new_netor_home_directory = input("Enter new Neto home directory (example: /full/path/netor/): ")
            if new_netor_home_directory[-1] != '/':
                new_netor_home_directory = new_netor_home_directory + '/'
            if os.path.isdir(new_netor_home_directory):
                config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
                netor_config_path_name = new_netor_home_directory + "netor/netor.config"
                config.read(netor_config_path_name)
                try:
                    config['Netor']['netor_home_directory'] = new_netor_home_directory
                except KeyError:
                    print("\nConfiguration files do no exist, clone the previous directory before start the changes\n")
                    sys.exit(1)
                with open(netor_config_path_name, 'w') as configfile:
                    config.write(configfile)
                update_ansible(new_netor_home_directory)
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


def update_ansible(netor_home_directory):
    ansible_config_file = os.environ['HOME'] + '/.ansible.cfg'
    replace_static_vars_scripts(ansible_config_file, 'inventory', ' = ' + netor_home_directory + 'netor/ansible/hosts',
                                '')
    replace_static_vars_scripts(ansible_config_file, 'library', ' = ' + netor_home_directory + 'netor/ansible/modules',
                                '')
    replace_static_vars_scripts(ansible_config_file, 'transport', ' = paramiko',
                                '')
    replace_static_vars_scripts(ansible_config_file, 'host_key_auto_add', ' = True',
                                '')
    print('Netor home directory replaced in Ansible.')


def backup_filename(new_netor_home_directory, filename):
    print('\nBacking up ' + filename + ' to ' + new_netor_home_directory + 'netor/salt/backup/')
    source = new_netor_home_directory + 'netor/salt/config/' + filename
    destination = new_netor_home_directory + 'netor/salt/backup/' + filename + "_" + \
                  datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    copyfile(source, destination)


def create_master_config_file(new_netor_home_directory, filename):
    full_path_filename = new_netor_home_directory + 'netor/salt/config/' + filename
    file = open(full_path_filename, '+w')
    file.write('# for salt-sproxy\n')
    file.write('use_existing_proxy: true\n')
    file.write('\n')
    file.write('#####        Security settings       #####\n')
    file.write('# Enable "open mode", this mode still maintains encryption, but turns off\n')
    file.write('# authentication, this is only intended for highly secure environments or for\n')
    file.write('# the situation where your keys end up in a bad state. If you run in open mode\n')
    file.write('# you do so at your own risk!\n')
    file.write('open_mode: True\n')
    file.write('\n')
    file.write('# Enable auto_accept, this setting will automatically accept all incoming\n')
    file.write('# public keys from the minions. Note that this is insecure.\n')
    file.write('auto_accept: True\n')
    file.write('\n')
    file.write('# The path to the master\'s configuration file.\n')
    file.write('conf_file: ' + new_netor_home_directory + 'netor/salt/config/master\n')
    file.write('\n')
    file.write('# Directory used to store public key data:\n')
    file.write('pki_dir: ' + new_netor_home_directory + 'netor/salt/config/pki/master\n')
    file.write('\n')
    file.write('#####      File Server settings      #####\n')
    file.write('file_roots:\n')
    file.write('  base:\n')
    file.write('    - ' + new_netor_home_directory + 'netor/salt/config/pillar/\n')
    file.write('    - ' + new_netor_home_directory + 'netor/salt/config/pillar/states/\n')
    file.write('\n')
    file.write('#####         Pillar settings        #####\n')
    file.write('pillar_roots:\n')
    file.write('  base:\n')
    file.write('    - ' + new_netor_home_directory + 'netor/salt/config/pillar/\n')
    file.write('    - ' + new_netor_home_directory + 'netor/salt/config/pillar/states/\n')
    file.close()


def update_master_config_file(new_netor_home_directory, filename):
    backup_filename(new_netor_home_directory, filename)
    # pending to develop update of the file with the new directory
    create_master_config_file(new_netor_home_directory, filename)


def create_minion_config_file(new_netor_home_directory, filename):
    full_path_filename = new_netor_home_directory + 'netor/salt/config/' + filename
    file = open(full_path_filename, '+w')
    file.write('##### Primary configuration settings #####\n')
    file.write('master: localhost\n')
    file.write('\n')
    file.write('# The path to the minion\'s configuration file.\n')
    file.write('conf_file: ' + new_netor_home_directory + 'netor/salt/config/minion\n')
    file.write('# The directory to store the pki information in\n')
    file.write('pki_dir: ' + new_netor_home_directory + 'netor/salt/config/pki/minion\n')
    file.write('\n')
    file.write('#####     File Directory Settings    #####\n')
    file.write('file_roots:\n')
    file.write('  base:\n')
    file.write('    - ' + new_netor_home_directory + 'netor/salt/config/pillar/\n')
    file.write('    - ' + new_netor_home_directory + 'neto/salt/config/pillar/states/\n')
    file.write('\n')
    file.write('pillar_roots:\n')
    file.write('  base:\n')
    file.write('    - ' + new_netor_home_directory + 'netor/salt/config/pillar/\n')
    file.write('    - ' + new_netor_home_directory + 'netor/salt/config/pillar/ states /\n')
    file.write('\n')
    file.write('######        Security settings       #####\n')
    file.write('# Enable "open mode", this mode still maintains encryption, but turns off\n')
    file.write('# authentication, this is only intended for highly secure environments or for\n')
    file.write('# the situation where your keys end up in a bad state. If you run in open mode\n')
    file.write('# you do so at your own risk!\n')
    file.write('open_mode: True\n')
    file.close()


def update_minion_config_file(new_netor_home_directory, filename):
    backup_filename(new_netor_home_directory, filename)
    # pending to develop update of the file with the new directory
    create_minion_config_file(new_netor_home_directory, filename)


def create_proxy_config_file(new_netor_home_directory, filename):
    full_path_filename = new_netor_home_directory + 'netor/salt/config/' + filename
    file = open(full_path_filename, '+w')
    file.write('##### Primary configuration settings #####\n')
    file.write('\n')
    file.write('master: localhost\n')
    file.write('conf_file: ' + new_netor_home_directory + 'netor/salt/config/proxy\n')
    file.write('mine_enabled: true  # not required, but nice to have\n')
    file.write('mine_functions:\n')
    file.write('  net.ipaddrs: []\n')
    file.write('  net.lldp: []\n')
    file.write('  net.mac: []\n')
    file.write('  net.arp: []\n')
    file.write('  net.interfaces: []\n')
    file.write('mine_interval: 5\n')
    file.write('\n')
    file.write('######         Thread settings        #####\n')
    file.write('multiprocessing: false\n')
    file.write('\n')
    file.write('#####     File Directory Settings    #####\n')
    file.write('file_roots:\n')
    file.write('  base:\n')
    file.write('    - ' + new_netor_home_directory + 'netor/salt/config/\n')
    file.write('    - ' + new_netor_home_directory + 'netor/salt/config/pillar/\n')
    file.write('pillar_roots:\n')
    file.write('  base:\n')
    file.write('    - ' + new_netor_home_directory + 'netor/salt/config/\n')
    file.write('    - ' + new_netor_home_directory + 'netor/salt/config/pillar/\n')
    file.write('\n')
    file.write('######        Security settings       #####\n')
    file.write('###########################################\n')
    file.write('# Enable "open mode", this mode still maintains encryption, but turns off\n')
    file.write('# authentication, this is only intended for highly secure environments or for\n')
    file.write('# the situation where your keys end up in a bad state. If you run in open mode\n')
    file.write('# you do so at your own risk!\n')
    file.write('open_mode: True\n')
    file.write('# The directory to store the pki information in\n')
    file.write('pki_dir: ' + new_netor_home_directory + 'netor/salt/config/pki/proxy  # not required - this separates '
               'the proxy keys into a different directory\n')
    file.close()


def update_proxy_config_file(new_netor_home_directory, filename):
    backup_filename(new_netor_home_directory, filename)
    # pending to develop update of the file with the new directory
    create_proxy_config_file(new_netor_home_directory, filename)


def file_update_redirect(new_netor_home_directory, filename):
    if 'master' in filename:
        update_master_config_file(new_netor_home_directory, filename)
    elif 'minion' in filename:
        update_minion_config_file(new_netor_home_directory, filename)
    elif 'proxy' in filename:
        update_proxy_config_file(new_netor_home_directory, filename)
    else:
        print('\nError while checking Salt master, minion and proxy configuration files')
        sys.exit(1)


def file_create_redirect(new_netor_home_directory, filename):
    if 'master' in filename:
        create_master_config_file(new_netor_home_directory, filename)
    elif 'minion' in filename:
        create_minion_config_file(new_netor_home_directory, filename)
    elif 'proxy' in filename:
        create_proxy_config_file(new_netor_home_directory, filename)
    else:
        print('\nError while checking Salt master, minion and proxy configuration files')
        sys.exit(1)


def create_update_master_minion_proxy(new_netor_home_directory, filename):
    full_salt_config_filename = new_netor_home_directory + 'netor/salt/' + filename
    if os.path.isfile(full_salt_config_filename):
        file_update_redirect(new_netor_home_directory, filename)
    else:
        file_create_redirect(new_netor_home_directory, filename)


def update_config(tinydb_log_file, __file__, new_netor_home_directory):
    """
    Execute the actual updates in the files. SaltStack master, minion and proxy.

    :param tinydb_log_file: the filename to send the logging message after the operation is completed
    :param __file__: script name who is sending the message to log
    :param new_netor_home_directory: it is the actual new Neto home directory to be updated on files

    :return: nothing
    """
    replace_static_vars_scripts((new_netor_home_directory + "netor/tinydb/scripts/listdb.py"),
                                "NETOR_HOME_DIRECTORY = ", new_netor_home_directory, '\"')
    replace_static_vars_scripts((new_netor_home_directory + "netor/tinydb/scripts/pushcustdb.py"),
                                "NETOR_HOME_DIRECTORY = ", new_netor_home_directory, '\"')
    replace_static_vars_scripts((new_netor_home_directory + "netor/tinydb/scripts/worker.py"),
                                "NETOR_HOME_DIRECTORY = ", new_netor_home_directory, '\"')
    replace_static_vars_scripts((new_netor_home_directory + "netor/tinydb/scripts/switchdb.py"),
                                "NETOR_HOME_DIRECTORY = ", new_netor_home_directory, '\"')
    replace_static_vars_scripts((new_netor_home_directory + "netor/tinydb/scripts/importcsv.py"),
                                "NETOR_HOME_DIRECTORY = ", new_netor_home_directory, '\"')

    replace_static_vars_scripts((new_netor_home_directory + "bin/netor-ping"), "hosts_file=",
                                (new_netor_home_directory + "netor/ansible/hosts"), '\"')
    replace_static_vars_scripts((new_netor_home_directory + "bin/netor-traceroute"), "hosts_file=",
                                (new_netor_home_directory + "netor/ansible/hosts"), '\"')

    replace_static_vars_scripts((new_netor_home_directory + "bin/netor-db-customers"), "netor_home_directory=",
                                new_netor_home_directory, '\"')
    replace_static_vars_scripts((new_netor_home_directory + "bin/netor-db-devices"), "netor_home_directory=",
                                new_netor_home_directory, '\"')
    replace_static_vars_scripts((new_netor_home_directory + "bin/netor-db-export"), "netor_home_directory=",
                                new_netor_home_directory, '\"')
    replace_static_vars_scripts((new_netor_home_directory + "bin/netor-db-import"), "netor_home_directory=",
                                new_netor_home_directory, '\"')
    replace_static_vars_scripts((new_netor_home_directory + "bin/netor-db-list"), "netor_home_directory=",
                                new_netor_home_directory, '\"')
    replace_static_vars_scripts((new_netor_home_directory + "bin/netor-db-push"), "netor_home_directory=",
                                new_netor_home_directory, '\"')
    replace_static_vars_scripts((new_netor_home_directory + "bin/netor-db-sites"), "netor_home_directory=",
                                new_netor_home_directory, '\"')
    replace_static_vars_scripts((new_netor_home_directory + "bin/netor-db-switch"), "netor_home_directory=",
                                new_netor_home_directory, '\"')
    replace_static_vars_scripts((new_netor_home_directory + "bin/netor-config"), "netor_home_directory=",
                                new_netor_home_directory, '\"')

    print("\nStatics vars in scripts replaced")

    create_update_master_minion_proxy(new_netor_home_directory, 'master')
    create_update_master_minion_proxy(new_netor_home_directory, 'minion')
    create_update_master_minion_proxy(new_netor_home_directory, 'proxy')

    print('\nNetor home directory replaced in salt master, minion and proxy.')
    print("\nATTENTION: SaltStack configuration files must be copied manually with root privilege")
    print("\nsudo cp " + new_netor_home_directory + "netor/salt/config/master /etc/salt/")
    print("\nsudo cp " + new_netor_home_directory + "netor/salt/config/minion /etc/salt/")
    print("\nsudo cp " + new_netor_home_directory + "netor/salt/config/proxy /etc/salt/")
    print("\nAdd " + new_netor_home_directory + "/bin to your .profile")
    print("     vi $HOME/.profile")
    print("     PATH=\"$PATH:" + new_netor_home_directory + "/bin")
    print("\nLogoff session, login again and restart salt with \"netor-salt-restart\"")

    tinydblogging.log_msg(tinydb_log_file, __file__,
                          "Netconf executed. Neto.config and static vars in scripts updated. ")


def replace_static_vars_scripts(filename, search, replace, delimiter):
    """
    Replace line by line the ``NETOR_HOME_DIRECTORY`` static variable in scripts.

    :param filename: filename to review
    :param search: search pattern to look for
    :param replace: patter to replace
    :param delimiter: to add a delimiter surrounding the path names

    :return: nothing
    """
    try:
        for line in fileinput.input(filename, inplace=True):
            if search in line:
                print((search + delimiter + replace + delimiter), end="\n")
            else:
                print(line, end="")
    except FileNotFoundError:
        print("\nERROR File not found " + filename)
        print("Manually find systemd folder and file " + filename.split("/")[-1] +
              " and modify the parameter \"" + search + "\" in the file to point to " + replace + "\n")
    except PermissionError:
        print("\nERROR Permission denied to modify file " + filename)
        print("Manually modify the parameter -\"" + search + "\" in the file to point to " + replace)


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
