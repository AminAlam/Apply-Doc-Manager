import flask
from threading import Thread

class WebApp():
    def __init__(self, db_configs, ip, port, static_folder): 
        self.ip = ip
        self.port = port
        self.db_configs = db_configs
        self.app = flask.Flask(__name__, static_folder=static_folder)

    def run(self):    
        app = self.app
        @app.route('/')
        def index():
            cursor = self.db_configs.conn.cursor()
            cursor.execute('SELECT * FROM supervisors')
            universities = cursor.fetchall()
            print(universities)
            return flask.render_template('index.html', posts=universities)

        
        t = Thread(target=self.app.run, args=(self.ip,self.port,False))
        t.start()
