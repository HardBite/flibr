from flask import Flask
from flask.ext.login import LoginManager
import database
#import app

app = Flask(__name__, static_url_path = '/static')
db = database.engine
app.config['SECRET_KEY'] = 'very-secret-key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/log_in"


from app import views
