from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment


# Create a Flask application object and configure it
app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

migration = Migrate(app, db)

############
## Models ##
############

class todoItem(db.Model):
    __tablename__ = 'todoItem'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    done = db.Column(db.Boolean)
    list_id = db.Column(db.Integer, db.ForeignKey('todoList.id'))
    
    # def __init__(self, title, done, list_id):
    #     self.title = title
    #     self.done = done
    #     self.list_id = list_id
        
class todoList(db.Model):
    __tablename__ = 'todoList'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    items = db.relationship('todoItem', backref='list', lazy='dynamic')
    
    # def __init__(self, title):

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True)
  email = db.Column(db.String(120), unique=True)
  # password = db.Column(db.String(120))
  
  
  


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
