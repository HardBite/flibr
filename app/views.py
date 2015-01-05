#-*- coding: utf-8 -*-
from app import app
from flask import render_template, request, redirect, url_for
from models import Record, Book, Author
from search import SearchForm


@app.route('/')
@app.route('/books')
def books():
    books_list = Book().get_all()
    return render_template('index/book.html', entities_list=books_list)


@app.route('/authors')
def autors():
    authors_list = Author().get_all()
    return render_template('index/author.html', entities_list=authors_list)


@app.route('/index/<instance>')
def index(instance):
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
    obj = Record().give_child(instance)
    form = obj.give_form()
    form = form(request.form, obj=obj)
    obj.populate_with(form)
    if request.method == 'POST':
        save_message = obj.save_or_error()
        if save_message is True:
            if request.is_xhr:
                return render_template(instance+'_row.html', entities_list=[obj])
            else:
                return redirect('index/'+repr(obj))
        else:
            return render_template('add/' + instance + '.html', form=form, notification=save_message)
    else:
    #Thats if request.method is GET
        if request.is_xhr:
            html = render_template(instance+"_form.html", form=form)
            print 'html marked to respond:', html
            return html
        else:
            return render_template('add/' + instance + '.html', form=form, notification=None)


@app.route('/edit/<instance>/<obj_id>', methods=['GET', 'POST'])
def edit(instance, obj_id):
    obj = Record().give_child(instance)
    form = obj.give_form()
    obj = obj.get_by_id_or_new(obj_id)
    form = form(request.form, obj=obj)
    if request.method == 'POST':
        obj.populate_with(form)
        save_message = obj.save_or_error()
        if save_message is True:
            print obj.pluralize()
            if not request.is_xhr:
                return redirect('index/'+instance)
            else:
                return render_template(instance+'_row.html', entities_list=[obj])
        else:
            return render_template('add/' + instance + '.html', form=form, notification=save_message)
    else:
    #Thats if request.method is GET
        if not request.is_xhr:
            return render_template('add/'    + instance + '.html', form=form)
        else:
            return render_template(instance + '_form.html', form=form)


@app.route('/delete/<instance>/<obj_id>', methods=['GET', 'DELETE'])
def delete(instance, obj_id):
    obj = Record().give_child(instance)
    obj = obj.get_by_id_or_new(obj_id)
    obj.delete()
    if not request.is_xhr:
        return redirect('index/'+repr(obj))
    else:
        return "it ok"
