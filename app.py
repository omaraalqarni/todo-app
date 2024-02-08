from flask import (
  Flask, 
  request, 
  jsonify
  )

import hashlib

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment

from config import secret_key

from flask_jwt_extended import (
  create_access_token,
  get_jwt_identity,
  jwt_required,
  JWTManager,
  )


# Create a Flask application object and configure it
app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

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
    
    def __repr__(self):
      return f'<Todo Item {self.id} {self.title}>'
        
class todoList(db.Model):
    __tablename__ = 'todoList'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    items = db.relationship('todoItem', backref='list', lazy='dynamic')
    
    def __repr__(self):
      return f'<Todo List {self.id} {self.title}>'

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True)
  email = db.Column(db.String(120), unique=True)
  password = db.Column(db.String(120))
  lists = db.relationship('todoList', backref='user', lazy='dynamic')
  
  def __repr__(self):
    return f'<User {self.id} {self.username}>'
  
  

############
## Routes ##
############

@app.route('/')
def hello_world():
    return 'Hello World!'



# signup route
@app.route('/signup', methods=['POST'])
def signUp():
  username = request.json.get("username", None)
  email = request.json.get("email", None)
  password = request.json.get("password", None)
  hashedPassword = hashlib.sha256(password.encode()).hexdigest()
  user = User(username=username, email=email, password=password)
  
  #check if username or email already exists
  if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
    return jsonify(message="Username already exists")
    
  db.session.add(user)
  db.session.commit()
  return jsonify(username=username, email=email)

# sign in route
@app.route('/login', methods=['POST'])
def login():
  username = request.json.get("username", None)
  password = request.json.get("password", None)
  hashedPassword = hashlib.sha256(password.encode()).hexdigest()
  if not username:
    return jsonify(message="Missing username parameter"), 400
  if not password:
    return jsonify(message="Missing password parameter"), 400
  
  user = User.query.filter_by(username=username).first()
  if user.password != hashedPassword:
    return jsonify(message="Bad username or password"), 401
  
  access_token = create_access_token(identity=username)
  return jsonify(access_token=access_token), 200


# create a new todo list
@app.route('/lists', methods=['POST'])
@jwt_required()
def createList():
  title = request.json.get("title", None)
  user = User.query.filter_by(username=get_jwt_identity()).first()
  newList = todoList(title=title, user=user)
  db.session.add(newList)
  db.session.commit()
  return jsonify(id=newList.id, title=newList.title)



if __name__ == '__main__':
    app.run()
