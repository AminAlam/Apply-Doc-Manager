import sys
sys.path.append('../database')
import operators

def init_db(db_configs):
    print('Initilizing the databse')
    operators.create_table(db_configs.conn, db_configs.sql_create_table_universities)
    operators.create_table(db_configs.conn, db_configs.sql_create_table_supervisors)


def check_existence_table(db_configs):
    conn = db_configs.conn
    cursor = conn.cursor()
    #get the count of tables with the name
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name=? ''', ['universities'])
    #if the count is 1, then table exists
    if cursor.fetchone()[0]==1:
        open_bool = 1
    else:
        open_bool = 0
    return open_bool

def check_existence_university_in_universities(conn, name):
    cursor = conn.cursor()
    cursor.execute("SELECT rowid FROM universities WHERE name = ?", (name,))
    data=cursor.fetchall()
    if len(data)==0:
        print('There is no university named %s'%name)
        existence_bool = 0
    else:
        print('University %s found with rowids %s'%(name,','.join(map(str, next(zip(*data))))))
        existence_bool = 1
    return existence_bool

def check_existence_supervisor_in_supervisors(conn, email):
    cursor = conn.cursor()
    cursor.execute("SELECT rowid FROM supervisors WHERE email = ?", (email,))
    data=cursor.fetchall()
    if len(data)==0:
        print('There is no supervisor with email =  %s'%email)
        existence_bool = 0
    else:
        print('Supervisors with email %s found with rowids %s'%(email,','.join(map(str, next(zip(*data))))))
        existence_bool = 1
    return existence_bool