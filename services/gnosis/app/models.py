from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# Many to many table
usersubjects = db.Table('usersubjects',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    subjects = db.relationship('Subject', secondary=usersubjects, lazy='subquery',
        backref=db.backref('users', lazy=True))

    def __repr__(self):
        return '<User {}>'.format(self.username)    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(120), index=True, unique=True)
    color = db.Column(db.String(64))

    def __repr__(self):
        return '<Subject {}>'.format(self.subject_name)  