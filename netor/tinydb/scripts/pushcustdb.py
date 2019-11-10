#!/usr/bin/env python3

from tinydb import TinyDB, Query
import datetime
import sys
from shutil import copyfile, move
import os
import configparser
import netorconf
import tinydblogging

NETOR_HOME_DIRECTORY = "/home/adrian/netor-master/"
DB_PATH_NAME = "/home/adrian/netor-master/netor/tinydb/data/db.json"


class DB:
    """
    Class DB with parameters used by all the methods to push DB info into **Ansible** and **SaltStack**.
    """

    def __init__(self, db_path_name):
        self.db_path_name = db_path_name
        self.db = TinyDB(self.db_path_name, sort_keys=True, indent=4, separators=(',', ': '))
        self.table_customers = self.db.table('customers')
        self.table_sites = self.db.table('sites')
        self.table_devices = self.db.table('devices')
        self.data_table_customers = sorted(self.table_customers.all(), key=lambda x: (x['customer']))
        self.data_table_sites = sorted(self.table_sites.all(), key=lambda x: (x['customer'], x['site']))
        self.data_table_devices = sorted(self.table_devices.all(), key=lambda x: (x['customer'], x['site'],
                                                                                  x['dev_ip']))

    def select_devices_to_push(self, filter_expression):
        """
        Provides a mechanism to filter the devices in the DB before pushing and replacing Ansible and SaltStack
        configuration.

        :param filter_expression: expression to use a the filter. Support RegEx.

        :return: ``db_devices`` with the filtered device list
        """
        query_customer = Query().customer.search(filter_expression)
        query_site = Query().site.search(filter_expression)
        query_dev_name = Query().dev_name.search(filter_expression)
        query_dev_ip = Query().dev_ip.search(filter_expression)
        query_os = Query().os.search(filter_expression)
        query_salt_proxy_required = Query().salt_proxy_required.search(filter_expression)

        devices_to_push = sorted(self.table_devices.search(query_customer | query_site | query_dev_name | query_dev_ip |
                                                           query_os | query_salt_proxy_required),
                                 key=lambda x: (x['customer'], x['site'], x['dev_name'], x['dev_ip']))

        print('\n%-22s %-22s %-20s %-17s %-11s %-20s %-20s %-16s' % ('Customer Name', 'Site Name', 'Device Name',
                                                                     'Device IP', 'Device OS', 'User Name',
                                                                     'Password', 'Req Slat Proxy'))
        for item in devices_to_push:
            print('%-22s %-22s %-20s %-17s %-11s %-20s %-20s %-16s' % (item['customer'].replace('_', ' '),
                                                                       item['site'].replace('_', ' '), item['dev_name'],
                                                                       item['dev_ip'], item['os'], item['userid'],
                                                                       item['passwd'], item['salt_proxy_required']))

        q = input('\nConfirm devices to push (y/n): ').lower()
        if q == 'y':
            return devices_to_push
        else:
            return False

    @staticmethod
    def ansible_push_inventory(tinydb_log_file, ansible_hosts_path_name, ansible_backup_hosts_path_name,
                               devices_to_push):
        """
        Backup of the ``ansible/hosts`` inventory file to ``ansible/backup`` directory.

        Generates a new ``ansible/hosts`` file based on the DB information (actual push of data).

        :param tinydb_log_file: log file to send the message after the operations are being completed
        :param ansible_hosts_path_name: full path name of the ansible hosts file
        :param ansible_backup_hosts_path_name: full path name of the ansible hosts file directory
        :param devices_to_push: list of devices to push

        :return: nothing
        """

        overwrite = input("\nAnsible: hosts file will be overwritten (y/n): ")
        if overwrite.lower() == "y":
            print("\nBacking up ansible/hosts inventory file to ansible/backup")
            source = ansible_hosts_path_name
            destination = ansible_backup_hosts_path_name + "_" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            copyfile(source, destination)

            print("Generating new ansible/hosts inventory file")
            try:
                file = open(source, "w+")
            except PermissionError:
                print("\nFile 'hosts' not owned. Permission denied.\n")
                sys.exit(1)

            file.write("\n#Time of push DB: " + str(datetime.datetime.now()) + "\n")

            c_prev, s_prev = "", ""

            for item_groups in devices_to_push:
                if item_groups['customer'] != c_prev:
                    file.write("\n[" + item_groups['customer'] + ":children]\n")
                    c_prev = item_groups['customer']
                    if item_groups['site'] != s_prev:
                        file.write(item_groups['customer'] + "_" + item_groups['site'] + "\n")
                        s_prev = item_groups['site']
                    else:
                        file.write(item_groups['customer'] + "_" + item_groups['site'] + "\n")
                        s_prev = item_groups['site']
                elif item_groups['site'] != s_prev:
                    file.write(item_groups['customer'] + "_" + item_groups['site'] + "\n")
                    s_prev = item_groups['site']

            c_prev, s_prev = "", ""

            for item_device in devices_to_push:
                if c_prev != item_device['customer']:
                    file.write("\n[" + item_device['customer'] + "_" + item_device['site'] + "]\n")
                    c_prev = item_device['customer']
                    if s_prev != item_device['site']:
                        file.write(
                            "{}_{}_{} ansible_host={} ansible_network_os={} ansible_user={} ansible_password={} "
                            "username={} password={} platform={}\n".format(item_device['customer'], item_device['site'],
                                                                           item_device['dev_name'],
                                                                           item_device['dev_ip'], item_device['os'],
                                                                           item_device['userid'],
                                                                           item_device['passwd'], item_device['userid'],
                                                                           item_device['passwd'], item_device['os']))
                        s_prev = item_device['site']
                    else:
                        file.write(
                            "{}_{}_{} ansible_host={} ansible_network_os={} ansible_user={} ansible_password={} "
                            "username={} password={} platform={}\n".format(item_device['customer'], item_device['site'],
                                                                           item_device['dev_name'],
                                                                           item_device['dev_ip'], item_device['os'],
                                                                           item_device['userid'],
                                                                           item_device['passwd'], item_device['userid'],
                                                                           item_device['passwd'], item_device['os']))
                        s_prev = item_device['site']
                elif s_prev == item_device['site']:
                    file.write("{}_{}_{} ansible_host={} ansible_network_os={} ansible_user={} ansible_password={} "
                               "username={} password={} platform={}\n"
                               .format(item_device['customer'], item_device['site'], item_device['dev_name'],
                                       item_device['dev_ip'], item_device['os'], item_device['userid'],
                                       item_device['passwd'], item_device['userid'], item_device['passwd'],
                                       item_device['os']))
                    s_prev = item_device['site']
                elif s_prev != item_device['site']:
                    file.write("\n[" + item_device['customer'] + "_" + item_device['site'] + "]\n")
                    file.write("{}_{}_{} ansible_host={} ansible_network_os={} ansible_user={} ansible_password={} "
                               "username={} password={} platform={}\n"
                               .format(item_device['customer'], item_device['site'], item_device['dev_name'],
                                       item_device['dev_ip'], item_device['os'], item_device['userid'],
                                       item_device['passwd'], item_device['userid'], item_device['passwd'],
                                       item_device['os']))

            file.close()
            tinydblogging.log_msg(tinydb_log_file, __file__, "Push DB executed. Ansible configuration files updated.")
            print("\nPush DB executed. Ansible configuration files updated.\n")
            return
        else:
            return

    @staticmethod
    def salt_push_inventory(tinydb_log_file, salt_minion_path_name, salt_backup_directory, salt_pillar_directory,
                            salt_backup_pillar_directory, salt_top_path_name, salt_states_directory, devices_to_push):
        """
        Backup ``salt/config/minion`` file to ``salt/config/backup`` directory.

        Generates a new minion file based on the actual minion file, but replacing the first lines
        **(to be improved in order to review the content/update of the lines)**.

        Generates the new ``top.sls`` file with the devices listed in the DB, and all the states only in the
        \\'*' section.

        **(To be improved to actually add the corresponding states to specific devices)**.

        Backup ``salt/config/pillar/\\*.sls`` files to ``/salt/config/backup/pillar directory``.

        Generates new ``pillar/*device_name*.sls`` files based on the content of the DB file, if the device has to be
        managed via ``salt-proxy`` according the DB ``salt_proxy_required`` field. With the following details:
        ::

            proxy:
              proxytype: napalm
              driver: ios
              host: dev_ip
              username: userid
              password: passwd
              optional_args:
                use_keys: True
                auto_rollback_on_error: True

        :param tinydb_log_file: log file to send the message after the operations are being completed
        :param salt_minion_path_name: minion full path name
        :param salt_backup_directory: minion backup directory
        :param salt_pillar_directory: pillar .sls files directory
        :param salt_backup_pillar_directory: backup pillar \\*.sls directory
        :param salt_top_path_name: full path name of ''top.sls'' file
        :param salt_states_directory: add all the states to the general ``\\'*'`` section of the ``top.sls`` file
        :param devices_to_push: list of devices to push to Ansible and SaltStack

        :return: nothing
        """
        overwrite = input("\nSalt: minion config file will be updated, and top.sls and [dev_name].sls files will be "
                          "overwritten (y/n): ")

        if overwrite.lower() == "y":
            print("\nBacking up salt/config/minion configuration file to salt/config/backup")
            salt_minion_backup_path_name = salt_backup_directory + "minion_" + \
                                           datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            copyfile(salt_minion_path_name, salt_minion_backup_path_name)

            print("Creating new temporary minion configuration file")
            new_file_name = salt_minion_path_name + ".pre"
            new_file = open(new_file_name, 'w+')
            new_file.write("master: localhost\n")
            new_file.write("\n")
            new_file.write("beacons:\n")
            new_file.write("  salt_proxy:\n")
            new_file.write("    - proxies:\n")
            for doc in devices_to_push:
                if doc['salt_proxy_required'] == "y":
                    new_file.write("        " + doc['customer'] + "_" + doc['site'] + "_" + doc['dev_name'] + ": {}\n")
            new_file.write("\n")
            salt_minion_former_start_config = False

            try:
                with open(salt_minion_path_name, 'r') as file:
                    for line in file:
                        if "Primary configuration settings" in line:
                            salt_minion_former_start_config = True
                        if salt_minion_former_start_config:
                            new_file.writelines(line)
            except (OSError, IOError):
                print("Original minion file not found, skipping.")

            new_file.close()

            print("Replacing minion configuration file")
            move(new_file_name, salt_minion_path_name)

            print("Backing up salt/config/pillar sls inventory files to salt/config/backup")
            for file_name in os.listdir(salt_pillar_directory):
                file_is_directory = salt_pillar_directory + file_name
                if not os.path.isdir(file_is_directory):
                    source_file_name = salt_pillar_directory + file_name
                    destination_file_name = salt_backup_pillar_directory + file_name + "." + \
                                            datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                    copyfile(source_file_name, destination_file_name)

            print("Removing salt/config/pillar sls inventory files")
            for file_name in os.listdir(salt_pillar_directory):
                file_is_not_directory = salt_pillar_directory + file_name
                if not os.path.isdir(file_is_not_directory):
                    os.remove(file_is_not_directory)

            print("Generating new top.sls inventory file")
            new_top_file = open(salt_top_path_name, "w+")
            new_top_file.write("base:\n")
            new_top_file.write("  '*':\n")
            for state_file_name in os.listdir(salt_states_directory):
                dev_name = state_file_name.split(".sls")
                new_top_file.write("    - " + str(dev_name[0]) + "\n")
            for item_device in devices_to_push:
                new_top_file.write("\n  '" + item_device['customer'] + "_" + item_device['site'] + "_" +
                                   item_device['dev_name'] + "':\n")
                new_top_file.write("    - " + item_device['customer'] + "_" + item_device['site'] + "_" +
                                   item_device['dev_name'] + "\n")
            new_top_file.close()

            print("Generating new sls devices files")
            for item_device in devices_to_push:
                new_sls_device_file_name = salt_pillar_directory + item_device['customer'] + "_" + \
                                           item_device['site'] + "_" + item_device['dev_name'] + ".sls"
                new_sls_device_file = open(new_sls_device_file_name, "w+")
                new_sls_device_file.write("proxy:\n")
                new_sls_device_file.write("  proxytype: napalm\n")
                new_sls_device_file.write("  driver: ios\n")
                new_sls_device_file.write("  host: " + item_device['dev_ip'] + "\n")
                new_sls_device_file.write("  username: " + item_device['userid'] + "\n")
                new_sls_device_file.write("  password: " + item_device['passwd'] + "\n")
                new_sls_device_file.write("  optional_args:\n")
                new_sls_device_file.write("    use_keys: True\n")
                new_sls_device_file.write("    auto_rollback_on_error: True\n")
                new_sls_device_file.close()
            tinydblogging.log_msg(tinydb_log_file, __file__, "Push DB executed. SaltStack configuration files updated.")
            print("\nPush DB executed. SaltStack configuration files updated.")
        else:
            return


