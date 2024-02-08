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
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
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


########## user routes ##########
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

# get user profile
@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
  user = get_jwt_identity()
  return jsonify(username=user), 200

# update user profile
@app.route('/profile', methods=['PUT'])
@jwt_required()
def updateProfile():
  username = request.json.get("username", None)
  email = request.json.get("email", None)
  user = get_jwt_identity()
  user = User.query.filter_by(username=user).first()
  user.username = username
  user.email = email
  db.session.commit()
  return jsonify(username=username, email=email), 200



########## todo list routes ##########

# create todo list
@app.route('/lists', methods=['POST'])
@jwt_required()
def createList():
  title = request.json.get("title", None)
  user = get_jwt_identity()
  list = todoList(title=title, owner_id=User.query.filter_by(username=user).first().id)
  db.session.add(list)
  db.session.commit()
  return jsonify(title=title),200

# get all todo lists
@app.route('/lists', methods=['GET'])
@jwt_required()
def getAllLists():
  user = get_jwt_identity()
  lists = todoList.query.filter_by(owner_id=User.query.filter_by(username=user).first().id).all()
  return jsonify([list.title for list in lists]), 200

# get a single todo list
@app.route('/lists/<int:id>', methods=['GET'])
@jwt_required()
def getAList(id):
  list = todoList.query.filter_by(id=id).first()
  return jsonify(title=list.title, items=[item.title for item in list.items.all()]), 200

# update a todo list title
@app.route('/lists/<int:id>', methods=['PUT'])
@jwt_required()
def updateListTitle(id):
  title = request.json.get("title", None)
  list = todoList.query.filter_by(id=id).first()
  list.title = title
  db.session.commit()
  return jsonify(title=title), 200

# add todo item to a list
@app.route('/lists/<int:id>/items', methods=['POST'])
@jwt_required()
def addItem(id):
  title = request.json.get("title", None)
  done = request.json.get("done", False)
  item = todoItem(title=title, done=done, list_id=id)
  db.session.add(item)
  db.session.commit()
  return jsonify(title=title, done=done), 200

# remove todo item from a list
@app.route('/lists/<int:list_id>/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def removeItem(list_id, item_id):
  list = todoList.query.filter_by(id=list_id).first()
  if not list:
    return jsonify(message="List not found"), 404
  if not list.items.filter_by(id=item_id).first():
    return jsonify(message="Item not found"), 404
  item = todoItem.query.filter_by(id=item_id).first()
  db.session.delete(item)
  db.session.commit()
  return jsonify(message="Item deleted"), 200

# update todo item in a list
@app.route('/lists/<int:list_id>/items/<int:item_id>', methods=['PUT'])
@jwt_required()
def updateItem(list_id, item_id):
  title = request.json.get("title", None)
  done = request.json.get("done", None)
  item = todoItem.query.filter_by(id=item_id).first()
  item.title = title
  item.done = done
  db.session.commit()
  return jsonify(title=title, done=done), 200

# delete a todo list
@app.route('/lists/<int:id>', methods=['DELETE'])
@jwt_required()
def deleteList(id):
  list = todoList.query.filter_by(id=id).first()
  db.session.delete(list)
  db.session.commit()
  return jsonify(message="List deleted"), 200

########## admin routes ##########
@app.route('/admin')
@jwt_required()
def admin():
  user = get_jwt_identity()
  if user != "admin":
    return jsonify(message="You are not an admin"), 403
  return jsonify(message="Welcome admin")

#  create a user
@app.route('/admin/users', methods=['POST'])
@jwt_required()
def createUser():
  user = get_jwt_identity()
  if user != "admin":
    return jsonify(message="You are not an admin"), 403
  username = request.json.get("username", None)
  email = request.json.get("email", None)
  password = request.json.get("password", None)
  hashedPassword = hashlib.sha256(password).hexdigest()
  user = User(username=username, email=email, password=hashedPassword)
  db.session.add(user)
  db.session.commit()
  return jsonify(username=username, email=email), 200

# delete a user
@app.route(('/admin/users/<int:id>/delete'), methods=['DELETE'])
@jwt_required()
def delete_user():
  user = get_jwt_identity()
  if user != "admin":
    return jsonify(message="You are not an admin"), 403
  user = User.query.filter_by(id=id).first()
  db.session.delete(user)
  db.session.commit()
  return jsonify(message="User deleted"), 200



if __name__ == '__main__':
    app.run()
