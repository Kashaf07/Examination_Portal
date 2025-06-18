from flask import Flask
from flask_cors import CORS
from db_config import init_mysql
from routes.auth_routes import create_auth_routes  
from routes.question_routes import create_question_routes
from routes.exam_routes import create_exam_routes

app = Flask(__name__)
CORS(app)

mysql = init_mysql(app)

auth_bp = create_auth_routes(mysql)  
app.register_blueprint(auth_bp, url_prefix="/api/auth")

question_bp = create_question_routes(mysql)
app.register_blueprint(question_bp, url_prefix="/api/questions")

exam_bp = create_exam_routes(mysql)
app.register_blueprint(exam_bp, url_prefix="/api/exam")

if __name__ == "__main__":
    app.run(debug=True)
