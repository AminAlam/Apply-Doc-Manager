# test cases for the main module
import sys

sys.path.append('./database')
sys.path.append('./utils')
sys.path.append('./web')

import unittest
import os
import tempfile
import api
import configs

class db_initialization(unittest.TestCase):
    def setUp(self):
        print("-- In method {0}\n".format(self._testMethodName))
        self.db_configs = configs.database_configs()
        self.db_configs.dbName = tempfile.mktemp()
        self.db_configs.make_conn()
        self.server_ip = 'localhost'
        self.port = 8080
        self.static_folder = 'web'
        self.webapp = api.WebApp(self.db_configs, self.server_ip, self.port, self.static_folder)

    def test_run(self):
        self.webapp.run()

    def tearDown(self):
        self.db_configs.conn.close()
        os.remove(self.db_configs.dbName)

if __name__ == '__main__':
    unittest.main()