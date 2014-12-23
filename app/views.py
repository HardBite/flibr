from app import app
from flask import render_template, request, jsonify, redirect, url_for
from models import Book, BookForm, Author, AuthorForm




def add_or_resubmit(request, obj, form, submit_template_path, json_response=False):
  print 'redirect request to add_of_resubmit'
  books_list = Book().get_all()
  notification=None
  if request.method == 'POST':
#    print 'POST method detected'
#    print 'request.form', request.form
    form.populate_obj(obj)
    is_submitted = obj.save_or_error()
    if is_submitted==True:
      if not json_response:
        return redirect(url_for('books'))
      else:
        return {"notification": "Book saved"}
    else:
      notification = is_submitted
      print notification
      if not json_response:
        return render_template(submit_template_path, form=form,  notification=notification, books_list = books_list)
      else:
        return {"notification": notification, "data": request.form}
  else:
    print 'GET method detected'
    return render_template(submit_template_path, form=form, notification=notification, books_list = books_list)


@app.route('/')
@app.route('/books')
def books():
  books_list = Book().get_all()
  return render_template('base.html', books_list=books_list)


@app.route('/authors')
def autors()

@app.route('/sign_up')
def sign_up():
  pass

@app.route('/log_in')
def log_in():
  pass

@app.route('/add_book', methods = ['GET', 'POST'])
def add_book(book=None):
  print 'call to add_book recieved via html'
  book = book or Book()
  book_form = BookForm(request.form, obj=book)
  return add_or_resubmit(request, book, book_form, 'add_book.html')

@app.route('/json_add_book', methods = ['POST'])
def json_add_book(book=None):
  print 'call to add_book recieved via ajax'
  book = book or Book()
  data = add_or_resubmit(request, book, BookForm(request.form, obj=book), 'add_book.html', json_response=True)
  print 'JSON response', data
  return jsonify(**data)

@app.route('/delete_book/<int:book_id>', methods = ['GET', 'DELETE'])
def delete_book(book_id):
  print 'call to delete book recieved'
  book = Book().get_by_id_or_new(book_id)
  notification = 'Book '+str(book.title)+' deleted.'
  class_to_hide = ".book_"+str(book_id)
  if book.delete():
    ###Distinguish html from ajax request. Ajax sends 'DELETE'
    if request.method == 'DELETE':
      data = {}
      data['notification'] = notification
      data['class_to_hide'] = class_to_hide
      print 'delete_book return data', data
      return jsonify(**data)
    else:
      redirect(url_for('books'))



@app.route('/add_author', methods = ['GET', 'POST'])
def add_author():
  author = Author()
  author_form = AuthorForm(request.form, obj=author)
  return add_or_resubmit(request, author, author_form, 'add_author.html', 'base.html')
