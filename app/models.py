#-*- coding: utf-8 -*-
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
        - basic validation of the model data;
        - CRUD operations for database.

    Book and Author classes co-inherit sqlalchemy declarative_base() class as
    Base, which does all of the database heavy-lifting, providing
    clean interface to store modelled data.

    Book(Base, Record): specific properties for the data model of book. Has a
    Title string column and maps many-to-many ralation with Author model via
    intermediate table authors_books.

    Author(Base, Record): specific properties of author: name and relation to
    Book via authors_books.

Generic variables:
    title_allowed_chars: compiled python regex of allowed unicode characters
    for the book title.

    name_allowed_chars: regex for allowed unicode chars within author name.

    authors_books: sqlalchemy Table object that facilitates many-to-many
    relationship storing values of correspondent book's and author's id as
    foreign keys.
"""
import re
from sqlalchemy import Column, Integer, Unicode, Table, ForeignKey  # , String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from database import Base, db_session
from wtforms.ext.sqlalchemy.orm import model_form
from search import Search


title_allowed_chars = re.compile(u"""[^a-zA-Zа-яА-Я0-9\&?!\.,'\s-]""", re.U)
name_allowed_chars = re.compile(u"""[^a-zA-Zа-яА-Я0-9.,'\s-]""", re.U)


authors_books = Table('authors_books', Base.metadata,
                      Column('author_id', Integer, ForeignKey('author.id')),
                      Column('book_id', Integer, ForeignKey('book.id')))


class Record(object):
    """
    Class encapsulates all common properties and functionality of models to be
    inherited by model classes as mix-in.
    """
    @declared_attr
    def __tablename__(cls):
        """Returns table name consistent with model class name"""
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return type(self).__name__.lower()


    def give_child(self, inst_name):
        """
        Accepts string with the name of instance to be created.
        Returns instance correspondant class name. If invalid string passed -
        returns None.
        """
        if inst_name == 'book':
            return Book()
        elif inst_name == 'author':
            return Author()
        else:
            return None

    def give_form(self):
        """
        Being called form child model class instance
        returns WTForms model_form object of corresponding model class.
        """
        form = model_form((eval(type(self).__name__)), db_session)
        print 'in give_form', type(self).__name__
        print form.data
        return form

    def populate_with(self, form):
        """
        Accepts object of corresponding model_form as argument
        and populates calling object with form data.
        """
        form.populate_obj(self)

    def pluralize(self):
        """Returns lowercased name of the class of calling object"""
        return str((type(self).__name__.lower() + 's'))

    def get_by_id_or_new(self, id=None):
        """
        Returns object populated with data found in database by the id.
        If none found or no id provided as argument, returns calling object
        """
        entry = self.query.get(id)
        return entry if entry else self

    def get_all(self):
        """
        Retrieves all records of model from database
        and returns them as a list of instances
        """
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
        """
        Being called from model class instance checks if object is populated
        with valid data. Validation respond (True or error message)
        contained in validity variable and is returned to caller.
        """
        print "Call to save_or_error. Id of given instance is", self.id
        validity = self.is_valid()
        if validity is True:
            #if self.id:
            #    db_session.add(self)
            #    db_session.commit()
            #    print 'entity', self, self.id, 'updated'
            #    return validity
            #else:
            db_session.add(self)
            db_session.commit()
            # print 'database commit commented out'
            return validity
        else:
            return validity

    def delete(self):
        """Delete database entry corresponding to calling model class object"""
        db_session.delete(self)
        db_session.commit()
        # print 'database commit commented out'
        return True


class Book(Base, Record):
    """
    Class of model Book. Contains unique properties (table column name:title
    and relationship through table authors_books); method that returnes column
    to be searched upon, specific validator, string and dictionary
    JSON representation of calling instance.
    """
    title = Column(Unicode(255))
    author = relationship("Author", secondary=authors_books)

    def __str__(self):
        """Returns sting representation of book model instance."""
        return self.title

    def searchable(self):
        """Returns column object upon which search will be performed"""
        return self.__table__.c.title

    def is_valid(self):
        """
        Checks if related authors assigned to book object.
        If so, calls inherited from the class Record() method to verify
        validity of given title
        """
        min_length = 1
        max_length = 255
        if not self.author:
            return 'You need to specify author(s) after entering book title'
        else:
            return self.string_valid(self.title, min_length, max_length, title_allowed_chars)

    def json_descr(self):
        """Returns dictionary of object data"""
        authors_list = []
        for author in self.author:
            authors_list.append(author.name)
        return {"prime_value": self.title, "related_values": authors_list, "id": self.id}


class Author(Base, Record):
    """
    Class of model Author. Contains unique properties (table column name:name
    and relationship through table authors_books); method that returnes column
    to be searched upon, specific validator, string and dictionary
    JSON representation of calling instance.
    """
    name = Column(Unicode(127))
    book = relationship("Book", secondary=authors_books)

    def __str__(self):
        """Returns sting representation of author model instance."""
        return self.name

    def searchable(self):
        """Returns column object upon which search will be performed"""
        return self.__table__.c.name

    def is_valid(self):
        """
        Calls inherited from the class Record() method to verify
        validity of given name.
        """
        min_length = 1
        max_length = 127
        return self.string_valid(self.name, min_length, max_length, name_allowed_chars)

    def json_descr(self):
        """Returns dictionary of object data"""
        books_list = []
        for book in self.book:
            books_list.append(book.title)
        return {"prime_value": self.name, "related_values": books_list, "id": self.id}
