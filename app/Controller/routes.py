from __future__ import print_function
from re import L
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login import  current_user, login_required
from flask_wtf.recaptcha.widgets import RecaptchaWidget
from app.Model.models import Faculty, Student, Post, User, Application,Apply
from app.Controller.forms import FacultyEditForm, StudentEditForm, PostForm, SortForm, ApplicationForm
from app.Controller.auth_forms import LoginForm
from config import Config

from app import db

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'

def load_defaults(_list):
    interests = ["Artificial Intelligence/Machine Learning", "Front End Development", "Back End Develoipment",
        "Data Science", "Software Engineering", "Web Development", "Full Stack", "Mobile Application", "Game Development",
        "Cybersecurity"]
    i = 0
    for interest in interests:
        _list.append([i, interest])
        i += 1
    _list.append([i+1, "Recommended"])
    _list.append([i+1, "View All"])
    return

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
def index():
    if (current_user.is_authenticated):
        if (current_user.user_type == 'Student'):
            return redirect(url_for('routes.s_index'))
        elif (current_user.user_type == 'Faculty'):
            return redirect(url_for('routes.f_index'))
    else:
        lform = LoginForm()
        return render_template('login.html', form = lform)


@bp_routes.route('/f_index', methods=['GET', 'POST'])
@login_required
def f_index():
    posts = current_user.get_user_posts()
    return render_template('faculty_home.html', posts = posts,all_posts = 0)


@bp_routes.route('/s_index', methods=['GET', 'POST'])
@login_required
def s_index():
    interest_list = []
    if (current_user.is_authenticated):
        # pull current user's interests
        available_interests = current_user.interests.all()
        interest_list = [(i.id, i.name) for i in available_interests]
        interest_list.append([len(available_interests), 'Recommended'])
        interest_list.append([len(available_interests)+1, 'View All'])
    else:
        load_defaults(interest_list)

    # create sortform
    sort_form = SortForm()
    # pass current user's interests to sortform
    sort_form.sort_by.choices = interest_list
    if sort_form.validate_on_submit():
            posts = get_posts(sort_form.sort_by.data)
            form = SortForm()
    else:
        posts = Post.query.order_by(Post.id.desc())
    return render_template('student_home.html', posts = posts, form=sort_form)
'''
    if request.method == 'POST':
        if sort_form.validate_on_submit():
            # pull list of posts
            posts = get_posts(sort_form.sort_by.data)
            form = SortForm()
            return render_template('index.html', posts = posts, form=sort_form)
    if request.method == 'GET':
        posts = Post.query.order_by(Post.id.desc())
        return render_template('index.html', posts = posts, form=sort_form)
'''



@bp_routes.route('/<userid>/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile(userid):
    if current_user.account_type == 0:  # faculty edit pages
        eform=FacultyEditForm()
        return render_template('f_edit_profile.html', title='Edit Profile', form=eform)
    else:
        sform = StudentEditForm()
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
            return redirect(url_for('routes.f_index'))
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
                current_user.interests=sform.interest.data

                db.session.add(current_user)
                db.session.commit()
                flash("Your changes have been saved")
                return redirect(url_for('routes.s_index'))
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
            sform.interest.data = current_user.interests
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
        return redirect(url_for('routes.f_index'))
    return render_template('createpost.html', title='Create Post', form=ppost)


@bp_routes.route('/delete/<post_id>', methods=['GET', 'POST'])
@login_required
def delete(post_id):
    post = Post.query.filter_by(id = post_id).first()
    if post != None:
        #for interest in Post.interests:
        #    Post.interests.remove(interest)
        db.session.delete(post)
        db.session.commit()
    flash('Post deleted!')
    # posts = Post.query.order_by(Post.id.desc())
    return redirect(url_for('routes.f_index'))


@bp_routes.route('/s_your_app', methods=['GET','POST'])
@login_required
def s_your_app():

    ### Query all applications to render
    studentApplications = Application.query.filter_by(student_id = current_user.id).all()
    print("student Apps:")
    print(studentApplications)
    print(current_user.id)
    for app in Application.query.filter_by(student_id = current_user.id).all():
        print(app.student_id)
    return render_template('s_your_apps.html',title='Your Application', studentApplications = studentApplications)



@bp_routes.route('/applicants/<post_id>', methods=['GET'])
@login_required
def applicants(post_id):
    thepost = Post.query.filter_by(id = post_id).first()
    if thepost is None:
        flash("Error")
        return redirect(url_for('routes.faculty_home'))
    studentApplications = Application.query.filter_by(post_id = post_id).all()
    return render_template('post_student_list.html', studentApplications = studentApplications)


@bp_routes.route('/apply/<postid>', methods=['GET','POST'])
def apply(postid): 
    applyForm = ApplicationForm()
    # Applies student to postition
    if applyForm.validate_on_submit(): 
        thePost = Post.query.filter_by(id = postid).first()
        if thePost is None:
            flash("Post with id '{}' not found").format(postid)
            return redirect(url_for("routes.s_index"))
        ### creates many-to-many relationship
        current_user.apply(thePost)
        #print(current_user.applications)
        theApply = Apply.query.filter_by(post_id = postid).first()
        ### adds varibles from the post and application
        theApplication = Application(student_id = current_user.id, post_id = postid,
            studentDescription = applyForm.studentDescription.data, reference_name = applyForm.reference_name.data,
            reference_email = applyForm.reference_email.data, title = thePost.title, endDate = thePost.endDate, 
            startDate = thePost.startDate, description = thePost.description, commitment = thePost.commitment,
            qualifications = thePost.qualifications, firstname = current_user.firstname, lastname = current_user.lastname,
            username = current_user.username)
    
        db.session.add(theApplication)
        db.session.commit()
        print("HEY THIS SORT OF DEFINITELY WORKED")
        print("pushed app")
        print(Application.query.all())

        allAppsForPost = Application.query.filter_by(post_id = postid).all()
        for app in allAppsForPost:
            print(app.firstname + app.lastname)

        return redirect(url_for("routes.s_index"))
   
    # sends student to application form
    return render_template('apply.html', title='Apply to Research Oppertunity', form=applyForm)

    #     current_user.apply(postid, newApplication)
    #     flash("You successfully applied")
    #     return redirect(url_for("routes.index"))
    #return render_template('apply.html', title = 'Apply', form = applyform)


@bp_routes.route('/withdraw/<post_id>', methods=['GET','POST'])
def withdraw(post_id):
    _post = Post.query.filter_by(id = post_id).first()
    if current_user.is_applied(_post):
        _application = Application.query.filter_by(id = post_id, student_id = current_user.id).first()
        db.session.remove(_application)
        db.session.commit()
        return redirect(url_for("routes.s_index"))
    else:
        flash('No pending application to posting found')
        return redirect(url_for("routes.s_index"))

@bp_routes.route('/allposts', methods=['GET', 'POST'])
@login_required
def allposts():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('faculty_home.html', posts = posts,all_posts = 1)


