import os


#needed for SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(basedir, 'app.db')
#windows DB path:
#SQLALCHEMY_DATABASE_URI = 'sqlite:///D:\\prg\\flibr\\flibr\\app\\app.db'





#needed for Flask-WTF
CSRF_ENABLED = True
SECRET_KEY = 'really-the-great-secret-key'