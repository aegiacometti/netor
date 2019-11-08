from tinydb import TinyDB


class DbParam:
    """Startup common DB parameters and tables"""

    def __init__(self, db_path_name):
        self.db_path_name = db_path_name
        self.db = TinyDB(self.db_path_name, sort_keys=True, indent=4, separators=(',', ': '))
        self.table_customers = self.db.table('customers')
        self.table_sites = self.db.table('sites')
        self.table_devices = self.db.table('devices')
