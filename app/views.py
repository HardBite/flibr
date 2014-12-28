#-*- coding: utf-8 -*-
from app import app
from flask import render_template, request, jsonify, redirect, url_for
from models import Record, Book, Author, SearchForm#, AuthorForm , BookForm
from database import db_session


@app.route('/')
@app.route('/books')
def books():
  books_list = Book().get_all()
  return render_template('base.html', entities_list=books_list)

@app.route('/authors')
def autors():
  authors_list = Author().get_all()
  return render_template('base.html', entities_list=authors_list)

@app.route('/search', methods=["POST", "GET"])
def search():
  form = SearchForm(request.form)
  if request.method == 'POST':
    return redirect(url_for('search_results', query = form.search.data))
  else:
    return render_template('search.html', search_form = form)

@app.route('/search_results/<query>', methods = ['GET'])
def search_results(query):
  found_instances = Book().search_by_kwords(query)
  found_titles = found_instances['in_titles']
  by_authors = found_instances['in_names']
  return render_template('search_results.html', query = query, found_titles = found_titles, by_authors = by_authors)


@app.route('/add/<instance>', methods = ['GET', 'POST'])
def add(instance):
  print 'call to add/inst with', instance, 'request', request.method
  if request.is_xhr:
    print '\t via xhr', 'with request.form', request.form

  obj = Record().give_child(instance)
  print '\tobj', type(obj).__name__, 'instantiated'
  form = obj.give_form()
  print '\tform given with data', form.data
  form = form(request.form, obj=obj)
  print '\tform populated', form.data
  obj.populate_with(form)
  if request.method == 'POST':
    print '\t POST branch'
    save_message = obj.save_or_error()
    print '\t save_message', save_message
    print '\t\t', obj.json_descr()
    if save_message == True:
      if request.is_xhr:
        return render_template(instance+'_row.html', entities_list = [obj])
      else:
        try:
          return redirect(url_for(obj.pluralize()))
        except:
          return redirect('/authors')
    else:
      return render_template('add_' + instance + '.html', form = form, notification = save_message)
  else:
    if request.is_xhr:
      return render_template(instance+"_form.html", form=form)
    else:
      return render_template('add_' + instance + '.html', form = form, notification = None, action = obj.introduce().lower())

@app.route('/edit/<instance>/<obj_id>', methods = ['GET', 'POST'])
def edit(instance, obj_id):
  obj = Record().give_child(instance)
  obj = obj.get_by_id_or_new(obj_id)
  form = obj.give_form()
  form = form(request.form, obj=obj)
  print form.data
  if request.method == 'POST':
    obj.populate_with(form)
    save_message = obj.save_or_error()
    if save_message == True:
      print obj.pluralize()
      if not request.is_xhr:
        try:
          return redirect(url_for(obj.pluralize()))
        except:
          return redirect('/authors')
      else:
        return render_template(instance+'_row.html', entities_list = [obj])
    else:
      return render_template('add_' + instance + '.html', form = form, notification = save_message)
  else:
    html = render_template('add_'  + instance + '.html', form=form)
    if not request.is_xhr:
      return html
    else:
      html = render_template(instance + '_form.html', form = form)
      print 'html marked to respond:', html
      return html

@app.route('/delete/<instance>/<obj_id>', methods = ['GET', 'DELETE'])
def delete(instance, obj_id):
  obj = Record().give_child(instance)
  obj = obj.get_by_id_or_new(obj_id)
  obj.delete()
  try:
    return redirect(url_for(obj.pluralize()))
  except:
    return redirect('/authors')



#def external_url_handler(error, endpoint, **values):
#  return '/authors'

#app.build_error_handler = external_url_handler
""" 
@app.route('/delete_author/<author_id>', methods = ['DELETE'])
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
"""