import sys
import requests
import os
sys.path.append('../database')
import operators

from datetime import datetime, date

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


def info(supervisors, universities):
    num_of_supervisors = len(supervisors)
    num_of_universities = len(universities)
    num_email_sent = 0
    num_good_answers = 0
    num_bad_answers = 0
    num_scheduled_interviews = 0
    num_bad_interviews = 0
    num_good_interviews = 0
    num_msc_positions = 0
    num_phd_positions = 0

    for supervisor in supervisors:
        if supervisor[4] == 'Yes':
            num_email_sent += 1
        if supervisor[5] == 'Good':
            num_email_sent += 1
            num_good_answers += 1
        elif supervisor[5] == 'Bad':
            num_email_sent += 1
            num_bad_answers += 1
        
        if supervisor[6] == 'Scheduled':
            num_scheduled_interviews += 1
        elif supervisor[6] == 'Bad':
            num_bad_interviews += 1
        elif supervisor[6] == 'Good':
            num_good_interviews += 1

        if supervisor[7] == 'MSc':
            num_msc_positions = num_msc_positions + 1
        elif supervisor[7] == 'PHD':
            num_phd_positions = num_phd_positions + 1

    return [num_of_supervisors, num_of_universities, num_email_sent, 
            num_good_answers, num_bad_answers, num_scheduled_interviews, 
            num_bad_interviews, num_good_interviews, num_msc_positions, 
            num_phd_positions]

def calc_difference_dates(date_email):
    date1 = date.today()
    # conver str to datetime
    date2 = datetime.strptime(date_email, "%Y-%m-%d").date()
    diff =  date1 - date2
    return diff.days

def apply_updates2db(db_configs):
    # add email_date to the database
    cursor = db_configs.conn.cursor()
    cursor.execute('SELECT * FROM universities')
    cursor.execute('SELECT * FROM supervisors')
    column_names = list(map(lambda x: x[0], cursor.description))
    if 'email_date' not in column_names:
        cursor.execute('ALTER TABLE supervisors ADD COLUMN email_date timestamp')

def check_for_update():
    if check_for_internet_connection():
        readme_url = 'https://github.com/MohammadAminAlamalhoda/Apply-Doc-Manager/blob/dev/updates/update.txt'
        readme_response = requests.get(readme_url)
        text_repo = readme_response.text                   
        text_local = os.popen('cat updates/update.txt').read()

        print(text_local)
        if text_local not in text_repo:
            return True
        else:
            return False
    else:
        return False


def check_for_internet_connection():
    try:
        requests.get('http://www.google.com')
        return True
    except requests.ConnectionError:
        return False