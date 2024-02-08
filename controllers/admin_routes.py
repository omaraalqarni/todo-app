from app import app, db
from flask import request, jsonify
from flask_jwt_extended import (
  jwt_required,
  get_jwt_identity
  )
from models import User
import hashlib

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