def start_process():
    """
    Checks if the ``netor.conf`` file exist according the local static variable ``NETOR_HOME_DIRECTORY``.

    It supports passing as parameter the ``NETOR_HOME_DIRECTORY`` in order to push to the DB specified
    in the ``netor.conf`` configuration file.

    Then execute the functions to push the DB content on **Ansible** ans **SaltStack** configuration files, according
    to the settings of the ``netor.conf`` configuration file.

    It supports filtering of the DB, with literal text or RegEx, in order to not import more devices than required. As
    an example, you could have several clients on a DB, and push only the clients with which you are working, or the
    same example applies to work per sites, per IP range, per device name, etc.

    **Restart of the Salt minion is required.**

    :return: nothing
    """
    netorconf.check_netor_config(NETOR_HOME_DIRECTORY)

    try:
        netor_home_directory = sys.argv[1]
    except IndexError:
        netor_home_directory = NETOR_HOME_DIRECTORY

    tinydb_log_file = netor_home_directory + "netor/log/tinydb.log"

    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    print("Reading netor.config")
    config.read((netor_home_directory + "netor/netor.config"))

    if os.path.isfile(config['TinyDB']['db_path_name']):
        x = DB(config['TinyDB']['db_path_name'])
        print("Using DB file at:" + config['TinyDB']['db_path_name'])
    else:
        print("DB path or file not found")
        return

    filter_question = input("\nFull database will be pushed. Do you want to specify a limiting filter? (y/n): ").lower()
    if filter_question == 'y':
        filter_expression = input('Enter literal filter or RegEx: ')
    elif filter_question == 'n':
        filter_expression = '.*'
    else:
        print('\nInvalid option')
        return

    devices_to_push = x.select_devices_to_push(filter_expression)

    if devices_to_push:
        print("\nPUSH DEVICE DB TO ANSIBLE AND SALTSTACK INVENTORY FILES")

        x.ansible_push_inventory(tinydb_log_file,
                                 config['Ansible']['ansible_hosts_path_name'],
                                 config['Ansible']['ansible_backup_hosts_path_name'], devices_to_push)

        x.salt_push_inventory(tinydb_log_file,
                              config['SaltStack']['salt_minion_path_name'],
                              config['SaltStack']['salt_backup_directory'],
                              config['SaltStack']['salt_pillar_directory'],
                              config['SaltStack']['salt_backup_pillar_directory'],
                              config['SaltStack']['salt_top_path_name'],
                              config['SaltStack']['salt_states_directory'], devices_to_push)

        print("\nPlease restart salt minion in order to use the new configuration files !!!")
        return

    else:
        print('\nCancelling push.')
        return


if __name__ == '__main__':
    start_process()
    print()
