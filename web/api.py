from email import message
import errno
import sys
sys.path.append('../database')
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
            return flask.render_template('index.html', posts=universities)

        @app.route('/universities')
        def universities():
            cursor = self.db_configs.conn.cursor()
            cursor.execute('SELECT * FROM universities')
            universities = cursor.fetchall()
            return flask.render_template('universities.html', posts=universities)

        @app.route('/supervisors')
        def supervisors():
            cursor = self.db_configs.conn.cursor()
            cursor.execute('SELECT * FROM supervisors')
            universities = cursor.fetchall()
            return flask.render_template('supervisors.html', posts=universities)


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


        t = Thread(target=self.app.run, args=(self.ip,self.port,False))
        t.start()
