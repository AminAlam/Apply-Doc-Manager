import sys
sys.path.append('../database')
sys.path.append('../utils')

import utils
import operators
import flask
from threading import Thread
import csv

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
            update_bool = utils.check_for_update()
            if update_bool:
                message = "There is an update available, pull it from the <a href='https://github.com/MohammadAminAlamalhoda/Apply-Doc-Manager' class='alert-link'>Github repo</a>!"
                flask.flash(flask.Markup(message))
            if not utils.check_for_internet_connection():
                message = "There is no internet connection, note that some CSS files may not be loaded completely."
                flask.flash(flask.Markup(message), 'error')
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
            filters = ['Default']
            return flask.render_template('universities.html', posts=universities, filters=filters)

        @app.route('/<int:id>/university')
        def university(id):
            cursor = self.db_configs.conn.cursor()
            cursor.execute('SELECT * FROM universities WHERE id = ?', (id,))
            university = cursor.fetchone()
            university_name = university[0]
            cursor.execute('SELECT * FROM supervisors WHERE university = ?', (university_name,))
            supervisors = cursor.fetchall()
            for supervisor_no, supervisor in enumerate(supervisors):
                if supervisor[4] == 'Yes':
                    diff = utils.calc_difference_dates(supervisor[12])
                    supervisor = list(supervisor)
                    supervisor[4] = '{0} Days ago'.format(diff)
                    supervisors[supervisor_no] = tuple(supervisor)
            return flask.render_template('university.html', posts=supervisors)

        @app.route('/supervisors')
        def supervisors():
            cursor = self.db_configs.conn.cursor()
            cursor.execute('SELECT * FROM supervisors')
            supervisors = cursor.fetchall()
            supervisors = utils.email_date_check(supervisors)
            filters = ['All', 'All', 'All', 'All']
            return flask.render_template('supervisors.html', posts=supervisors, filters=filters)

        @app.route('/supervisors_format', methods=['GET', 'POST'])
        def supervisors_format():
            if flask.request.method == 'POST':
                emailed = flask.request.form['emailed']
                answered = flask.request.form['answered']
                interview = flask.request.form['interview']
                position_type = flask.request.form['position_type']

                sql_command = 'SELECT * FROM supervisors WHERE ' 
                infos = []
                if emailed != 'All':
                    sql_command = sql_command + 'emailed=? AND '
                    infos.append(emailed)
                if answered != 'All':
                    sql_command = sql_command + 'answer=? AND '
                    infos.append(answered)
                if interview != 'All':
                    sql_command = sql_command + 'interview=? AND '
                    infos.append(interview)
                if position_type != 'All':
                    sql_command = sql_command + 'position_type=? AND '
                    infos.append(position_type)
                sql_command = sql_command + '1'
                cursor = self.db_configs.conn.cursor()
                infos = tuple(infos)
                cursor.execute(sql_command, infos)
                supervisors = cursor.fetchall()
                supervisors = utils.email_date_check(supervisors)
                filters = [emailed, answered, interview, position_type]
                return flask.render_template('supervisors.html', posts=supervisors, filters=filters)

        @app.route('/<int:id>/supervisor')
        def supervisor(id):
            cursor = self.db_configs.conn.cursor()
            cursor.execute('SELECT * FROM supervisors where id = ?', (id,))
            supervisors = cursor.fetchall()
            return flask.render_template('supervisor.html', posts=supervisors)

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
                    email_date = flask.request.form['email_date_value']
                except:
                    flask.flash('Please Fill all the Forms')
                    return flask.redirect(flask.url_for('insert_supervisor'))

                if name == '' or university == '' or email == '' or country == '':
                    flask.flash('Please Fill all the Forms')
                    return flask.redirect(flask.url_for('insert_supervisor'))
                success_bool = operators.insert_supervisor(self.db_configs.conn, name, university, email, country,
                                webpage=webpage, position_type=position_type, rank=university_rank, 
                                emailed=emailed, answer=answer, interview=interview, notes=notes,
                                email_date=email_date)

                if success_bool:
                    message = 'Supervisor is added successfully'
                else:
                    message = 'Supervisor already exists'

                flask.flash(message)
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
                    email_date = flask.request.form['email_date_value']
                except:
                    flask.flash('Please Fill all the Forms')
                    return flask.redirect(flask.url_for('supervisor', id=id))

                if name == '' or university == '' or email == '' or country == '':
                    flask.flash('Please Fill all the Forms')
                    return flask.redirect(flask.url_for('supervisor', id=id))
                operators.edit_supervisor(self.db_configs.conn, name, university, email, country,
                                webpage=webpage, position_type=position_type, rank=university_rank, 
                                emailed=emailed, answer=answer, interview=interview, notes=notes, id=id,
                                email_date=email_date)
            
                message = 'Supervisor is updated successfully'
                flask.flash(message)
                return flask.redirect(flask.url_for('supervisor', id=id))

        @app.route('/<int:id>/delete_supervisor_in_db', methods=['GET', 'POST'])
        def delete_supervisor_in_db(id):
            operators.delete_supervisor(self.db_configs.conn, id)
            message = 'Supervisor is deleted successfully'
            flask.flash(message)
            return flask.redirect(flask.url_for('supervisors'))

        @app.route('/universities_format', methods=['GET', 'POST'])
        def universities_format():
            rank = flask.request.form['rank']
            if rank == 'Default':
                cursor = self.db_configs.conn.cursor()
                cursor.execute('SELECT * FROM universities')
                filters = ['Default']
            elif rank == 'Ascending':
                cursor = self.db_configs.conn.cursor()
                cursor.execute('SELECT * FROM universities ORDER BY rank ASC')
                filters = ['Ascending']
            else:
                cursor = self.db_configs.conn.cursor()
                cursor.execute('SELECT * FROM universities ORDER BY rank DESC')
                filters = ['Descending']
            universities = cursor.fetchall()

            for university_no in range(0,len(universities)):
                cursor.execute("SELECT rowid FROM supervisors WHERE university = ?", (universities[university_no][0],))
                num_supervisors = len(cursor.fetchall())
                universities[university_no] = universities[university_no]+(num_supervisors, )

            return flask.render_template('universities.html', posts=universities, filters=filters)

        @app.route('/export_csv')
        def export_csv():
            cursor = self.db_configs.conn.cursor()
            cursor.execute('SELECT * FROM supervisors')
            supervisors = cursor.fetchall()
            file_name = 'supervisors.csv'
            with open('web/'+file_name, 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Name', 'University', 'Email', 'Country', 'Emailed?', 'Answered?', 'Interviewed?', 'Position Type', 'Webpage', 'Univerity Rank', 'Notes', 'ID', 'Email Date'])
                for supervisor in supervisors:
                    writer.writerow(supervisor)
            send_file(file_name)
            flask.flash(flask.Markup("CSV file is exported successfully! File is located at: <a href='"+file_name+"' download class='alert-link'>here </a>"))
            return flask.redirect(flask.url_for('index'))

        @app.route("/<path:filename>")
        def static_dir(filename):
            return flask.send_from_directory(app.root_path, filename)

        # flask send file for download
        @app.route('/<path:path>')
        def send_file(path):
            # flask send file to browser for download
            return flask.send_from_directory(app.root_path, path, as_attachment=True)




        t = Thread(target=self.app.run, args=(self.ip,self.port,False))
        t.start()        
