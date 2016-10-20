from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))

    task = db.relationship('Tasks', backref='author')

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Role %r>' % self.username


class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(32))
    description = db.Column('description', db.String(255))
    creation_date = db.Column('creation_date', db.Date)
    is_done = db.Column('is_done', db.Boolean)
    category = db.Column('category', db.String(32))
    priority = db.Column('priority', db.String(32))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Role %r>' % self.name
