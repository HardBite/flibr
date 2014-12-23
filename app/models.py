import re

from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, db_session
#from flask_wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from sqlalchemy.ext.declarative import declared_attr
from wtforms import StringField, validators

title_forbidden_chars = re.compile("""[^a-zA-Z0-9\&?!\.,'\s-]""", re.U)
name_forbidden_chars = re.compile("""[^a-zA-Z0-9.,'\s-]""", re.U)




authors_books = Table('authors_books', Base.metadata,
                Column('author_id', Integer, ForeignKey('author.id')),
                Column('book_id', Integer, ForeignKey('book.id'))
                       )
class Record(object):
# Abstracts common properties from Book and Author that to be inherited with mix-in
  @declared_attr
  def __tablename__(cls):
    return cls.__name__.lower()

  id = Column(Integer, primary_key=True)

  def introduce(self):
    return type(self).__name__

  def pluralize(self):
    return (type(self).__name__.lower()+'s')

  def get_by_id_or_new(self, id):
    entry = self.query.get(id)
    return entry if entry else self

  def get_all(self):
    return self.query.all()[::-1]
    

  def string_valid(self, string, min_length, max_length, forbidden_re):
    print "Validation message: validation call recieved"
    if string:
      if min_length<=len(string)<=max_length:
        if not forbidden_re.search(string):
          print "Validation message: string seems valid"
          return True
        else:
         return 'You have entered inacceptible characters'
      else:
        return 'Field should contain at least '+str(min_length)+' and '+str(max_length)+' at most'
    else:
      return 'Field required'


  def save_or_error(self):
    print "Call to save_or_error. Id of given instance is", self.id
    validity = self.is_valid()
    if validity == True:
      if self.id:
        return true
      else:
        db_session.add(self)
        db_session.commit()
        #print 'database commit commented out'
        return True
    else:
      return validity

  def delete(self):
    db_session.delete(self)
    db_session.commit()
    print 'database commit commented out'
    return True


class Book(Base, Record):
  title = Column(String(255))
  author = relationship("Author", secondary = authors_books)

  def __str__(self):
    return self.title

  def is_valid(self):
    min_length = 1
    max_length = 255
    if not self.author:
      return 'You need to specify author(s) after entering book title'
    else:
      return self.string_valid(self.title, min_length, max_length, title_forbidden_chars)

  def json_descr(self):
    authors_list = []
    for author in self.author:
      authors_list.append(author.name)
    return {"prime_value": self.title, "related_values": authors_list, "id" : self.id}
    

    

class Author(Base, Record):
  name = Column(String(127))
  book = relationship("Book", secondary = authors_books)

  def __str__(self):
    return self.name

  def json_descr(self):
    books_list = []
    for book in self.book:
      books_list.append(book.title.name)
    return {"prime_value": self.title, "related_values": self.author, "id": self.id}

  def is_valid(self):
    min_length = 1
    max_length = 127
    return self.string_valid(self.name, min_length, max_length, name_forbidden_chars)

BookForm = model_form(Book, db_session)
AuthorForm = model_form(Author, db_session)
