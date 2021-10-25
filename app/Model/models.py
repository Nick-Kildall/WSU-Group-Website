from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login


@login.user_loader  
def load_user(id):
    return Faculty.query.get(int(id))


studentInterests = db.Table('studentInterests',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('interest_id', db.Integer, db.ForeignKey('interest.id'))
)


# this is the beginning for the post model. i have added the details i need for
# the _post.html and index.html page
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
#    interests = db.relationship("Interest", secondary = studentInterests,
#        primaryjoin=(studentInterests.c.student_id == id),
#        backref=db.backref('studentInterests',
#        lazy='dynamic'), lazy='dynamic')


class User(UserMixin, db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(64),unique=True,index=True)
    email = db.Column(db.String(120),unique=True,index=True)
    password_hash=db.Column(db.String(128))
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    phone_num=db.Column(db.String(15))
    wsu_id=db.Column(db.String(10),unique=True,index=True)

    def __repr__(self):
        return '<ID: {} Username: {}>'.format(self.id,self.username)
    
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    
    def get_password(self, password):
        return check_password_hash(self.password_hash, password)


class Student(User, db.Model):
    major = db.Column(db.String(64))
    gpa = db.Column(db.String(5))
    grad_date = db.Column(db.String(64))
    tech_electives = db.Column(db.String(1000))
    languages = db.Column(db.String(1000))
    prior_exp = db.Column(db.String(10000))

    # The interests relationship could also be moved to the User class, and therefore will be inherited by the
    # faculty class as well. Faculty
    interests = db.relationship("Interest", secondary = studentInterests,
        primaryjoin=(studentInterests.c.student_id == id),
        backref=db.backref('studentInterests',
        lazy='dynamic'), lazy='dynamic')


class Faculty(User, db.Model):
    pass


class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __repr__(self):
        return '<ID: {} Name: {}>'.format(self.id,self.name)




'''
Sample class inheritence structure as follows
drouhana

class User(UserMixin, db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(64),unique=True,index=True)
    email = db.Column(db.String(120),unique=True,index=True)
    password_hash=db.Column(db.String(128))
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    phone_num=db.Column(db.String(15))
    wsu_id=db.Column(db.String(10),unique=True,index=True)

    def __repr__(self):
        return '<ID: {} Username: {}>'.format(self.id,self.username)
    
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    
    def get_password(self, password):
        return check_password_hash(self.password_hash, password)


class Student(User, db.Model):
    major = db.Column(db.String(64))
    gpa = db.Column(db.String(5))
    grad_date = db.Column(db.String(64))
    tech_electives = db.Column(db.String(1000))
    languages = db.Column(db.String(1000))
    prior_exp = db.Column(db.String(10000))

    # The interests relationship could also be moved to the User class, and therefore will be inherited by the
    # faculty class as well. Faculty
    interests = db.relationship("Interest", secondary = studentInterests,
        primaryjoin=(studentInterests.c.student_id == id),
        backref=db.backref('studentInterests',
        lazy='dynamic'), lazy='dynamic')


class Faculty(User, db.Model):
    pass

'''