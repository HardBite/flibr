from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, db_session
from flask_wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms import StringField, validators


#from sqlalchemy.ext.associationproxy import association_proxy


authors_books = Table('authors_books', Base.metadata,
                Column('author_id', Integer, ForeignKey('author.id')),
                Column('book_id', Integer, ForeignKey('book.id'))
                       )

class Book(Base):
  __tablename__ = 'book'
  id = Column(Integer, primary_key=True)
  title = Column(String(255))
  author = relationship("Author", secondary = authors_books)

  def get_by_id_or_new(self, id):
    book = Book.query.get(id)
    return book if book else self

  def save(self):
    db_session.add(self)
    db_session.commit()
    return True


class Author(Base):
  __tablename__ = 'author'
  id = Column(Integer, primary_key=True)
  name = Column(String(127))
  book = relationship("Book", secondary = authors_books)

  def __str__(self):
    return self.name

BookForm = model_form(Book, db_session)
AuthorForm = model_form(Author, db_session)


#class BookForm(Form):
#  pass
