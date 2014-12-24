from app import app
from flask import render_template, request, jsonify, redirect, url_for
from models import Record, Book, BookForm, Author, AuthorForm
#import ipdb

@app.route('/')
@app.route('/books')
def books():
  books_list = Book().get_all()
  return render_template('base.html', entities_list=books_list)

@app.route('/authors')
def autors():
  authors_list = Author().get_all()
  return render_template('base.html', entities_list=authors_list)

@app.route('/sign_up')
def sign_up():
  pass

@app.route('/log_in')
def log_in():
  pass
"""
@app.route('/add_book', methods = ['GET', 'POST'])
def add_book(book=None):
  book = book or Book()
  book_form = BookForm(request.form, obj=book)
  return add_or_resubmit(request, book, book_form, 'add_book.html')

@app.route('/add_author', methods = ['GET', 'POST'])
def add_author():
  author = Author()
  author_form = AuthorForm(request.form, obj=author)
  return add_or_resubmit(request, author, author_form, 'add_author.html')"""

@app.route('/add/<instance>', methods = ['GET', 'POST'])
def add(instance):
  obj = Record().give_child(instance)
  form = obj.give_form()
  #ipdb.set_trace()
  form = form(request.form, obj=obj)
  print form
  print form.data
  form.populate_obj(obj)
  if request.method == 'POST':
    save_message = obj.save_or_error()
    if save_message == True:
      return redirect(url_for(obj.pluralize()))
    else:
      return render_template('add_' + instance + '.html', form = form, notification = save_message)
  else:
    return render_template('add_' + instance + '.html', form = form, notification = None, action = obj.introduce().lower())





@app.route('/edit/<int:book_id>', methods = ['GET', 'POST'])
def edit(book_id):
  book = Book().get_by_id_or_new(book_id)
  print 'Edit book call. Book found: book'
  if request.method == 'POST':
    book_form = BookForm(request.form, obj=book)
    book_form.populate_obj(book)
    print book.save_or_error()
    return redirect(url_for('books'))
  else:
    book_form = BookForm(obj=book)
    action = str(book.id)
    html = render_template('add_book.html', form=book_form, action = action)
    if not request.is_xhr:
      return html
    else:
      html = '<tr><td> <div hidden class="hiddenDisv">'+str(book.id)+'</div>'+html+'</td></tr>'
      class_to_sub = ".row_"+str(book_id)
      json_response = {'html': html, 'ClassToSub': class_to_sub}
      #print json_response  
      return jsonify(**json_response)




@app.route('/delete_book/<int:book_id>', methods = ['GET', 'DELETE'])
def delete_book(book_id):
  book = Book().get_by_id_or_new(book_id)
  return destroy_record(request, book)
 
@app.route('/delete_author/<int:author_id>', methods = ['DELETE'])
def delete_author(author_id):
  print 'call to delete author recieved'
  author = Author().get_by_id_or_new(author_id)
  return destroy_record(request, author)


def add_or_resubmit(request, obj, form, submit_template_path):
  print 'redirect request to add_of_resubmit'
  entities_list = obj.get_all()
  notification=None
  if request.method == 'POST':
#    print 'POST method detected'
    object_id = obj.id
    print "Call in add_of_resub. Id of given instance is", object_id
    if not obj.id:
      form.populate_obj(obj)
    else:
      form.populate_obj(obj)
      obj.id = object_id

    is_submitted = obj.save_or_error()
    if is_submitted==True:
      if not request.is_xhr:
        return redirect(url_for(obj.pluralize()))
      else:
        #json_response = obj.json_descr()
        from_template = render_template(str(obj.introduce().lower()+'_row.html'), entities_list = [obj])
        json_response.update({"notification": obj.introduce()+" saved", "html": from_template})
        return jsonify(**json_response)
    else:
      notification = is_submitted
      print notification
      if not request.is_xhr:
        return render_template(submit_template_path, form=form,  notification=notification, entities_list = entities_list)
      else:
        return jsonify(**{"notification": notification, "data": request.form})
  else:
    print 'GET method detected'
    return render_template(submit_template_path, form=form, notification=notification, entities_list = entities_list)

def destroy_record(request, obj):
  notification = obj.introduce()+' deleted.'
  class_to_hide = ".row_"+str(obj.id)
  if obj.delete():
    if request.is_xhr:
      data = {}
      data['notification'] = notification
      data['class_to_hide'] = class_to_hide
      print 'delete_', obj.introduce(), 'return data', data
      return jsonify(**data)
    else:
      return redirect(url_for(obj.pluralize()))
