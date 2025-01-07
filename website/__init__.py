from flask import Flask

def create_app():
    "create flask application with a secret key"
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'acedemo'

    from .views import views
    from .auth import auth
    
    "register blueprint"
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    
    return app
