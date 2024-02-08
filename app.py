from flask import Flask
from flask_migrate import Migrate
from flask_moment import Moment
from config import secret_key
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from controllers.todo_routes import todo
from controllers.user_routes import user
from controllers.admin_routes import admin_route



# Create a Flask application object and configure it
app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = secret_key
app.register_blueprint(user)
app.register_blueprint(admin_route)
app.register_blueprint(todo)

migration = Migrate(app, db)

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'


#######################

# launch app
if __name__ == '__main__':
  app.debug= True
  app.run(ssl_context=('ssl-certs/server.crt', 'ssl-certs/server.key'))

