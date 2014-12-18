from app import app

@app.route('/')
@app.route('/index')
def index():
  return 'Hello World!'

@app.route('/sign_up')
def sign_up():
  pass

@app.route('/log_in')
def log_in():
  pass


