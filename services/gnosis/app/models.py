from app import db

# Many to many table
usersubjects = db.Table('usersubjects',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    subjects = db.relationship('Subject', secondary=usersubjects, lazy='subquery',
        backref=db.backref('users', lazy=True))

    def __repr__(self):
        return '<User {}>'.format(self.username)    

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(120), index=True, unique=True)
    color = db.Column(db.String(64))

    def __repr__(self):
        return '<Subject {}>'.format(self.subject_name)  