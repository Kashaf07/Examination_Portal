from flask_mysqldb import MySQL


def init_mysql(app):
    app.config['MYSQL_HOST'] = '69.49.230.69:3306'
    app.config['MYSQL_USER'] = 'kiy_nuv_entrance'
    app.config['MYSQL_PASSWORD'] = 'bEWeNviz4mn*g^65'
    app.config['MYSQL_DB'] = 'admin_nuv_entrance'
    
    mysql = MySQL(app)
    return mysql
