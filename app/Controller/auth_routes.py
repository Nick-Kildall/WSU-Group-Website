from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for
from flask_sqlalchemy import sqlalchemy
from config import Config
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.Controller.auth_forms import FacultyRegForm, StudentRegForm, LoginForm 
from app.Model.models import Faculty, Student, User
bp_auth = Blueprint('auth', __name__)
bp_auth.template_folder = Config.TEMPLATE_FOLDER 

@bp_auth.route('/faculty_registration', methods=['GET', 'POST'])
def f_register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('routes.index'))
    rform=FacultyRegForm()
    if rform.validate_on_submit():
        faculty=Faculty(username=rform.username.data, firstname=rform.firstname.data,
                        lastname=rform.lastname.data,phone_num=rform.phone_num.data,wsu_id=rform.wsu_id.data)
        faculty.set_password(rform.password.data)
        db.session.add(faculty)
        db.session.commit()
        flash('Congratulations, you are now a registered faculty member!')
        return redirect(url_for('routes.index'))
    return render_template('f_registration.html',form=rform)

@bp_auth.route('/student_registration', methods=['GET','POST'])
def student_registration():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    srform = StudentRegForm()
    if srform.validate_on_submit():
        newStudent = Student(username = srform.username.data, 
            phone_num = srform.phone_num.data, firstname = srform.firstname.data,
            lastname = srform.lastname.data, wsu_id = srform.wsu_id.data,
            major = srform.major.data, gpa = srform.gpa.data,
            grad_date = srform.grad_date.data, tech_electives = srform.tech_electives.data,
            languages = srform.languages.data, prior_exp = srform.prior_exp.data)
        newStudent.set_password(srform.password.data) 
        #for tempInterest in srform.interest.data:
        #    newStudent.interests.append(tempInterest)
        db.session.add(newStudent)
        db.session.commit()
        flash("Congratulations, you are now a registered student!")
        return redirect(url_for('routes.index'))
    print(srform.password.errors)
    print(srform.password.errors)
    print("out sform")
    return render_template('student_registration.html', title='Student Registration', form=srform)



@bp_auth.route('/login', methods =['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    lform = LoginForm()
    if lform.validate_on_submit():
        user = User.query.filter_by(username = lform.username.data).first()
        if(user is None) or (user.get_password(lform.password.data) == False):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember = lform.remember_me.data)
        return redirect(url_for('routes.index'))
    return render_template('login.html', title = 'Sign In', form=lform)

@bp_auth.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
