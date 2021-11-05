from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login import  current_user, login_required
from flask_wtf.recaptcha.widgets import RecaptchaWidget
from app.Model.models import Faculty, Student, Post, User
from app.Controller.forms import FacultyEditForm, StudentEditForm, PostForm, SortForm
from config import Config

from app import db

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


def get_posts(selection):
    if selection == 'Recommended':
        available_interests = current_user.interests.query.all()
        for interest in available_interests:
            posts = []
            posts.append(Post.query.filter_by(interest).first())
        return posts
    elif selection == 'View All':
        return Post.query.order_by(Post.id.desc())
    else:
        print(selection)
        return Post.query.filter(Post.interests.any(name = selection)).all()


@bp_routes.route('/', methods=['GET', 'POST'])
@bp_routes.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    interest_list = []

    #if (current_user.is_authenticated):
    #    # pull current user's interests
    #    available_interests = current_user.interests.query.all()
    #    interest_list = [(i.id, i.name) for i in available_interests]
    #    interest_list.append([len(available_interests), 'Recommended'])
    #    interest_list.append([len(available_interests)+1, 'View All'])
    #else:
    j = 0
    interest_list.append([1, 'Machine Learning'])
    interest_list.append([2, 'Full Stack'])
    interest_list.append([3, 'Financial Modeling'])
    interest_list.append([4, 'Recommended'])
    interest_list.append([5, 'View All'])

    # create sortform
    sort_form = SortForm()
    # pass current user's interests to sortform
    sort_form.sort_by.choices = interest_list
    if sort_form.validate_on_submit():
            posts = get_posts(sort_form.sort_by.data)
            form = SortForm()
    else:
        posts = Post.query.order_by(Post.id.desc())
    return render_template('index.html', posts = posts, form=sort_form)

    # if request.method == 'POST':
    #     if sort_form.validate_on_submit():
    #         # pull list of posts
    #         posts = get_posts(sort_form.sort_by.data)
    #         form = SortForm()
    #         return render_template('index.html', posts = posts, form=sort_form)
    # if request.method == 'GET':
    #     posts = Post.query.order_by(Post.id.desc())
    #     return render_template('index.html', posts = posts, form=sort_form)



@bp_routes.route('/<userid>/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile(userid):
    if current_user.account_type == 0:  # faculty edit pages
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
    else:
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
    return

@bp_routes.route('/f_edit_profile', methods=['GET','POST'])
@login_required
def f_edit_profile():
    eform=FacultyEditForm()
    if request.method=='POST':
        if eform.validate_on_submit():
            current_user.phone_num=eform.phone_num.data
            current_user.set_password(eform.password.data)
            db.session.add(current_user)
            db.session.commit()
            flash("Your changes have been saved")
            return redirect(url_for('routes.index'))
        elif (request.method == "GET"):
            eform.phone_num.data=current_user.phone_num
        else:
            pass
    return render_template('f_edit_profile.html', title='Edit Profile', form=eform)

@bp_routes.route('/s_edit_profile', methods=['GET','POST'])
@login_required
def s_edit_profile():
    sform = StudentEditForm()
    if request.method=='POST':
        if current_user.user_type == "Student":
            if sform.validate_on_submit():
                current_user.phone_num = sform.phone_num.data
                current_user.set_password(sform.password.data) 
                current_user.major = sform.major.data
                current_user.gpa = sform.gpa.data
                current_user.grad_date = sform.grad_date.data
                current_user.tech_electives = sform.tech_electives.data
                current_user.languages = sform.languages.data
                current_user.prior_exp = sform.prior_exp.data
                db.session.add(current_user)
                db.session.commit()
                flash("Your changes have been saved")
                return redirect(url_for('routes.index'))
    elif (request.method == "GET"):
        # Populate DB with User data
        
        if current_user.user_type == "Student":
            sform.phone_num.data = current_user.phone_num
            sform.major.data = current_user.major
            sform.gpa.data = current_user.gpa
            sform.grad_date.data = current_user.grad_date
            sform.tech_electives.data = current_user.tech_electives
            sform.languages.data = current_user.languages
            sform.prior_exp.data = current_user.prior_exp
        #sform.interest.data = current_user.interest
    else:
        pass 
    return render_template('s_edit_profile.html', title='Edit Profile', form=sform)

@bp_routes.route('/createpost', methods=['GET','POST'])
@login_required
def createpost():
    ppost = PostForm()
    if ppost.validate_on_submit(): 
        newPost = Post(title = ppost.title.data,endDate = ppost.end_date.data, description = ppost.description.data,qualifications=ppost.qualifications.data, startDate = ppost.start_date.data,commitment = ppost.commitment.data, interests = ppost.interest.data,faculty_id = current_user.id)
        for i in newPost.interests:
            newPost.interests.append(i)
        db.session.add(newPost)
        db.session.commit()
        flash("Your post has been created.")
        return redirect(url_for('routes.index'))
    return render_template('createpost.html', title='Create Post', form=ppost)


@bp_routes.route('/apply', methods=['GET','POST'])
def apply(studentid):
    return