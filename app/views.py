from app import app
from flask import render_template, request, json
from models import Book, BookForm, Author, AuthorForm


def add_or_resubmit(request, obj, form, submit_template_path, success_template_path):
  print 'redirect request to add_of_resubmit'
  error=None
  if request.method == 'POST':
    print 'POST method detected'
    print 'request.form', request.form
    form.populate_obj(obj)
    is_submitted = obj.save_or_error()
    if is_submitted==True:
      return render_template(success_template_path)
    else:
      error = is_submitted
      return render_template(submit_template_path, form=form, error=error)
  else:
    print 'GET method detected'
    return render_template(submit_template_path, form=form, error=error)


@app.route('/')
@app.route('/index')
def index():
  return render_template('base.html')

@app.route('/sign_up')
def sign_up():
  pass

@app.route('/log_in')
def log_in():
  pass

@app.route('/add_book', methods = ['GET', 'POST'])
def add_book(book=None):
  print 'call to add_book recieved'
  book = book or Book()
  book_form = BookForm(request.form, obj=book)
  return add_or_resubmit(request, book, book_form, 'add_book.html', 'base.html')

@app.route('/add_author', methods = ['GET', 'POST'])
def add_author():
  author = Author()
  author_form = AuthorForm(request.form, obj=author)
  return add_or_resubmit(request, author, author_form, 'add_author.html', 'base.html')
