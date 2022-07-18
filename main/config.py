from main import app

class Config_db :
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_user.db'

from datetime import timedelta
class Config_app :
    app.config['SECRET_KEY'] = 'SECRET KEY'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    ACCESS_EXPIRES = timedelta(hours=1)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES

