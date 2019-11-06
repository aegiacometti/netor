#!/usr/bin/env python3

import netoconf
import configparser
import os
import tinydblogging

NETO_HOME_DIRECTORY = "/home/adrian/neto-master/neto/"


def switchdb():
    """
    Updates the full path name of the DB in configuration and scripts files.

    As an example it can be used to have multiple database files on the same neto home directory, in order
    to support different group of devices, like different customers, environments, group of devices, or even
    for copying DB files to different folders or machines for sharing them.

    :return: nothing
    """
    netoconf.check_neto_config(NETO_HOME_DIRECTORY)
    tinydb_log_file = NETO_HOME_DIRECTORY + "/log/tinydb.log"
    db_name = input("Select DB name to switch to: ").lower()
    full_db_path_name = (NETO_HOME_DIRECTORY + "tinydb/data/" + db_name + ".json")
    if os.path.isfile(full_db_path_name):
        print("\nReusing existing DB")
        update_config(db_name, full_db_path_name)
    else:
        print("\nNew DB name detected")
        print(full_db_path_name)
        update_config(db_name, full_db_path_name)
        print("\nPlease create the first customer in order to create DB with (dbcustomer)")

    tinydblogging.log_msg(tinydb_log_file, __file__,
                          "Switch DB command executed. Parameters in configuration files and scripts updated. ")
    print("\nSwitch DB command executed. Parameters in configuration files and scripts updated. ")


def update_config(db_name, full_db_path_name):
    """
    Updates the configuration files.

    *To complete the process you need to push the DB with dbpush*.

    :param db_name: DB name to use
    :param full_db_path_name: full path name of the DB to use

    :return: nothing
    """
    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    neto_config_path_name = (NETO_HOME_DIRECTORY + "neto.config")
    config.read(neto_config_path_name)
    config['TinyDB']['db_path_name'] = "${Neto:neto_home_directory}" + "tinydb/data/" + db_name + ".json"
    with open(neto_config_path_name, 'w') as configfile:
        config.write(configfile)

    netoconf.replace_static_vars_scripts((NETO_HOME_DIRECTORY + "tinydb/scripts/listdb.py"), "DB_PATH_NAME = ",
                                         full_db_path_name)
    netoconf.replace_static_vars_scripts((NETO_HOME_DIRECTORY + "tinydb/scripts/pushcustdb.py"), "DB_PATH_NAME = ",
                                         full_db_path_name)
    netoconf.replace_static_vars_scripts((NETO_HOME_DIRECTORY + "tinydb/scripts/worker.py"), "DB_PATH_NAME = ",
                                         full_db_path_name)
    netoconf.replace_static_vars_scripts((NETO_HOME_DIRECTORY + "tinydb/scripts/importcsv.py"), "DB_PATH_NAME = ",
                                         full_db_path_name)

    print("\nNew DB parameters updated in configuration files")
    print("\nRemember to push new DB to configuration files to start using the BD (dbpush)")


if __name__ == '__main__':
    switchdb()
    print()
