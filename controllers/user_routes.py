from app import db
from flask import request, jsonify, Blueprint

import hashlib
from models import User
from flask_jwt_extended import (
  create_access_token,
  get_jwt_identity,
  jwt_required
  )


user = Blueprint('user', __name__)



# signup route
@user.route('/signup', methods=['POST'])
def signUp():
  username = request.json.get("username", None)
  email = request.json.get("email", None)
  password = request.json.get("password", None)
  hashedPassword = hashlib.sha256(password.encode()).hexdigest()
  user = User(username=username, email=email, password=hashedPassword)
  
  #check if username or email already exists
  if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
    return jsonify(message="Username already exists")
    
  db.session.add(user)
  db.session.commit()
  return jsonify(username=username, email=email)

# sign in route
@user.route('/login', methods=['POST'])
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
@user.route('/profile', methods=['GET'])
@jwt_required()
def profile():
  user = get_jwt_identity()
  return jsonify(username=user), 200

# update user profile
@user.route('/profile', methods=['PUT'])
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
