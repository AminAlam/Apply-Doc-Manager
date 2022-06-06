import sys
sys.path.append('../database')
import operators

def init_db(db_configs):
    print('Initilizing the databse')
    operators.create_table(db_configs.conn, db_configs.sql_create_table_universities)
    operators.create_table(db_configs.conn, db_configs.sql_create_table_supervisors)


def check_existence_table(db_configs):
    conn = db_configs.conn
    c = conn.cursor()
    #get the count of tables with the name
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name=? ''', ['universities'])
    #if the count is 1, then table exists
    if c.fetchone()[0]==1:
        open_bool = 1
    else:
        open_bool = 0
    return open_bool