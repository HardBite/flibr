import os

#needed for SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(basedir, 'app.db')






#needed for Flask-WTF
CSRF_ENABLED = True
SECRET_KEY = 'really-the-great-secret-key'