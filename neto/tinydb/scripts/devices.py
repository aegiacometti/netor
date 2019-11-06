from tinydb import Query
import ipaddress
import dbparam


class Devices(dbparam.DbParam):
    """
    Devices worker to operate DB on table ``devices`` (list, add, modify and delete methods).

    Device names has to be alphanumeric and less than 20 characters. At the DB all the spaces ``" "`` will be replaced
    by underscores ``"_"``.
    """

    @staticmethod
    def check_value(value):
        """
        Verifies the value to be alphanumeric string and less than 20 characters.

        :param value: string to verify
        :return: ``True`` if the value is a valid string otherwise returns ``False``
        """
        if '-' in value:
            test = value.split('-')
            for item in test:
                if not item.isalnum():
                    return False
                else:
                    if len(value) < 20:
                        return True
                    else:
                        return False
        else:
            if value.isalnum() and len(value) < 20:
                return True
            else:
                return False

    def list(self):
        """
        List the table ``devices`` ordered alphabetically, and filtered according the selected options (customer, site,
        IP, device name, or OS.

        :return: ``True`` if the devices were listed, or ``False`` if there is no match between the conditions selected.
        """
        print("LIST DATABASE")
        print("List Devices")
        q = input("All devices or per customer (1.- all , 2.- p/customer, 3.- p/customer & Site:, 4.- IP, name, os): ")
        if q == "1":
            db_devices = sorted(self.table_devices.all(), key=lambda x: (x['customer'], x['site'], x['dev_name']))
        elif q == "2":
            customer = input("Customer name: ")
            customer = customer.replace(' ', '_')
            query_per_customer = Query().customer == customer
            db_devices = sorted(self.table_devices.search(query_per_customer), key=lambda x: (x['customer'], x['site'],
                                                                                              x['dev_name']))
            if not db_devices:
                print("\nCustomer do no exist or no data found")
                return False
        elif q == "3":
            customer = input("Customer name: ")
            customer = customer.replace(' ', '_')
            query_per_customer = Query().customer == customer
            db_devices = sorted(self.table_devices.search(query_per_customer), key=lambda x: (x['customer'], x['site'],
                                                                                              x['dev_name']))
            if not db_devices:
                print("\nCustomer do no exist")
                return False
            site = input("Site name: ")
            site = site.replace(' ', '_')
            query_per_customer_site = (Query().customer == customer) & (Query().site == site)
            db_devices = sorted(self.table_devices.search(query_per_customer_site),
                                key=lambda x: (x['customer'], x['site'], x['dev_name']))
            if not db_devices:
                print("\nSite do no exist")
                return False
        elif q == "4":
            os_list = ["ios", "ios-xr", "nx-os", "eos", "jnos"]
            string = input("Enter device IP, name, or OS " + str(os_list) + ": ")
            query_ip = Query().dev_ip == string
            query_name = Query().dev_name == string
            query_os = Query().os == string
            db_devices = sorted(self.table_devices.search(query_ip | query_name | query_os),
                                key=lambda x: (x['customer'], x['site'], x['dev_name']))
            if not db_devices:
                print("\nNo data found")
                return False
        else:
            return False
        print('\n%-22s %-22s %-20s %-17s %-11s %-20s %-20s %-16s' % ('Customer Name', 'Site Name', 'Device Name',
                                                                     'Device IP', 'Device OS', 'User Name',
                                                                     'Password', 'Req Slat Proxy'))
        for item in db_devices:
            print('%-22s %-22s %-20s %-17s %-11s %-20s %-20s %-16s' % (item['customer'].replace('_', ' '),
                                                                       item['site'].replace('_', ' '), item['dev_name'],
                                                                       item['dev_ip'], item['os'], item['userid'],
                                                                       item['passwd'], item['salt_proxy_required']))
        return True

    def add(self):
        """
        Add a *device*.

        :return: ``Dev_name`` added or ``False`` if there was an error.
        """
        print("ADD DEVICE TO CUSTOMER AND SITE")
        customer = input("Customer Name: ")
        customer = customer.replace(' ', '_')
        query_customer = Query().customer == customer
        res = self.table_customers.search(query_customer)
        if not res:
            print("\nCustomer do not exist")
            print()
            return False
        else:
            site = input("Site Name: ")
            site = site.replace(' ', '_')
            query_site = Query().site == site
            res = self.table_sites.search(query_customer & query_site)
            if not res:
                print("\nSite do not exist")
            else:
                dev_ip = input("Device IP: ")
                try:
                    ipaddress.ip_address(dev_ip)
                except ValueError:
                    print("\nInvalid IP")
                    return False
                if self.table_devices.search(query_site & query_customer & (Query().dev_ip == dev_ip)):
                    print("\nDevice IP already exist")
                    return False
                dev_name = input("Device name: ")
                dev_name = dev_name.replace(' ', '_')
                if self.table_devices.search(query_site & query_customer & (Query().dev_name == dev_name)):
                    print("\nDevice Name already exist")
                    return False
                os_list = ["ios", "ios-xr", "nx-os", "eos", "jnos"]
                os_input = input("Operating System " + str(os_list) + ": ")
                if os_input not in os_list:
                    print("\nOS not in list")
                    return False
                userid = input("User id (def: cisco): ")
                passwd = input("Password (def: cisco): ")
                if userid == '':
                    userid = "cisco"
                if passwd == '':
                    passwd = "cisco"
                salt_proxy_required = input("Salt proxy required (y/n): ").lower()
                if not (salt_proxy_required == "y" or salt_proxy_required == "n"):
                    print("\nInvalid option\n")
                    return False
                self.table_devices.insert({'customer': customer, 'site': site, 'dev_name': dev_name, 'dev_ip': dev_ip,
                                           'os': os_input, 'userid': userid, 'passwd': passwd,
                                           'salt_proxy_required': salt_proxy_required})
                print("\nDevice added")
                return dev_name

    def modify(self):
        """
        Modify a *device*.

        :return: ``Dev_name`` original and ``new_dev_name`` of the modified device, or ``False`` if there was an error.
        """
        print("MODIFY DEVICE FROM CUSTOMER AND SITE")
        customer = input("Customer Name: ")
        customer = customer.replace(' ', '_')
        query_customer = Query().customer == customer
        res = self.table_customers.search(query_customer)
        if not res:
            print("Customer do not exist")
            return False
        else:
            site = input("Site Name: ")
            site = site.replace(' ', '_')
            query_site = Query().site == site
            res = self.table_sites.search(query_customer & query_site)
            if not res:
                print("\nSite do not exist")
                return False
            else:
                dev_ip = input("Device IP: ")
                try:
                    ipaddress.ip_address(dev_ip)
                except ValueError:
                    print("\nInvalid IP")
                    return False
                if not self.table_devices.search(query_site & query_customer & (Query().dev_ip == dev_ip)):
                    print("\nDevice IP do not exist")
                    return False
                dev_name = input("Device name: ")
                if dev_name == "":
                    print("\nNo device name introduced")
                    return False
                if not self.table_devices.search(query_site & query_customer & (Query().dev_name == dev_name) &
                                                 (Query().dev_ip == dev_ip)):
                    print("\nDevice IP or Name do not match")
                    return False
                modified_device = self.table_devices.search(query_site & query_customer & (Query().dev_name == dev_name)
                                                            & (Query().dev_ip == dev_ip))
                query_new_dev_ip = input("New Device IP [" + modified_device[0]['dev_ip'] + "]: ")
                if query_new_dev_ip == "":
                    new_dev_ip = modified_device[0]['dev_ip']
                else:
                    try:
                        ipaddress.ip_address(query_new_dev_ip)
                        new_dev_ip = query_new_dev_ip
                    except ValueError:
                        print("\nInvalid IP")
                        return False
                if not dev_ip == new_dev_ip:
                    if self.table_devices.search(query_site & query_customer & (Query().devIP == new_dev_ip)):
                        print("\nDevice IP already exist")
                        return False
                new_dev_name = input("New Device name [" + modified_device[0]['dev_name'] + "]: ")
                if new_dev_name == "":
                    new_dev_name = modified_device[0]['dev_name']
                new_dev_name = new_dev_name.replace(' ', '_')
                if dev_name == new_dev_name:
                    if self.table_devices.search(query_site & query_customer & (Query().devName == new_dev_name)):
                        print("\nDevice Name already exist")
                        return False
                os_list = ["ios", "ios-xr", "nx-os", "eos", "jnos"]
                new_os = input("New Operating System [current: " + modified_device[0]['os'] + "] or new " +
                               str(os_list) + ": ")
                if new_os == "":
                    new_os = modified_device[0]['os']
                if new_os not in os_list:
                    print("\nOS not in list")
                    return False
                new_userid = input("New User id [" + modified_device[0]['userid'] + "]: ")
                if new_userid == "":
                    new_userid = modified_device[0]['userid']
                new_passwd = input("New Password [" + modified_device[0]['passwd'] + "]: ")
                if new_passwd == "":
                    new_passwd = modified_device[0]['passwd']

                try:
                    new_salt_proxy_required = input("Salt proxy required current [" +
                                                    modified_device[0]['salt_proxy_required'] +
                                                    "] select (y/n): ").lower()
                except KeyError:
                    new_salt_proxy_required = input(
                        "Salt proxy required current [null] select (y/n): ").lower()

                if new_salt_proxy_required == "":
                    try:
                        new_salt_proxy_required = modified_device[0]['salt_proxy_required']
                    except KeyError:
                        new_salt_proxy_required = "n"
                if not (new_salt_proxy_required == "y" or new_salt_proxy_required == "n"):
                    print("\nInvalid option")
                    return False
                self.table_devices.update({'customer': customer, 'site': site, 'dev_name': new_dev_name,
                                           'dev_ip': new_dev_ip, 'os': new_os, 'userid': new_userid,
                                           'passwd': new_passwd, 'salt_proxy_required': new_salt_proxy_required},
                                          (query_site & query_customer & (Query().dev_ip == dev_ip) &
                                           (Query().dev_name == dev_name)))
                print("\nDevice modified")
                return new_dev_name

    def delete(self):
        """
        Delete a *device*.

        :return: ``dev_name`` of the delete device, or ``False`` it there was an error.
        """
        print("DELETE DEVICE FROM CUSTOMER AND SITE")
        customer = input("Customer Name: ")
        customer = customer.replace(' ', '_')
        if not self.check_value(customer):
            print("\nInvalid customer name")
            return False
        query_customer = Query().customer == customer
        res = self.table_customers.search(query_customer)
        if not res:
            print("\nCustomer do not exist")
            return False
        else:
            site = input("Site Name: ")
            site = site.replace(' ', '_')
            if not self.check_value(site):
                print('\nInvalid site name')
                return False
            query_site = Query().site == site
            res = self.table_sites.search(query_customer & query_site)
            if not res:
                print("\nSite do not exist")
            else:
                dev_ip = input("Device IP: ")
                try:
                    ipaddress.ip_address(dev_ip)
                except ValueError:
                    print("\nInvalid IP")
                    return False
                dev_name = input("Device name: ")
                dev_name = dev_name.replace(' ', '_')
                if dev_name == "":
                    print("\nNo device name introduced")
                    return False
                query_device = query_site & query_customer & ((Query().dev_name == dev_name) &
                                                              (Query().dev_ip == dev_ip))
                if not self.table_devices.search(query_device):
                    print("\nDevice name or IP not found")
                    return False
                self.table_devices.remove(query_device)
                print("\nDevice deleted")
                return dev_name
