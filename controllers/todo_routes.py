from app import app, db
from jwt import JWT, jwt_required, get_jwt_identity
from flask import request, jsonify
from models import User, todoList, todoItem

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
