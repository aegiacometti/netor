from tinydb import Query
import dbparam


class Customers(dbparam.DbParam):
    """
    Customer worker to operate DB on table ``customers`` (list, add, modify and delete methods).

    Customer name has to be alphanumeric and less than 20 characters. At the DB all the spaces ``" "`` will be replaced
    by underscores ``"_"``.
    """

    @staticmethod
    def _check_value(value):
        """
        Verifies the value to be alphanumeric string, and less than 20 characters
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
        List the table ``customers`` ordered alphabetically.

        :return: True
        """
        print("LIST DATABASE")
        print("List Customers")
        print('\nCustomer Name')
        db_customers = sorted(self.table_customers.all(), key=lambda x: (x['customer']))
        for item in db_customers:
            print(item['customer'].replace('_', ' '))
        return True

    def add(self):
        """
        Add a *customer*.

        :return: ``Customer`` name added or ``False`` if the customer already exists.
        """
        print("ADD NEW CUSTOMER")
        customer = input("Customer Name (Only alphanumeric values and less than 20 characters): ")
        query_customer = Query().customer == customer
        res = self.table_customers.search(query_customer)
        customer = customer.replace(' ', '_')
        if res:
            print("\nCustomer already exist")
            return False
        else:
            if not self._check_value(customer):
                print('\nInvalid customer name')
                return False
            else:
                self.table_customers.insert({'customer': customer})
                print("\nCustomer added")
                return customer

    def modify(self):
        """
        Modify a *customer*.

        :return: ``Customer`` original name and ``new_name``, or ``False`` if the customer do not exists.
        """
        print("MODIFY CUSTOMER")
        customer = input("Customer Name: ")
        customer = customer.replace(' ', '_')
        query_customer = Query().customer == customer
        res = self.table_customers.search(query_customer)
        if not res:
            print("\nCustomer do not exist")
            return False
        else:
            new_customer = input("New customer name (Only alphanumeric values and less than 20 characters): ")
            new_customer = new_customer.replace(' ', '_')
            if new_customer == "":
                print("\nNo name introduced")
                print()
                return False
            if not self._check_value(new_customer):
                print('\nInvalid customer name')
                return False
            if self.table_customers.search(Query().customer == new_customer):
                print("\nCustomer already exist")
                return False
            self.table_customers.update({'customer': new_customer}, query_customer)
            self.table_sites.update({'customer': new_customer}, query_customer)
            self.table_devices.update({'customer': new_customer}, query_customer)
            print("\nCustomer modified")
            return [customer, new_customer]

    def delete(self):
        """
        Delete a *customer*.

        :return: ``Customer`` name deleted or ``False`` if the customer already exists.
        """
        print("DELETE CUSTOMER")
        customer = input("Customer Name: ")
        customer = customer.replace(' ', '_')
        query_customer = Query().customer == customer
        res = self.table_customers.search(query_customer)
        if not res:
            print("\nCustomer do not exist")
            return False
        else:
            self.table_customers.remove(query_customer)
            self.table_sites.remove(query_customer)
            self.table_devices.remove(query_customer)
            print("\nCustomer deleted")
            return customer
