from flask import Flask
import database
#import app

app = Flask(__name__, static_url_path = '/static')
#app.config.from_object('config')
db = database.engine


from app import views