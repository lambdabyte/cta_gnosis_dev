from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

# Many to many table
usersubjects = db.Table('usersubjects',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'), primary_key=True),
    db.Column('subject_description', db.String(256)),
    db.Column('color', db.String(120))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    subjects = db.relationship('Subject', secondary=usersubjects, lazy='subquery',
        backref=db.backref('users', lazy=True))
    tasks = db.relationship('Task', backref='user', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(120), index=True, unique=True)
    tasks = db.relationship('Task', backref='subject', lazy=True)

    def __repr__(self):
        return '<Subject {}>'.format(self.subject_name)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(120), index=True)
    due_date = db.Column(db.DateTime, index=True)
    task_description = db.Column(db.String(256))
    task_type = db.Column(db.String(120), nullable=True, index=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'),
        nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    



# lets login module know where to find user id
@login.user_loader
def load_user(id):
    return User.query.get(int(id))  