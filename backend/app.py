from flask import Flask
from flask_cors import CORS
from db_config import init_mysql
from routes.auth_routes import create_auth_routes  
from routes.question_routes import create_question_routes
from routes.exam_routes import create_exam_routes
from routes.AddStudents import add_students_bp
from routes.ExamNotification import exam_notify_bp
from routes.applicants import create_applicants_bp
from routes.AddApplicants_exam import create_add_applicants_exam_bp
from routes.assign_applicants import create_assign_routes

app = Flask(__name__)
CORS(app)

mysql = init_mysql(app)

auth_bp = create_auth_routes(mysql)  
app.register_blueprint(auth_bp, url_prefix="/api/auth")

question_bp = create_question_routes(mysql)
app.register_blueprint(question_bp, url_prefix="/api/questions")

exam_bp = create_exam_routes(mysql)
app.register_blueprint(exam_bp, url_prefix="/api/exam")

app.register_blueprint(add_students_bp, url_prefix="/api")

app.register_blueprint(exam_notify_bp)

app.register_blueprint(create_add_applicants_exam_bp(mysql), url_prefix='/api')

app.register_blueprint(create_assign_routes(mysql))

applicants_bp = create_applicants_bp(mysql)
app.register_blueprint(applicants_bp)

if __name__ == "__main__":
    app.run(debug=True)