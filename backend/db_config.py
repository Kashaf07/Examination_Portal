import os
from flask_mysqldb import MySQL

def init_mysql(app):
    app.config['MYSQL_HOST'] = os.getenv('DB_HOST', '127.0.0.1')
    app.config['MYSQL_PORT'] = int(os.getenv('DB_PORT', 3306))
    app.config['MYSQL_USER'] = os.getenv('DB_USER', 'root')
    app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD', 'root')
    app.config['MYSQL_DB'] = os.getenv('DB_NAME', 'entrance_database')

    return MySQL(app)