from flask import Flask
from flask_cors import CORS
from db_config import init_mysql
from routes.auth_routes import create_auth_routes  
from routes.exam_routes import create_exam_routes
from routes.AddStudents import add_students_bp



app = Flask(__name__)
CORS(app)

mysql = init_mysql(app)

auth_bp = create_auth_routes(mysql)  
app.register_blueprint(auth_bp, url_prefix="/api/auth")

exam_bp = create_exam_routes(mysql)
app.register_blueprint(exam_bp, url_prefix="/api/exam")

app.register_blueprint(add_students_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)


    