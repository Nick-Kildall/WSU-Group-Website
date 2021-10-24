from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for
from flask_sqlalchemy import sqlalchemy
from config import Config
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.Controller.auth_forms import FacultyRegForm, StudentRegForm
from app.Model.models import Faculty, Student
bp_auth = Blueprint('auth', __name__)
bp_auth.template_folder = Config.TEMPLATE_FOLDER 

@bp_auth.route('/faculty_registration', methods=['GET', 'POST'])
def f_register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('routes.index'))
    rform=FacultyRegForm()
    if rform.validate_on_submit():
        faculty=Faculty(username=rform.username.data, email=rform.email.data, firstname=rform.firstname.data,
        lastname=rform.lastname.data,phone_num=rform.phone_num.data,wsu_id=rform.wsu_id.data)
        faculty.set_password(rform.password.data)
        db.session.add(faculty)
        db.session.commit()
        flash('Congratulations, you are now a registered faculty member!')
        return redirect(url_for('routes.index'))
    return render_template('f_registration.html',form=rform)

@bp_auth.route('/student_registration', methods=['GET','POST'])
def student_registration():
    # if current_user.is_authenticated:
    #     return redirect(url_for('routes.index'))
    srform = StudentRegForm()
    if srform.validate_on_submit():
        newStudent = Student(username = srform.username.data, 
        phone_num = srform.phone_num.data, first_name = srform.first_name.data,
        last_name = srform.last_name.data, wsu_id = srform.wsu_id.data,
        major = srform.major.data, gpa = srform.gpa.data,
        grad_date = srform.grad_date.data, tech_electives = srform.tech_electives.data,
        languages = srform.languages.data, prior_exp = srform.prior_exp.data)
        newStudent.set_password(srform.password.data) 
        for tempInterest in srform.interest.data:
            newStudent.interests.append(tempInterest)
        db.session.add(newStudent)
        db.session.commit()
        flash("Congratulations, you are now a registered student!")
        return render_template(url_for('routes.index'))
    return render_template('student_registration.html', title='Student Registration', form=srform)