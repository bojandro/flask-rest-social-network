from flask import Flask
from views import main_blueprint
from service.db import init_db
from config import (
    SECRET_KEY,
    DATABASE_CONNECTION_URI
)

def create_app():
    app = Flask(__name__)
    uri = DATABASE_CONNECTION_URI
    print(uri)

    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.register_blueprint(main_blueprint)
    init_db(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
