#-*- coding: utf-8 -*-
from app import app
from flask import render_template, request, redirect, url_for, jsonify
from models import Record, Book, Author
from search import SearchForm


def instantiate_and_form(request, instance, obj_id=None):
    """
    Abstracts common operations from actions add/<instance>, edit/<instance>.
    Instantiates blank model object obj by it's string name (i. e.
    instance=book will produce obj=Book()). Instantiates corresponding
    WTForm model_form object form. If obj_id provided, tries to populate
    obj with database data.
    Populates form with request.from data (if any). Than tries to modify
    obj with data in form. Returns ready to use obj, form to caller.
    """
    obj = Record().give_child(instance)
    form = obj.give_form()
    obj = obj.get_by_id_or_new(obj_id)
    form = form(request.form, obj=obj)
    obj.populate_with(form)
    return obj, form


def try_to_submit(obj, form):
    """
    Abstracts common operations from actions add/<instance>, edit/<instance>.
    Calling save_or_error model object obj method recieves True if save
    succeded or error message otherwise.
    If obj saved, redirects HTML call to corresponding index page (i. e.
    if obj is instance of a model Book(), than redirect is to index/book).
    If call was XMLHttpRequest (sent via JavaScript jQuery), renders
    corresponding partial template (i.e. Book() object will produce
    partial/book.html template that is a table row filled with submitted data)
    Validation error on obj save produce re-rendering of submission form with
    corresponding error message.
    """
    save_message = obj.save_or_error()
    if save_message is True:
        if request.is_xhr:
            return render_template('partial/'+repr(obj)+'.html', obj=obj)
        else:
            return redirect('index/'+repr(obj))
    else:
        if request.is_xhr:
            return jsonify({'error': save_message})
        else:
            return render_template('add/'+repr(obj)+'.html', form=form,
                                   notification=save_message)


@app.route('/')
@app.route('/books')
def books():
    """
    Default route for application ('/') as well as shortcut to
    '/index/<instance>' action where instance=book.
    """
    books_list = Book().get_all()
    return render_template('index/book.html', entities_list=books_list)


@app.route('/authors')
def autors():
    """Shortcut to '/index/<instance>' action where instance=author."""
    authors_list = Author().get_all()
    return render_template('index/author.html', entities_list=authors_list)


@app.route('/index')
@app.route('/index/<instance>')
def index(instance='book'):
    entities_list = Record().give_child(instance).get_all()
    return render_template('index/'+instance+'.html',
                           entities_list=entities_list)


@app.route('/search', methods=["POST", "GET"])
def search():
    form = SearchForm(request.form)
    if request.method == 'POST':
        return redirect(url_for('search_results', query=form.search.data))
    else:
        return render_template('search.html', search_form=form)


@app.route('/search_results/<query>', methods=['GET'])
def search_results(query):
    found_instances = Book().search_by_kwords(query)
    found_titles = found_instances['in_titles']
    by_authors = found_instances['in_names']
    return render_template('search_results.html', query=query,
                           found_titles=found_titles, by_authors=by_authors)


@app.route('/add/<instance>', methods=['GET', 'POST'])
def add(instance):
    obj, form = instantiate_and_form(request, instance)
    if request.method == 'POST':
        return try_to_submit(obj, form)
    else:
        if request.is_xhr:
            return render_template('form/'+instance+".html", form=form)
        else:
            return render_template('add/'+instance+'.html',
                                   form=form, notification=None)


@app.route('/edit/<instance>/<obj_id>', methods=['GET', 'POST'])
def edit(instance, obj_id):
    obj, form = instantiate_and_form(request, instance, obj_id)
    if request.method == 'POST':
        return try_to_submit(obj, form)
    else:
        if request.is_xhr:
            return render_template('form/'+instance+'.html', form=form)
        else:
            return render_template('add/' + instance + '.html', form=form)


@app.route('/delete/<instance>/<obj_id>', methods=['GET', 'DELETE'])
def delete(instance, obj_id):
    obj = Record().give_child(instance)
    obj = obj.get_by_id_or_new(obj_id)
    obj.delete()
    if not request.is_xhr:
        return redirect('index/'+repr(obj))
    else:
        return "it ok"
