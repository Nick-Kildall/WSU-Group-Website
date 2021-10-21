from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login import  current_user, login_required
from app.Controller.forms import FacultyEditForm
from config import Config
from app.Model.models import Faculty

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