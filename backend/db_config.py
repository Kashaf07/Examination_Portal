from flask_mysqldb import MySQL


def init_mysql(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'Diamond@7115'
    app.config['MYSQL_DB'] = 'entrance_database'
    
    mysql = MySQL(app)
    return mysql
