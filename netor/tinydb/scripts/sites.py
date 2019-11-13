from tinydb import Query
import dbparam


class Sites(dbparam.DbParam):
    """
    Sites worker to operate DB on table sites (list, add, modify and delete methods).

    Site name has to be alphanumeric and less than 20 characters. At the DB all the spaces ``" "`` will be replaced
    by underscores ``"_"``.
    """

    @staticmethod
    def _check_value(value):
        """
        Verifies the value to be alphanumeric string, and less than 20 characters.

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
        List the table ``sites`` ordered alphabetically, and filtered by customer if that option was selected.

        :return: ``True`` if the site was listed or ``False`` if the customer do not exists.
        """
        print("LIST DATABASE")
        print("List Sites")
        q = input("All sites or per customer (1.- all , 2.- p/customer): ")
        if q == "1":
            db_sites = sorted(self.table_sites.all(), key=lambda x: (x['customer'], x['site']))
        elif q == "2":
            customer = input("Customer name: ")
            customer = customer.replace(' ', '_')
            query_per_customer = Query().customer == customer
            db_sites = sorted(self.table_sites.search(query_per_customer), key=lambda x: (x['customer'], x['site']))
            if not db_sites:
                print("\nCustomer do no exist")
                return False
        else:
            print("\nInvalid option")
            return False
        print('\n%-23s %-23s' % ('Customer Name', 'Site Name'))
        for item in db_sites:
            print('%-23s %-23s' % (item['customer'].replace('_', ' '), item['site'].replace('_', ' ')))
        return True

    def add(self):
        """
        Add a *site*.

        :return: ``Site`` name added or ``False`` if the parent Customer do not exists, or the site already exists.
        """
        print("ADD SITE TO CUSTOMER")
        customer = input("Customer Name: ")
        customer = customer.replace(' ', '_')
        if not self._check_value(customer):
            return False
        query_customer = Query().customer == customer
        res = self.table_customers.search(query_customer)
        if not res:
            print("\nCustomer do not exist")
            print()
            return False
        else:
            site = input("Site Name: ")
            site = site.replace(' ', '_')
            query_site = Query().sites.any(Query().site == site)
            res = self.table_sites.search(query_customer & query_site)
            if res:
                print("\nSite already exist")
                return False
            else:
                self.table_sites.insert({'customer': customer, 'site': site})
                print("\nSite added")
                return site

    def modify(self):
        """
        Modify a *site*.

        :return: ``Site`` original name and ``new_name`` name, or ``False`` if there is with parent Customer or site
        """
        print("MODIFY SITE FROM CUSTOMER")
        customer = input("Customer Name: ")
        customer = customer.replace(' ', '_')
        if not self._check_value(customer):
            return False
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
                return False
            else:
                site_new_name = input("Site New Name: ")
                site_new_name = site_new_name.replace(' ', '_')
                if not self._check_value(customer):
                    print("\nInvalid customer new name")
                    return False
                if self.table_sites.search(query_customer & (Query().site == site_new_name)):
                    print("\nSite already exist")
                    return False
                self.table_sites.update({'site': site_new_name}, (query_customer & query_site))
                self.table_devices.update({'site': site_new_name}, (query_customer & query_site))
                print("\nSite modified")
                return [site, site_new_name]

    def delete(self):
        """
        Delete a *site*.

        :return: ``Site`` name deleted or ``False`` if the site do not exists.
        """
        print("DELETE SITE FROM CUSTOMER")
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
                return False
            else:
                self.table_sites.remove(query_customer & query_site)
                self.table_devices.remove(query_customer & query_site)
                print("\nSite deleted")
                return site
