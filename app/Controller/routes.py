from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login import  current_user, login_required
from app.Controller.forms import FacultyEditForm, StudentEditForm
from config import Config
from app.Model.models import Faculty, Student

from app import db

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET'])
@bp_routes.route('/index', methods=['GET'])
def index():
    

    return render_template('index.html')

@bp_routes.route('/f_edit_profile', methods=['GET','POST'])
def f_edit_profile():
    eform=FacultyEditForm()
    # if request.method=='POST':
    #     if eform.validate_on_submit():
    #         current_user.phone_num=eform.phone_num.data
    #         current_user.set_password(eform.password.data)
    #         db.session.add(current_user)
    #         db.session.commit()
    #         flash("Your changes have been saved")
    #         return render_template(url_for('routes.index'))
    return render_template('f_edit_profile.html', title='Edit Profile', form=eform)

@bp_routes.route('/s_edit_profile', methods=['GET','POST'])
def s_edit_profile():
    sform = StudentEditForm()
    # if request.method=='POST':
    #     if sform.validate_on_submit():
    #         current_user.phone_num = sform.phone_num.data
    #         current_user.set_password(sform.password.data) 
    #         current_user.major = sform.major.data
    #         current_user.gpa = sform.gpa.data
    #         current_user.grad_date = sform.grad_date.data
    #         current_user.tech_electives = sform.tech_electives.data
    #         current_user.languages = sform.languages.data
    #         current_user.prior_exp = sform.prior_exp.data
    #         db.session.add(current_user)
    #         db.session.commit()
    #         flash("Your changes have been saved")
    #         return render_template(url_for('routes.index'))
    # elif (request.method == "GET"):
    #     # Populate DB with User data
    #     sform.phone_num.data = current_user.phone_num
    #     sform.major.data = current_user.major
    #     sform.gpa.data = current_user.gpa
    #     sform.grad_date.data = current_user.grad_date
    #     sform.tech_electives.data = current_user.tech_electives
    #     sform.languages.data = current_user.languages
    #     sform.prior_exp.data = current_user.prior_exp
    #     sform.interest.data = current_user.interest
    # else:
    #     pass 
    return render_template('s_edit_profile.html', title='Edit Profile', form=sform)