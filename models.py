from sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
  