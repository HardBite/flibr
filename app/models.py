#-*- coding: utf-8 -*-
import re
from sqlalchemy import Column, Integer, Unicode, Table, ForeignKey  # , String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from database import Base, db_session
from wtforms.ext.sqlalchemy.orm import model_form

from search import Search

#import ipdb

"""
Introduces scalable ORM layer with models via sqlalchemy.orm along with
some generic methods and variables.
Models encapsulate all "buisness" logic and provides database data
manipulations consistent to internal relations of the models. Basically You
should only import model classes themselfs elsewhere.

Classes:
    Record(object): abstracts all common properties and functionality
    of the models to be inherited by them as a mix-in:
        Properties:
        - corresponding database table named "<modelname>"
        after the "Modelname";
        - id field
        Functionality:
        - instantiating of the correspondent model object on it's
        name passed as a string;
        - instantiating and populating WTForms model_form() object;
        - basic validation of the field;
        - CRUD operations for database.

    Book and Author classes co-inherit sqlalchemy declarative_base() class as
    Base, which does all of the database heavy-lifting, providing
    clean interface to store modelled data.

    Book(Base, Record): specific properties for the data model of book. Has a
    Title string column and maps many-to-many ralation with Author model via
    intermediate table authors_books.

    Author(Base, Record): specific properties of author: name and relation to
    Book via authors_books.

    SearchForm(Form): form of WTForms instantiated explicitly for the search.
    Forms for the data models are generated with WTF model_form().

Generic variables:
    title_allowed_chars: compiled python regex of allowed unicode characters
    for the book title.

    name_allowed_chars: regex for allowed unicode chars within author name.

    authors_books: sqlalchemy Table object that facilitates many-to-many
    relationship storing values of correspondent book's and author's id as
    foreign keys.
"""

title_allowed_chars = re.compile(u"""[^a-zA-Zа-яА-Я0-9\&?!\.,'\s-]""", re.U)
name_allowed_chars = re.compile(u"""[^a-zA-Zа-яА-Я0-9.,'\s-]""", re.U)


authors_books = Table('authors_books', Base.metadata,
                      Column('author_id', Integer, ForeignKey('author.id')),
                      Column('book_id', Integer, ForeignKey('book.id')))


class Record(object):
# Abstracts common properties from Book and Author that to be inherited
# with mix-in

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)

    def give_child(self, inst_name):
        if inst_name == 'book':
            return Book()
        elif inst_name == 'author':
            return Author()

    def give_form(self):
        form = model_form((eval(type(self).__name__)), db_session)
        print 'in give_form', type(self).__name__
        print form.data
        return form

    def populate_with(self, form):
        form.populate_obj(self)

    def pluralize(self):
        return str((type(self).__name__.lower() + 's'))

    def get_by_id_or_new(self, id):
        #print 'call to get_by_id_or_new recieved with', type(self).__name__, id
        entry = self.query.get(id)
        if entry:
            pass
            #print 'entry found:', entry.id
        return entry if entry else self

    def get_all(self):
        return self.query.all()[-5:]

    def search_by_kwords(self, query_text):
        found_id = {}
        found_id['in_titles'] = Search(Book(), query_text).result
        found_id['in_names'] = Search(Author(), query_text).result

        found_inst = {'in_titles': [], 'in_names': []}
        for ident in found_id['in_titles']:
            found_inst['in_titles'].append(Book().get_by_id_or_new(ident.id))
        for ident in found_id['in_names']:
            for book in Author().get_by_id_or_new(ident.id).book:
                found_inst['in_names'].append(book)
        return found_inst

    def string_valid(self, string, min_length, max_length, forbidden_re):
        print "Validation message: validation call recieved"
        if string:
            if min_length <= len(string) <= max_length:
                if not forbidden_re.search(string):  # (transliterate(string)):
                    print "Validation message: string seems valid"
                    return True
                else:
                    return 'You have entered inacceptable characters'
            else:
                return 'Field should contain at least ' + str(min_length) + \
                       ' and ' + str(max_length) + ' at most'
        else:
            return 'Field required'

    def save_or_error(self):
        print "Call to save_or_error. Id of given instance is", self.id
        validity = self.is_valid()
        if validity is True:
            if self.id:
                db_session.add(self)
                db_session.commit()
                print 'entity', self, self.id, 'updated'
                return validity
            else:
                db_session.add(self)
                db_session.commit()
                # print 'database commit commented out'
                return validity
        else:
            return validity

    def delete(self):
        db_session.delete(self)
        db_session.commit()
        # print 'database commit commented out'
        return True


class Book(Base, Record):
    title = Column(Unicode(255))
    author = relationship("Author", secondary=authors_books)

    def __str__(self):
        return self.title

    def searchable(self):
        """Returns column object upon which search will be performed"""
        return self.__table__.c.title

    def is_valid(self):
        min_length = 1
        max_length = 255
        if not self.author:
            return 'You need to specify author(s) after entering book title'
        else:
            return self.string_valid(self.title, min_length, max_length, title_allowed_chars)

    def json_descr(self):
        authors_list = []
        for author in self.author:
            authors_list.append(author.name)
        return {"prime_value": self.title, "related_values": authors_list, "id": self.id}


class Author(Base, Record):
    name = Column(Unicode(127))
    book = relationship("Book", secondary=authors_books)

    def __str__(self):
        return self.name

    def searchable(self):
        """Returns column object upon which search will be performed"""
        return self.__table__.c.name

    def json_descr(self):
        books_list = []
        for book in self.book:
            books_list.append(book.title)
        return {"prime_value": self.name, "related_values": books_list, "id": self.id}

    def is_valid(self):
        min_length = 1
        max_length = 127
        return self.string_valid(self.name, min_length, max_length, name_allowed_chars)
