#!/usr/bin/env python3

import customers
import sites
import devices
import sys
import os
import netorconf
import tinydblogging

_NETOR_HOME_DIRECTORY = "/home/adrian/netor-master/"
_DB_PATH_NAME = "/home/adrian/netor-master/netor/tinydb/data/db.json"


def _redirect():
    """
    Worker redirect to all operations on the DB tables.

    Operates the DB on table specified, for list, add, modify and delete registers.

    It uses the local static variables of the ``worker.py`` script as ``NETOR_HOME_DIRECTORY`` and ``DB_PATH_NAME``,
    unless a full path name to a TinyDB database is specified.

    It supports the following parameters:

    1. specifying operations:

       - l (list)
       - a (add)
       - m (modify)
       - d (delete)

    2. table to operate with

       - customer
       - sites
       - devices

    3. specifying DB full path name

    Example:
    ``../tinydb/scripts/worker.py -l customers /full/path/name/database.json``

    Logging to file ./log/tinydb.log

    :return: nothing
    """

    netorconf.check_netor_config(_NETOR_HOME_DIRECTORY)
    tinydb_log_file = _NETOR_HOME_DIRECTORY + "netor/log/tinydb.log"

    if (len(sys.argv) == 0) or len(sys.argv) > 4:
        print("\nInvalid parameters. Admin -operation tablename dbfile\n")
        return
    else:
        option = sys.argv[1]
        table = sys.argv[2]

    if len(sys.argv) == 4:
        if os.path.isfile((sys.argv[3])):
            print("Using specified DB file: " + sys.argv[3])
            db_path_name = sys.argv[3]
        else:
            print("DB path or file not found")
            return
    elif len(sys.argv) == 3:
        db_path_name = _DB_PATH_NAME
        print("\nUsing script default DB File: " + db_path_name + "\n")
    else:
        print("\nInvalid parameters. Admin -operation tablename\n")
        return

    if table == "customers":
        x = customers.Customers(db_path_name)
    elif table == "sites":
        x = sites.Sites(db_path_name)
    elif table == "devices":
        x = devices.Devices(db_path_name)
    else:
        print("Invalid table name")
        return

    if option == "-l":
        item = x.list()
        if item:
            tinydblogging.log_msg(tinydb_log_file, __file__,
                                  "DB \"" + db_path_name.split("/")[-1] + "\" table \"" + table + "\" listed")
    elif option == "-a":
        item = x.add()
        if item:
            tinydblogging.log_msg(tinydb_log_file, __file__,
                                  "DB \"" + db_path_name.split("/")[-1] + "\" table \"" + table + "\" added \""
                                  + item + "\"")
    elif option == "-m":
        item = x.modify()
        if item:
            tinydblogging.log_msg(tinydb_log_file, __file__,
                                  "DB \"" + db_path_name.split("/")[-1] + "\" table \"" + table + "\" modified: \""
                                  + item[0] + "\" to \"" + item[1] + "\"")
    elif option == "-d":
        item = x.delete()
        if item:
            tinydblogging.log_msg(tinydb_log_file, __file__,
                                  "DB \"" + db_path_name.split("/")[-1] + "\" table \"" + table + "\" deleted \""
                                  + item + "\"")
    else:
        print("Invalid class operation")


if __name__ == '__main__':
    _redirect()
    print()
