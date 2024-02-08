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

from models import db, User, todoList, todoItem


# Create a Flask application object and configure it
app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db.init_app(app)
migrate = Migrate(app, db)
app.config['JWT_SECRET_KEY'] = secret_key

jwt = JWTManager(app)

migration = Migrate(app, db)


#######################

# launch app
if __name__ == '__main__':
    app.run()
