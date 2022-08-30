import sys
sys.path.append('../utils')

import utils
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        print('Connected to database using SQLite', sqlite3.version)
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_supervisor(conn, name, university, email, country, position_type, emailed, answer, interview, notes, email_date=None, rank=None, webpage=None):
    cursor = conn.cursor()
    existence_bool_supervisor = utils.check_existence_supervisor_in_supervisors(conn, email)
    if not existence_bool_supervisor:
        if emailed=='No':
            email_date = None
        rows = [(name, university, email, country, emailed, answer, interview, position_type, webpage, rank, notes, None, email_date)]
        cursor.executemany('insert into supervisors values (?,?,?,?,?,?,?,?,?,?,?,?,?)', rows)
        conn.commit()
        existence_bool_university = utils.check_existence_university_in_universities(conn, university)
        if not existence_bool_university:
            insert_university(conn, university, country, rank=rank)
        success_bool = 1
    else:
        success_bool = 0
    return success_bool

def edit_supervisor(conn, name, university, email, country, position_type, emailed, answer, interview, notes, id, email_date=None, rank=None, webpage=None):
    cursor = conn.cursor()

    cursor = conn.cursor()
    cursor.execute('select * from supervisors where id=?', (id,))
    supervisor_old = cursor.fetchone()

    rows = [(name, university, email, country, emailed, answer, interview, position_type, webpage, rank, notes, email_date, id)]
    cursor.executemany('''update supervisors set name=?, university=?, email=?, country=?, emailed=?, answer=?, interview=?,
                          position_type=?, webpage=?, university_rank=?, notes=?, email_date=? where id=?''', rows)
    conn.commit()
    existence_bool_university = utils.check_existence_university_in_universities(conn, university)
    if not existence_bool_university:
        insert_university(conn, university, country, rank=rank)
    else:
        update_university(conn, university, country, rank=rank)
    delete_university_with_no_supervisor(conn, university_name=supervisor_old[1])

def update_university(conn, name, country, rank=None):
    cursor = conn.cursor()
    rows = [(country, rank, name)]
    cursor.executemany('update universities set country=?, rank=? where name=?', rows)
    cursor.executemany('update supervisors set university_rank=? where university=?', [(rank, name)])
    conn.commit()



def delete_supervisor(conn, id):
    cursor = conn.cursor()
    cursor.execute('select * from supervisors where id=?', (id,))
    supervisor = cursor.fetchone()
    cursor.execute('delete from supervisors where id=?', (id,))
    conn.commit()

    delete_university_with_no_supervisor(conn, university_name=supervisor[1])

def insert_university(conn, name='sharif', country=None, rank=None):
    cursor = conn.cursor()
    rows = [(name, country, rank, None)]
    cursor.executemany('insert into universities values (?, ?, ?, ?)', rows)
    conn.commit()

def delete_university_with_no_supervisor(conn, university_name):
    cursor = conn.cursor()
    cursor.execute('select * from supervisors where university=?', (university_name,))
    supervisors = cursor.fetchall()
    print('ffff', supervisors)
    if len(supervisors)==0:
        cursor.execute('delete from universities where name=?', (university_name,))
        conn.commit()

