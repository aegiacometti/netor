#!/usr/bin/env python3

import netorconf
import configparser
import os
import tinydblogging
import glob

_NETOR_HOME_DIRECTORY = "/home/adrian/netor-master/"


def _switchdb():
    """
    Updates the full path name of the DB in configuration and scripts files.

    As an example it can be used to have multiple database files on the same netor home directory, in order
    to support different group of devices, like different customers, environments, group of devices, or even
    for copying DB files to different folders or machines for sharing them.

    :return: nothing
    """
    netorconf.check_netor_config(_NETOR_HOME_DIRECTORY)
    tinydb_log_file = _NETOR_HOME_DIRECTORY + "netor/log/tinydb.log"
    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    netor_config_path_name = (_NETOR_HOME_DIRECTORY + "netor/netor.config")
    config.read(netor_config_path_name)
    current_db_path_name = config['TinyDB']['db_path_name']

    print('\nAvailable Databases:\n')
    for item in glob.glob(_NETOR_HOME_DIRECTORY + 'netor/tinydb/data/*.json'):
        print(item)
    print()
    db_name = input("Enter DB full path name, or \"name\" to create a new DB as \"name.json\", "
                    "or hit enter to use current [" + current_db_path_name + "]: ").lower()

    if db_name == '':
        print("\nUsing current DB")
        db_name = current_db_path_name
    elif os.path.isfile(db_name):
        print("\nReusing existing DB")
        db_name = db_name
    elif db_name.isalnum():
        print("\nCreating new DB")
        db_name = _NETOR_HOME_DIRECTORY + "netor/tinydb/data/" + db_name + ".json"
        print("\nPlease create the first customer in order to create DB with (dbcustomer)")
    else:
        print('Invalid DB file directory')
        exit(0)

    _update_config(db_name)

    tinydblogging.log_msg(tinydb_log_file, __file__,
                          "Switch DB command executed. Parameters in configuration files and scripts updated. ")
    print("\nSwitch DB command executed. Parameters in configuration files and scripts updated. ")


def _update_config(full_db_path_name):
    """
    Updates the configuration files.

    *To complete the process you need to push the DB with netor-db-push*.

    :param full_db_path_name: full path name of the DB to use

    :return: nothing
    """
    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    netor_config_path_name = (_NETOR_HOME_DIRECTORY + "netor/netor.config")
    config.read(netor_config_path_name)
    db_name = full_db_path_name.split('/')[-1]
    config['TinyDB']['db_path_name'] = "${Netor:netor_home_directory}" + "netor/tinydb/data/" + db_name
    with open(netor_config_path_name, 'w') as configfile:
        config.write(configfile)

    netorconf.replace_static_vars_scripts((_NETOR_HOME_DIRECTORY + "netor/tinydb/scripts/listdb.py"),
                                          "DB_PATH_NAME = ", full_db_path_name, '\"')
    netorconf.replace_static_vars_scripts((_NETOR_HOME_DIRECTORY + "netor/tinydb/scripts/pushcustdb.py"),
                                          "DB_PATH_NAME = ", full_db_path_name, '\"')
    netorconf.replace_static_vars_scripts((_NETOR_HOME_DIRECTORY + "netor/tinydb/scripts/worker.py"),
                                          "DB_PATH_NAME = ", full_db_path_name, '\"')
    netorconf.replace_static_vars_scripts((_NETOR_HOME_DIRECTORY + "netor/tinydb/scripts/importcsv.py"),
                                          "DB_PATH_NAME = ", full_db_path_name, '\"')

    print("\nNew DB parameters updated in configuration files")
    print("\nRemember to push new DB to configuration files to start using the BD (netor-db-push)")


if __name__ == '__main__':
    _switchdb()
    print()
