from app import app
from flask import render_template, request
from models import Book, BookForm, Author, AuthorForm


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
def add_book():
  #book = Book.get_by_id_or_new(request.args['id'])
  book = Book()
  book_form = BookForm(request.book_form, obj=book)
  author = Author()
  author_form = AuthorForm(request.author_form, obj=author)
  if request.method == 'POST':
    print 'well done'
    book_form.populate_obj(book)
    author_form.populate_obj(author)
    book.save()
    author.save()
    return render_template('base.html')
  else:
    return render_template('add_book.html', form=form)

def add_author():


