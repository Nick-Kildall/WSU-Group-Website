from datetime import datetime
from flask.helpers import flash
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login



class Association(db.Model):
    __tablename__ = 'association_table'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    interest_id = db.Column(db.Integer, db.ForeignKey('interest.id'), nullable=False)

    __table_args__ = (db.UniqueConstraint(user_id, post_id, interest_id))

    user = db.relationship("User")
    post = db.relationship("Post", back_populates = 'association_table')
    interest = db.relationship("Interest", back_populates = 'association_table')


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(150))
    endDate = db.Column(db.String(64))
    startDate = db.Column(db.String(64))
    description = db.Column(db.String(2500))
    faculty_id = db.Column(db.String(20),db.ForeignKey('user.id'))
    commitment = db.Column(db.Integer)
    qualifications = db.Column(db.String(2500))


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username=db.Column(db.String(120),unique=True,index=True)
    password_hash=db.Column(db.String(128))
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    phone_num=db.Column(db.String(15))
    wsu_id=db.Column(db.String(10),index=True)
    user_type = db.Column(db.String(50))

    def __repr__(self):
        return '<ID: {} Username: {}>'.format(self.id,self.username)
    
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    
    def get_password(self, password):
        return check_password_hash(self.password_hash, password)

class Interest(db.Model):
    __tablename__ = 'interest'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))