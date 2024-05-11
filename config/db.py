from flaskext.mysql import MySQL

class Database:
    def __init__(self, app):
        self.mysql = MySQL()
        app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        app.config['MYSQL_DATABASE_USER'] = 'root'
        app.config['MYSQL_DATABASE_PASSWORD'] = ''
        app.config['MYSQL_DATABASE_DB'] = 'sitio'
        self.mysql.init_app(app)

    def connect(self):
        return self.mysql.connect()
