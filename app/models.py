import re

from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, db_session
#from flask_wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from sqlalchemy.ext.declarative import declared_attr
from wtforms import StringField, validators

title_forbidden_chars = re.compile("""[^a-zA-Z0-9\&?!\.,'-]""", re.U)
name_forbidden_chars = re.compile("""[^a-zA-Z0-9.,'-]""", re.U)




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

  def get_by_id_or_new(self, id):
    entry = self.query.get(id)
    return entry if entry else self

  def get_all(self):
    return self.query.all()
    

  def string_valid(self, string, min_length, max_length, forbidden_re):
    if string:
      if min_length<=len(string)<=max_length:
        if not forbidden_re.match(string):
          return True
        else:
         return 'You have entered inacceptible cheracters'
      else:
        return 'Field should contain at least '+str(min_length)+' and '+str(max_length)+' at most'
    else:
      return 'Field required'


  def save_or_error(self):
    validity = self.is_valid()
    if validity == True:
      db_session.add(self)
      db_session.commit()
      return True
    else:
      return validity

  def delete(self):
    db_session.delete(self)
    #db_session.commit()
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
    

    

class Author(Base, Record):
  name = Column(String(127))
  book = relationship("Book", secondary = authors_books)

  def __str__(self):
    return self.name

  def is_valid(self):
    min_length = 1
    max_length = 127
    return self.string_valid(self.name, min_length, max_length, name_forbidden_chars)

BookForm = model_form(Book, db_session)
AuthorForm = model_form(Author, db_session)
