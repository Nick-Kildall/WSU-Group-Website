from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login

@login.user_loader  
def load_user(id):
    return Faculty.query.get(int(id))

class Faculty(db.Model):
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
