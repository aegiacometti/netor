#!/usr/bin/env python3

import glob
import os
from sys import exit
import netorconf
import ipaddress
import dbparam
from tinydb import Query
import tinydblogging

_NETOR_HOME_DIRECTORY = "/home/adrian/netor-master/"
_DB_PATH_NAME = "/home/adrian/netor-master/netor/tinydb/data/db.json"


class ImportDevices(dbparam.DbParam):
    """
    Class to import data from a CSV file

    Format: customer,site,dev_name,dev_ip,os,userid,passwd,salt_proxy_required

    Names should be alphanumeric, and less than 20 characters, all names will be transformed to lowercase.
    """

    def add_line_to_db(self, checked_line_values, line_number):
        """
        Add a customers, sites and devices to the DB.

        :param checked_line_values: CSV line to import to DB.
        :param line_number: line number being processed.

        :return: ``True`` if the lines was added and ``False`` if not.
        """

        customer = checked_line_values[0]
        query_customer = Query().customer == customer
        res = self.table_customers.search(query_customer)
        if not res:
            self.table_customers.insert({'customer': customer})

        site = checked_line_values[1]
        query_site = Query().site == site
        res = self.table_sites.search(query_customer & query_site)
        if not res:
            self.table_sites.insert({'customer': customer, 'site': site})

        dev_name = checked_line_values[2]
        dev_ip = checked_line_values[3]

        res = self.table_devices.search(query_site & query_customer &
                                        (Query().dev_ip == dev_ip) & (Query().dev_name == dev_name))
        if not res:
            os_input = checked_line_values[4]
            userid = checked_line_values[5]
            passwd = checked_line_values[6]
            salt_proxy_required = checked_line_values[7]
            self.table_devices.insert({'customer': customer, 'site': site, 'dev_name': dev_name, 'dev_ip': dev_ip,
                                       'os': os_input, 'userid': userid, 'passwd': passwd,
                                       'salt_proxy_required': salt_proxy_required})
            return True
        else:
            print('Device already exist. Skipping line ', line_number)
            return False


def _check_values(line_value_list):
    """
    Verify the values of each field of the line being processed.

    :param line_value_list: contains the line transformed to a list

    :return: ``line_value_list`` with corrections, or ``False`` if the list has an invalid value.
    """

    if not line_value_list[0].isalnum() and len(line_value_list[0] < 20):
        return False
    else:
        line_value_list[0].lower().replace(' ', '_')

    if not line_value_list[1].isalnum() and len(line_value_list[1] < 20):
        return False
    else:
        line_value_list[1].lower().replace(' ', '_')

    if '-' in line_value_list[2]:
        test = line_value_list[2].split('-')
        for item in test:
            if not item.isalnum():
                return False
            else:
                if len(line_value_list[2]) < 18:
                    line_value_list[1].lower().replace(' ', '_')
                else:
                    return False
    else:
        if not (line_value_list[2].isalnum()) and len(line_value_list[2] < 18):
            return False
        else:
            line_value_list[1].lower().replace(' ', '_')

    try:
        ipaddress.ip_address(line_value_list[3])
    except ValueError:
        return False

    if not line_value_list[4].lower() in ["ios", "ios-xr", "nx-os", "eos", "junos"]:
        return False
    else:
        line_value_list[4] = line_value_list[4].lower()

    line_value_list[7] = line_value_list[7].strip('\n')
    if not line_value_list[7].lower() in ['y', 'n']:
        return False
    else:
        line_value_list[7] = line_value_list[7].lower()

    return line_value_list


def _import_csv(destination_db_to_import, csv_file_to_import):
    """
    Import the CSV to the DB

    :param destination_db_to_import: DB to import the CSV
    :param csv_file_to_import: the file to import to the DB

    :return: ``total_lines_number_processed`` and ``lines_imported``
    """
    total_lines_number_processed = 0
    lines_imported = 0

    for line in open(csv_file_to_import):
        total_lines_number_processed += 1
        values_list = line.split(',')
        if values_list[0] == 'customer':
            continue
        checked_line_values = _check_values(values_list)
        if len(values_list) == 8 and checked_line_values:
            x = ImportDevices(destination_db_to_import)
            if x.add_line_to_db(checked_line_values, total_lines_number_processed):
                lines_imported += 1
            else:
                pass
        else:
            print('Line number %i incorrect, skipping line.' % total_lines_number_processed)
            continue

    return total_lines_number_processed, lines_imported


def start_process():
    """
    Starts the process of import the CSV to DB, asking for the path names to the files.

    :return: Nothing
    """
    netorconf.check_netor_config(_NETOR_HOME_DIRECTORY)
    tinydb_log_file = _NETOR_HOME_DIRECTORY + "netor/log/tinydb.log"

    print('\nAvailable Databases:\n')
    for item in glob.glob(_NETOR_HOME_DIRECTORY + 'netor/tinydb/data/*.json'):
        print(item)
    select_db = input('\nSelect DB to upload the CSV. Copy full path to the DB, or Hit ENTER to use Current [' +
                      _DB_PATH_NAME + '] or \"new\" for a new DB: ').lower()

    if select_db == '':
        destination_db_to_import = _DB_PATH_NAME
    elif select_db == 'new':
        new_db = input('Enter new DB name. Example \"newdb.json\": ')
        if not ('.json' in new_db or not new_db.isalnum()):
            print('\nInvalid file name')
            exit(1)
        destination_db_to_import = _NETOR_HOME_DIRECTORY + 'netor/tinydb/data/' + new_db
        print('\nRemember to \"netor-db-switch\" in order to start using the data uploaded to the DB.')
    elif select_db in glob.glob(_NETOR_HOME_DIRECTORY + 'netor/tinydb/data/*.json'):
        destination_db_to_import = select_db
        print('\nRemember to \"netor-db-switch\" in order to start using the data uploaded to the DB.')
    else:
        print('\nInvalid file name')
        destination_db_to_import = ''
        exit(1)

    csv_file_to_import = input('Enter full path name to .CSV file to import (example: /full/path/name/file.csv): '). \
        lower()
    print()
    if not os.path.isfile(csv_file_to_import):
        print('\nFile not found')
        exit(1)
    else:
        total_lines_number_processed, lines_imported = _import_csv(destination_db_to_import, csv_file_to_import)
        print('\nFinished importing the file.')
        print('%i lines processed' % total_lines_number_processed)
        print('%i lines imported' % lines_imported)
        tinydblogging.log_msg(tinydb_log_file, __file__, 'CSV imported. ' + str(total_lines_number_processed) +
                              ' lines processed, and ' + str(lines_imported) + ' lines imported.')

    return


if __name__ == '__main__':
    start_process()
    print()
