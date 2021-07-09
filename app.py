from flask import Flask
from views import main_blueprint
from service.db import init_db
from config import (
    db_username,
    db_password,
    CONNECTOR,
    SECRET_KEY,
    DATABASE,
    LINK
)

def create_app():
    app = Flask(__name__)
    uri = f'{CONNECTOR}://{db_username}:{db_password}@{LINK}/{DATABASE}?charset=utf8mb4'

    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = uri

    app.register_blueprint(main_blueprint)
    init_db(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
