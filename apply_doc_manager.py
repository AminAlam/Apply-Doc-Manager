import sys
sys.path.append('./database')
sys.path.append('./utils')
sys.path.append('./web')

import flask
import click
import os
import operators
import configs
import utils
import api

# dastabase configuration
db_configs = configs.database_configs()
if not utils.check_existence_table(db_configs):
    utils.init_db(db_configs)

# apply updates to the database (if exists)
utils.apply_updates2db(db_configs)

# Args parser from command line
@click.command()
@click.option('--server_ip', default='localhost', help='Server address')
@click.option('--port', default=8080, help='Port to run the server on')
@click.option('--static_folder', default='web', help='Folder with static files')
def setup_all(server_ip, port, static_folder):
    webapp = api.WebApp(db_configs, server_ip, port, static_folder)
    webapp.run()

if __name__ == '__main__':
    setup_all()

