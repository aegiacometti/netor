#!/usr/bin/env python3

import dbparam
import configparser
import netoconf
import sys
import os
import tinydblogging

NETO_HOME_DIRECTORY = "/home/adrian/neto-master/neto/"
DB_PATH_NAME = "/home/adrian/neto-master/neto/tinydb/data/db.json"


class DB(dbparam.DbParam):

    def list(self, tinydb_log_file, db_path_name):
        """
        List full DB content.

        :param tinydb_log_file: log file to send the message
        :param db_path_name: full path name of the DB to list

        :return:
        """
        print("\nLIST DATABASE")

        db_customers = sorted(self.table_customers.all(), key=lambda x: (x['customer']))
        db_sites = sorted(self.table_sites.all(), key=lambda x: (x['customer'], x['site']))
        db_devices = sorted(self.table_devices.all(), key=lambda x: (x['customer'], x['site'], x['dev_name']))
        print()
        print("List Customers")
        for item in db_customers:
            print(item['customer'].replace('_', ' '))
        print()
        print("List Sites")
        print('\n%-23s %-23s' % ('Customer Name', 'Site Name'))
        for item in db_sites:
            print('%-23s %-23s' % (item['customer'].replace('_', ' '), item['site'].replace('_', ' ')))
        print()
        print("List Devices")
        print('\n%-22s %-22s %-20s %-17s %-11s %-20s %-20s %-16s' % ('Customer Name', 'Site Name', 'Device Name',
                                                                     'Device IP', 'Device OS', 'User Name',
                                                                     'Password', 'Req Slat Proxy'))
        for item in db_devices:
            print('%-22s %-22s %-20s %-17s %-11s %-20s %-20s %-16s' % (item['customer'].replace('_', ' '),
                                                                       item['site'].replace('_', ' '), item['dev_name'],
                                                                       item['dev_ip'], item['os'], item['userid'],
                                                                       item['passwd'], item['salt_proxy_required']))
        tinydblogging.log_msg(tinydb_log_file, __file__, "Full DB listed: " + db_path_name)
        print("\nFull DB listed: " + db_path_name)

    def export_csv(self, tinydb_log_file, db_path_name, export_path_name):
        """
        Export full DB table 'devices' content to CSV

        :param tinydb_log_file: log file to send the message
        :param db_path_name: full path name of the DB to list
        :param export_path_name: full path name of .CVS file to export the DB

        :return:
        """

        db_devices = self.table_devices.all()
        file = open(export_path_name, "w")
        file.write("customer,site,dev_name,dev_ip,os,userid,passwd,salt_proxy_required\n")
        print()
        for item in db_devices:
            print("%s,%s,%s,%s,%s,%s,%s,%s" % (item['customer'], item['site'], item['dev_name'], item['dev_ip'],
                                               item['os'], item['userid'], item['passwd'], item['salt_proxy_required']))
            file.write("%s,%s,%s,%s,%s,%s,%s,%s\n" % (item['customer'], item['site'], item['dev_name'], item['dev_ip'],
                                                      item['os'], item['userid'], item['passwd'],
                                                      item['salt_proxy_required']))
        file.close()
        tinydblogging.log_msg(tinydb_log_file, __file__, "Full DB exported: " + db_path_name + " to filename"
                              + export_path_name)
        print("\nFull DB exported: " + db_path_name + " to filename " + export_path_name)


def listdb():
    """
    List the full content of the DB specified in the configuration file ``neto.conf``, unless a full path name
    to different TinyDB database is specified as an argument.

    Verify existence of ``neto.conf`` file, since it could be required by the confparse module in order to get
    the DB full path name.

    example:
        ``../tinydb/scripts/listdb.py /full/path/name/database.json``

    Also has an export function to dump the current DB to a ``.csv`` file. If you want to export another DB you will
    need to ``dbswitch`` first.

    example:
        ``../tinydb/scripts/listdb.py -e``

    :return: nothing
    """
    netoconf.check_neto_config(NETO_HOME_DIRECTORY)
    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    tinydb_log_file = NETO_HOME_DIRECTORY + "/log/tinydb.log"

    if len(sys.argv) == 2:
        if os.path.isfile(sys.argv[1]):
            db_path_name = sys.argv[1]
            print("\nUsing specified DB file: " + db_path_name)
            x = DB(db_path_name)
            x.list(tinydb_log_file, db_path_name)
        elif sys.argv[1] == "-e":
            export_path_name = input("Enter full path name for the export file (example: /full/path/name/export.csv): ")
            tmp = export_path_name.split("/")[:-1]
            separator = "/"
            export_directory = separator.join(tmp)
            if os.path.isdir(export_directory):
                print("\nUsing default DB File: " + DB_PATH_NAME)
                config.read((NETO_HOME_DIRECTORY + "neto.config"))
                db_path_name = config['TinyDB']['db_path_name']
                x = DB(db_path_name)
                x.export_csv(tinydb_log_file, db_path_name, export_path_name)
            else:
                print("\nInvalid directory.")
        else:
            print("\nInvalid specified DB file")
            return
    elif len(sys.argv) == 1:
        print("\nUsing default DB File: " + DB_PATH_NAME)
        config.read((NETO_HOME_DIRECTORY + "neto.config"))
        db_path_name = config['TinyDB']['db_path_name']
        x = DB(db_path_name)
        x.list(tinydb_log_file, db_path_name)
    else:
        print("\nInvalid parameters. Only admit specify DB full path name\n")
        return


if __name__ == '__main__':
    listdb()
    print()
