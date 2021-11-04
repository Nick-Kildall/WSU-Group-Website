from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

@login.user_loader  
def load_user(id):
    return User.query.get(int(id))

userInterests = db.Table('userInterests',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('interest_id', db.Integer, db.ForeignKey('interest.id'))
)

postInterests = db.Table('postInterests',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('interest_id', db.Integer, db.ForeignKey('interest.id'))
)

# this is the beginning for the post model. i have added the details i need for
# the _post.html and index.html page
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    endDate = db.Column(db.String(64))
    startDate = db.Column(db.String(64))
    description = db.Column(db.String(2500))
    faculty_id = db.Column(db.String(20),db.ForeignKey('user.id'))
    commitment = db.Column(db.Integer)
    qualifications = db.Column(db.String(2500))
    # postInterests
    interests = db.relationship('Interest',
        secondary = postInterests,
        primaryjoin=(postInterests.c.post_id == id), 
        backref=db.backref('postInterests', lazy='dynamic'), 
        lazy='dynamic')

    def get_interests(self):
        return self.interests


class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    # postInterests
    posts = db.relationship("Post",
        secondary = postInterests,
        primaryjoin=(postInterests.c.interest_id == id),
        backref=db.backref('postInterests',
        lazy='dynamic'),
        lazy='dynamic')
    # userInterests
    users = db.relationship('User',
        secondary = userInterests,
        primaryjoin=(userInterests.c.interest_id == id),
        backref=db.backref('userInterests',
        lazy='dynamic'),
        lazy='dynamic')

    def __repr__(self):
        return '<ID: {} Name: {}>'.format(self.id,self.name)

"""
class User(UserMixin, db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(120),unique=True,index=True)
    #email = db.Column(db.String(120),unique=True,index=True)
    password_hash=db.Column(db.String(128))
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    phone_num=db.Column(db.String(15))
    wsu_id=db.Column(db.String(10),index=True)
    # userInterests
    interests = db.relationship("Interest",
        secondary = userInterests,
        primaryjoin=(userInterests.c.user_id == id),
        backref=db.backref('userInterests',
        lazy='dynamic'),
        lazy='dynamic')
    major = db.Column(db.String(64), default = "")
    gpa = db.Column(db.String(5),default = "")
    grad_date = db.Column(db.String(64),default = "")
    tech_electives = db.Column(db.String(1000),default = "")
    languages = db.Column(db.String(1000),default = "")
    prior_exp = db.Column(db.String(10000),default = "")
    #temp

    def __repr__(self):
        return '<ID: {} Username: {}>'.format(self.id,self.username)
    
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    
    def get_password(self, password):
        return check_password_hash(self.password_hash, password)


class Student(User, db.Model):
    pass
    # major = db.Column(db.String(64))
    # gpa = db.Column(db.String(5))
    # grad_date = db.Column(db.String(64))
    # tech_electives = db.Column(db.String(1000))
    # languages = db.Column(db.String(1000))
    # prior_exp = db.Column(db.String(10000))


class Faculty(User, db.Model):
    pass


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
"""

class User(Base):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username=db.Column(db.String(120),unique=True,index=True)
    #email = db.Column(db.String(120),unique=True,index=True)
    password_hash=db.Column(db.String(128))
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    phone_num=db.Column(db.String(15))
    wsu_id=db.Column(db.String(10),index=True)
    # userInterests
    interests = db.relationship("Interest",
        secondary = userInterests,
        primaryjoin=(userInterests.c.user_id == id),
        backref=db.backref('userInterests',
        lazy='dynamic'),
        lazy='dynamic')

    __mapper_args__ = {
        "polymorphic_identity": "user",
        'with_polymorphic': '*',
        "polymorphic_on": type
    }

    
    def __repr__(self):
        return '<ID: {} Username: {}>'.format(self.id,self.username)
    
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    
    def get_password(self, password):
        return check_password_hash(self.password_hash, password)

    #type = Column(String(50))

   
    def __repr__(self):
        return "User %s" % self.name


class Faculty(User):
    __tablename__ = "faculty"
    id = db.Column(db.ForeignKey("user.id"), primary_key=True)
    
    __mapper_args__ = {"polymorphic_identity": "faculty"}




class Student(User):
    __tablename__ = "user"
    id = db.Column(db.ForeignKey("person.id"), primary_key=True)
    status = db.Column(db.String(30))
    major = db.Column(db.String(64), default = "")
    gpa = db.Column(db.String(5),default = "")
    grad_date = db.Column(db.String(64),default = "")
    tech_electives = db.Column(db.String(1000),default = "")
    languages = db.Column(db.String(1000),default = "")
    prior_exp = db.Column(db.String(10000),default = "")
    

    __mapper_args__ = {"polymorphic_identity": "manager"}




