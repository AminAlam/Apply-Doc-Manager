from email import message
import errno
import sys
sys.path.append('../database')
sys.path.append('../utils')

import utils
import operators
import flask
from threading import Thread

class WebApp():
    def __init__(self, db_configs, ip, port, static_folder): 
        self.ip = ip
        self.port = port
        self.db_configs = db_configs
        self.app = flask.Flask(__name__, static_folder=static_folder)
        self.app.config['SECRET_KEY'] = 'evmermrefmwrf92i4=fi3fj2q4fj2M#RKM-!#$Km343FIJ!$Ifo943f-02f40-F-132-4fk!#$fi91f-'


    def run(self):    
        app = self.app
        @app.route('/')
        def index():
            cursor = self.db_configs.conn.cursor()
            cursor.execute('SELECT * FROM universities')
            universities = cursor.fetchall()

            cursor.execute('SELECT * FROM supervisors')
            supervisors = cursor.fetchall()

            info = utils.info(supervisors, universities)

            return flask.render_template('index.html', post=info)

        @app.route('/universities')
        def universities():
            cursor = self.db_configs.conn.cursor()
            cursor.execute('SELECT * FROM universities')
            universities = cursor.fetchall()
            for university_no in range(0,len(universities)):
                cursor.execute("SELECT rowid FROM supervisors WHERE university = ?", (universities[university_no][0],))
                num_supervisors = len(cursor.fetchall())
                universities[university_no] = universities[university_no]+(num_supervisors, )
            return flask.render_template('universities.html', posts=universities)

        @app.route('/supervisors')
        def supervisors():
            cursor = self.db_configs.conn.cursor()
            cursor.execute('SELECT * FROM supervisors')
            supervisors = cursor.fetchall()
            return flask.render_template('supervisors.html', posts=supervisors)

        
        @app.route('/<int:id>/supervisor')
        def supervisor(id):
            cursor = self.db_configs.conn.cursor()
            cursor.execute('SELECT * FROM supervisors where id = ?', (id,))
            supervisor = cursor.fetchall()
            print(supervisor)
            return flask.render_template('supervisor.html', posts=supervisor)


        @app.route('/insert_supervisor', methods=('GET', 'POST'))
        def insert_supervisor():
            return flask.render_template('insert_supervisor.html')

        @app.route('/insert_supervisor_to_db', methods=['GET', 'POST'])
        def insert_supervisor_to_db():
            if flask.request.method == 'POST':
                try:
                    name = flask.request.form['name']
                    university = flask.request.form['university']
                    email = flask.request.form['email']
                    country = flask.request.form['country']
                    webpage = flask.request.form['webpage']
                    position_type = flask.request.form['position_type']
                    university_rank = flask.request.form['university_rank']
                    emailed = flask.request.form['emailed']
                    answer = flask.request.form['answer']
                    interview = flask.request.form['interview']
                    notes = flask.request.form['notes']
                except:
                    flask.flash('Please Fill all the Forms')
                    return flask.redirect(flask.url_for('insert_supervisor'))

                if name == '' or university == '' or email == '' or country == '':
                    flask.flash('Please Fill all the Forms')
                    return flask.redirect(flask.url_for('insert_supervisor'))
                success_bool = operators.insert_supervisor(self.db_configs.conn, name, university, email, country,
                                webpage=webpage, position_type=position_type, rank=university_rank, 
                                emailed=emailed, answer=answer, interview=interview, notes=notes)

                if success_bool:
                    message = 'Supervisor is added successfully'
                else:
                    message = 'Supervisor already exists'

                flask.flash(message)
                print(message)
                return flask.redirect(flask.url_for('index'))


        @app.route('/<int:id>/edit_supervisor_in_db', methods=['GET', 'POST'])
        def edit_supervisor_in_db(id):
            if flask.request.method == 'POST':
                try:
                    name = flask.request.form['name']
                    university = flask.request.form['university']
                    email = flask.request.form['email']
                    country = flask.request.form['country']
                    webpage = flask.request.form['webpage']
                    position_type = flask.request.form['position_type']
                    university_rank = flask.request.form['university_rank']
                    emailed = flask.request.form['emailed']
                    answer = flask.request.form['answer']
                    interview = flask.request.form['interview']
                    notes = flask.request.form['notes']
                except:
                    flask.flash('Please Fill all the Forms')
                    return flask.redirect(flask.url_for('supervisor', id=id))

                if name == '' or university == '' or email == '' or country == '':
                    flask.flash('Please Fill all the Forms')
                    return flask.redirect(flask.url_for('supervisor', id=id))
                operators.edit_supervisor(self.db_configs.conn, name, university, email, country,
                                webpage=webpage, position_type=position_type, rank=university_rank, 
                                emailed=emailed, answer=answer, interview=interview, notes=notes, id=id)
            
                message = 'Supervisor is updated successfully'
                
                flask.flash(message)
                print(message)
                return flask.redirect(flask.url_for('supervisor', id=id))

        @app.route('/<int:id>/delete_supervisor_in_db', methods=['GET', 'POST'])
        def delete_supervisor_in_db(id):
            operators.delete_supervisor(self.db_configs.conn, id)
            message = 'Supervisor is deleted successfully'
            flask.flash(message)
            return flask.redirect(flask.url_for('supervisors'))

        t = Thread(target=self.app.run, args=(self.ip,self.port,False))
        t.start()
