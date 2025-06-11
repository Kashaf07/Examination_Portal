from flask import Flask
from flask_cors import CORS
from db_config import init_mysql
from routes.auth_routes import create_auth_routes  

app = Flask(__name__)
CORS(app)

mysql = init_mysql(app)

auth_bp = create_auth_routes(mysql)  
app.register_blueprint(auth_bp, url_prefix="/api/auth")

if __name__ == "__main__":
    app.run(debug=True)
