from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

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

class Author(Base):
  __tablename__ = 'author'
  id = Column(Integer, primary_key=True)
  name = Column(String(127))
  book = relationship("Book", secondary = authors_books)


