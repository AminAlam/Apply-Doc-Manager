import sys
sys.path.append('./database')
sys.path.append('./utils')
sys.path.append('./web')

import os
import operators
import configs
import utils
import flask
import api

port = 8080
ip = 'localhost'
static_folder = './web'

db_configs = configs.database_configs()

if not utils.check_existence_table(db_configs):
    utils.init_db(db_configs)

if __name__ == '__main__':
    webapp = api.WebApp(db_configs, ip, port, static_folder)
    webapp.run()

