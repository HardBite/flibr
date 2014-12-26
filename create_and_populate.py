import app.database
import app.models
import random as rnd

eng = app.database.engine
db_ses = app.database.db_session
app.database.init_db()

### generating some data for amusement and testing
v1 = ["Let's ", "How to ", "Stop "]
v2 = ["rock ", "draw ", "tell jokes ", "write a code "]
v3 = ["hard", "good", "bad", "ugly", "well"]

authors = ["Rockwell", "Drawgood", "Stopson", "Hardwell", "Letbe"]
aut_inst = []

for author in authors:
  a = app.models.Author()
  a.name = author
  a.save_or_error()
  aut_inst.append(a)
  print a.name

for n in range(25):
  b = app.models.Book()
  b.title = rnd.choice(v1)
  for v in (v2, v3):
    b.title += rnd.choice(v)
  b.author = rnd.sample(aut_inst, rnd.randint(1, 5))
  b.save_or_error()
  print b.title, b.author




