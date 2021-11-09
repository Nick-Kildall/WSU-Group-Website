from datetime import datetime
from flask.helpers import flash
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login

@login.user_loader  
def load_user(id):
    return User.query.get(int(id))
 
    
    

studentInterests = db.Table('studentInterests',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('interest_id', db.Integer, db.ForeignKey('interest.id'))
)

postInterests = db.Table('postInterests',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('interest_id', db.Integer, db.ForeignKey('interest.id'))
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    endDate = db.Column(db.String(64))
    startDate = db.Column(db.String(64))
    description = db.Column(db.String(2500))
    faculty_id = db.Column(db.String(20),db.ForeignKey('user.id'))
    commitment = db.Column(db.Integer)
    qualifications = db.Column(db.String(2500))
    students_applied = db.relationship("Applied", back_populates = "post_applied")
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

    posts = db.relationship("Post",
        secondary = postInterests,
        primaryjoin=(postInterests.c.interest_id == id),
        backref=db.backref('postInterests',
        lazy='dynamic'),
        lazy='dynamic')
    users = db.relationship('User',
        secondary = studentInterests,
        primaryjoin=(studentInterests.c.interest_id == id),
        backref=db.backref('studentInterests',
        lazy='dynamic'),
        lazy='dynamic')

    def __repr__(self):
        return '<ID: {} Name: {}>'.format(self.id,self.name)

class User(db.Model,UserMixin):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username=db.Column(db.String(120),unique=True,index=True)
    password_hash=db.Column(db.String(128))
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    phone_num=db.Column(db.String(15))
    wsu_id=db.Column(db.String(10),index=True)
    user_type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'users',
        'polymorphic_on':user_type
    }
    
    def __repr__(self):
        return '<ID: {} Username: {}>'.format(self.id,self.username)
    
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    
    def get_password(self, password):
        return check_password_hash(self.password_hash, password)
   
    def __repr__(self):
        return "User %s" % self.name


class Faculty(User):
    __tablename__='faculty'
    id = db.Column(db.ForeignKey("user.id"), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'Faculty'
    }



class Student(User):
    __tablename__='student'
    id = db.Column(db.ForeignKey("user.id"), primary_key=True)
    major = db.Column(db.String(64), default = "")
    gpa = db.Column(db.String(5),default = "")
    grad_date = db.Column(db.String(64),default = "")
    tech_electives = db.Column(db.String(1000),default = "")
    languages = db.Column(db.String(1000),default = "")
    prior_exp = db.Column(db.String(10000),default = "")
    applications = db.relationship("Applied", back_populates = "student_applied")
    interests = db.relationship("Interest",
        secondary = studentInterests,
        primaryjoin=(studentInterests.c.user_id == id),
        backref=db.backref('studentInterests',
        lazy='dynamic'),
        lazy='dynamic')
    __mapper_args__ = {
        'polymorphic_identity': 'Student',
    }
    
    def apply(self, thePost):
        if not self.is_applied(thePost):
            newApplication = Applied(post_applied = thePost)
            self.applications.append(newApplication)
            db.session.commit()
            flash('Applied to post {}'.format(thePost.title))
        else:
            flash("Already applied to post")
    
    def is_applied(self, thePost):
        return (Applied.query.filter_by(student_id = self.id).filter_by(post_id = thePost.id).count() > 0)

class Applied(db.Model):
    ### Relationships
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key = True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key = True)
    student_applied = db.relationship('Student')
    post_applied = db.relationship('Post')

    ### Application Form elements
    # description = db.Column(db.String(2500))
    # reference_name = db.Column(db.String(256))
    # reference_email = db.Column(db.String(256))




