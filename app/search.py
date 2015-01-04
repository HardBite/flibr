"""
Classes:
    SearchForm(Form): form of WTForms instantiated explicitly for the search.
    Forms for the data models are generated with WTF model_form().

Generic methods:
    make_unicode(string): accepts string and returns it converted to unicode
    if it was't the the instance of unicode, else returns string itself.
"""
from database import db_session
import itertools
from wtforms import Form, StringField, validators
"""
    Performs a recursive search through the DB entries for a model within given
    property_column by filtering db_query gradually with all combinations of
    whitespace terminated literals passed with query_text.

    Example:
    If one wants to search by keywords query_text="abc defg h" in books titles
    this method will be called from instanse of the Book model with
    corresponding Query object, contained in db_query, where search will be
    performed in the property_column=column title of the model table.
    Search will go on untill maximum length of result reached (20 entries)
    or all reductive permutations of the keywords are searched with.
    itertools.permutations will be called to select all possible subsets of:
    3 (length of query_text), 2, 1 keywords.
    For given example permutations will be:
        ('abc', 'defg', 'h')
        ('abc', 'h', 'defg')
        ('defg', 'abc', 'h')
        ('defg', 'h', 'abc')
        ('h', 'abc', 'defg')
        ('h', 'defg', 'abc')
        ('abc', 'defg')
        ('abc', 'h')
        ('defg', 'abc')
        ('defg', 'h')
        ('h', 'abc')
        ('h', 'defg')
        ('abc',)
        ('defg',)
        ('h',)
    From objects currently populating db_query, firstly those will be selected
    which contain substring "abc" by filter(property_column.like("%abc%")).
    Next step (depth += 1) filters remaining objects by substring
    "defg" and so on. If on some step of filtering 0 objects found, than result
    of previous step is added to result list. If none objects found even with
    first keyword (depth==0), empty list is explicitly submitted to result.

    Args:
        db_query: sqlalchemy Query object for given model.
        query_text (string): keyword(s) submitted
        property_column (Book().__table__.c.title): column object of model
            attribute to search within

    Returns:
        result (list): list of id's of objects matching search criteria.
        The most precise mathes goes last.
    """
MAX_SEARCH_RESULTS = 20
MAX_QUERY_WORDS = 4
MAX_QUERY_CHARS = 40


def make_unicode(s):
    """Accepts string, returns same string utf-8 encoded if it wasn't"""
    if isinstance(s, str):
        return s.decode('utf-8')
    elif isinstance(s, unicode):
        return s
    else:
        print "unknown encoding"
        return None


class Search(object):

    def __init__(self, obj, query_text):
        self.property_column = obj.searchable()
        self.id_column = obj.__table__.c.id
        self.db_query = db_session.query(self.id_column, self.property_column)
        self.query_list = make_unicode(query_text).split()
        self.result = []
        self.used_patterns = []
        self.search()
        self.objects = []

    def search(self):
        for n in range(len(self.query_list), 0, -1):
            if len(self.result) > MAX_SEARCH_RESULTS:
                break
            for pattern in itertools.permutations(self.query_list, n):
                if not pattern in self.used_patterns:
                    result = self.filter_out(pattern)
                    if result:
                        for item in result:
                            if not item in self.result:
                                self.result.append(item)

    def filter_out(self, pattern):
        current_step = self.db_query
        depth = 0
        for word in pattern:
            next_step = current_step.filter(
                self.property_column.like("%" + unicode(word) + "%"))
            if next_step.count() > 0:
                current_step = next_step
                depth += 1
            else:
                if depth == 0:
                    current_step = []
                    break
                else:
                    break
        self.used_patterns.append(pattern[:depth+1])
        return current_step


class SearchForm(Form):
    search = StringField('search', validators=[validators.DataRequired()])
