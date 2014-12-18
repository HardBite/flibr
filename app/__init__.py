from flask import Flask
import database
#import app

app = Flask(__name__)
#app.config.from_object('config')
db = database.engine


from app import views