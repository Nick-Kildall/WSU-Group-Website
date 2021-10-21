from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for
from flask_sqlalchemy import sqlalchemy
from config import Config
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.Controller.auth_forms import FacultyRegForm
from app.Model.models import Faculty
bp_auth = Blueprint('auth', __name__)
bp_auth.template_folder = Config.TEMPLATE_FOLDER 

@bp_auth.route('/f_register', methods=['GET', 'POST'])
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