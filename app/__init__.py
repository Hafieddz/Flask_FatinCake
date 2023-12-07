from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

from .extension import db
from .routes.admin.routes import admin
from .routes.user.routes import main  
from .models.models import Users

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://fatincake:fatin2cake_@localhost/fatin_blueprint'
    app.config['SECRET_KEY'] = "this is very secret"
    
    db.init_app(app)
    app.register_blueprint(main)
    app.register_blueprint(admin)
    migrate = Migrate(app, db)

    app.app_context().push() 
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.index'
    
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    return app