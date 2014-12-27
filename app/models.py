#-*- coding: utf-8 -*-
import re
from sqlalchemy import Column, Integer, Unicode, Table, ForeignKey #, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import label
from sqlalchemy.ext.declarative import declared_attr
from database import Base, db_session
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms import Form, StringField, validators
import itertools
#import ipdb


title_forbidden_chars = re.compile(u"""[^a-zA-Zа-яА-я0-9\&?!\.,'\s-]""", re.U)
name_forbidden_chars = re.compile(u"""[^a-zA-Z0-9.,'\s-]""", re.U)



authors_books = Table('authors_books', Base.metadata,
                Column('author_id', Integer, ForeignKey('author.id')),
                Column('book_id', Integer, ForeignKey('book.id')))

class Record(object):
# Abstracts common properties from Book and Author that to be inherited with mix-in
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
    return form

  def populate_with(self, form):
    form.populate_obj(self)


  def introduce(self):
    return type(self).__name__

  def pluralize(self):
    return str((type(self).__name__.lower()+'s'))

  def get_by_id_or_new(self, id):
    print 'call to get_by_id_or_new recieved with', type(self).__name__, id
    entry = self.query.get(id)
    if entry:
      print 'entry found:', entry.id
    return entry if entry else self

  def get_all(self):
    return self.query.all()[::-1]

  def search_by_kwords(self, query_text, query_session=None):
    found_id = {'in_titles':[], 'in_names':[]}

    #class_alias = aliased(Book)
    property_column = Book().__table__.c.title
    book_query_session = db_session.query(Book.id, property_column)
    found_id['in_titles'] = process_query(book_query_session, query_text, property_column)

    #id_alias = aliased(Author.id)
    property_column = Author().__table__.c.name
    author_query_session = db_session.query(Author.id, property_column)
    found_id['in_names'] = process_query(author_query_session, query_text, property_column)

    found_inst = {'in_titles' : [], 'in_names':[]}
    for ident in found_id['in_titles']:
      found_inst['in_titles'].append(Book().get_by_id_or_new(ident))
    for ident in found_id['in_names']:
      for book in Author().get_by_id_or_new(ident).book:
        found_inst['in_names'].append(book)
    return found_inst

  def string_valid(self, string, min_length, max_length, forbidden_re):
    print "Validation message: validation call recieved"
    if string:
      if min_length<=len(string)<=max_length:
        if not forbidden_re.search(string):          #(transliterate(string)):
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
        db_session.add(self)
        db_session.commit()
        print 'entity', self, self.id, 'updated'
        return validity
      else:
        db_session.add(self)
        db_session.commit()
        #print 'database commit commented out'
        return validity
    else:
      return validity

  def delete(self):
    db_session.delete(self)
    db_session.commit()
    #print 'database commit commented out'
    return True

class Book(Base, Record):
  title = Column(Unicode(255))
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
  name = Column(Unicode(127))
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

class SearchForm(Form):
  search = StringField('search', validators=[validators.DataRequired()])

def process_query(query_session, query_text, property_column):
    current = query_session
    #query_text = transliterate(query_text)
    query_text = make_unicode(query_text)
    query_list = query_text.split()
    result = []
    print query_list

    for n in range(len(query_list), 0, -1):
      print n
      for subset in itertools.permutations(query_list, n):
        print subset
        
        current = query_session
        depth = 0
        for word in subset:
          next = current.filter(property_column.like("%"+unicode(word)+"%"))
          if next.count()>0:
            current = next
            depth += 1
          else:
            if depth == 0:
              current = []
              break
            else:
              break
        
        for item in current:
          if not item.id in result:
            result.append(item.id)
      if len(result)>20:
        return result
    else:
      return result

def make_unicode(s):
  if isinstance(s, str):
    return s.decode('utf-8')
  elif isinstance(s, unicode):
    return s
  else:
    print "unknown encoding"
    return None
"""
def transliterate(unicode_string):
  string = unicode_string.lower()
  #sting = string.decode('cp1251')
  charmap = {u"а": "a",u"б": "b",u"в":"v",u"г":"g",u"д":"d",u"е":"e",u"ё":"e",
  u"ж": "g",u"з": "z",u"и":"i",u"й":"j",u"к":"k",u"л":"l",u"м":"m",u"н":"n",
  u"о":"o",u"п":"p",u"р":"r",u"с":"s",u"т":"t",u"у":"u",u"ф":"f",u"х":"h",
  u"ц":"z",u"ч":"h",u"ш":"h",u"щ":"h",u"ъ": "",u"ы": "i",u"ь": "",u"э":"e",
  u"ю":"u",u"я":"a"}
  new_string = ""
  for n in range(len(string)):
    if string[n] in charmap:
      new_string+=charmap[string[n]]
  print new_string
  return new_string"""
