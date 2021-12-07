from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login import  current_user, login_required
from flask_wtf.recaptcha.widgets import RecaptchaWidget
from app.Model.models import Faculty, Student, Post, User, Application,Apply
from app.Controller.forms import FacultyEditForm, StudentEditForm, PostForm, SortForm, ApplicationForm
from config import Config

from app import db

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'

def get_posts(selection):
    if selection == "Recommended": #recommended
        posts = []
        available_interests = current_user.interests
        for interest in available_interests:
            posts.append(Post.query.filter_by(current_user.interests.contains(interest)).first())
        return posts
    elif selection == "View All": # view
        return Post.query.order_by(Post.id.desc()).all()
    else: # filter by specific interest
        return Post.query.filter(Post.interests.any(name = selection)).all()

#all_posts is used to reuse faculty home to display all posts 
#all_posts == 0 implies you are viewing just the faculty's posts 
@bp_routes.route('/f_index', methods=['GET', 'POST'])
@login_required
def f_index():
    posts = current_user.get_user_posts()
    return render_template('faculty_home.html', posts = posts,all_posts = 0)

@bp_routes.route('/', methods=['GET', 'POST'])
@bp_routes.route('/s_index', methods=['GET', 'POST'])
@login_required
def s_index():
    interest_list = []
    if (current_user.is_authenticated):
        # pull current user's interests
        available_interests = current_user.interests.all()
        interest_list = [(i.name) for i in available_interests]
        interest_list.append('Recommended')
        interest_list.append('View All')
        print(available_interests)
        
    else:
        load_defaults(interest_list)

    # create sortform
    sort_form = SortForm()
    # pass current user's interests to sortform
    sort_form.sort_by.choices = interest_list

    if sort_form.validate_on_submit():
        print("selection : " + str(sort_form.sort_by.data))
        posts = get_posts(sort_form.sort_by.data)
    else:
        posts = Post.query.order_by(Post.id.desc())
    print(posts)
    return render_template('student_home.html', posts = posts, form=sort_form)

# '''
#     if request.method == 'POST':
#         if sort_form.validate_on_submit():
#             # pull list of posts
#             posts = get_posts(sort_form.sort_by.data)
#             form = SortForm()
#             return render_template('index.html', posts = posts, form=sort_form)
#     if request.method == 'GET':
#         posts = Post.query.order_by(Post.id.desc())
#         return render_template('index.html', posts = posts, form=sort_form)
# '''

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
        newPost = Post(title = ppost.title.data,endDate = ppost.end_date.data, description = ppost.description.data,qualifications=ppost.qualifications.data, startDate = ppost.start_date.data,commitment = ppost.commitment.data, faculty_id = current_user.id)
        for i in ppost.interest.data:
            newPost.interests.append(i)
        db.session.add(newPost)
        db.session.commit()
        flash("Your post has been created.")
        print("testing: you are in the if statement")
        return redirect(url_for('routes.f_index'))
    return render_template('createpost.html', title='Create Post', form=ppost)


@bp_routes.route('/delete/<post_id>', methods=['DELETE', 'POST'])
@login_required
def delete(post_id):
    post = Post.query.filter_by(id = post_id).first()
    if post != None:
        for interest in post.interests:
            print("deleting interests:",interest)
            #post.interests.remove(interest)
       #  post.interests.clear()
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
       # theApply = Apply.query.filter_by(post_id = postid).first()
        str=""
        allInterests=current_user.interests.all()
        interest_list = [(i.name) for i in allInterests]
        for interests in interest_list:
            print(interests)
            str = str + " " + interests 
        
        ### adds varibles from the post and application
        theApplication = Application(student_id = current_user.id, post_id = postid,
            studentDescription = applyForm.studentDescription.data, reference_name = applyForm.reference_name.data,
            reference_email = applyForm.reference_email.data, title = thePost.title, endDate = thePost.endDate, 
            startDate = thePost.startDate, description = thePost.description, commitment = thePost.commitment,
            qualifications = thePost.qualifications, firstname = current_user.firstname, lastname = current_user.lastname,
            username = current_user.username, gpa=current_user.gpa,tech_electives=current_user.tech_electives, languages=current_user.languages,
            prior_exp=current_user.prior_exp, interests=str)
    
        db.session.add(theApplication)
        db.session.commit()

        return redirect(url_for("routes.s_index"))
   
    # sends student to application form
    return render_template('apply.html', title='Apply to Research Oppertunity', form=applyForm)

@bp_routes.route('/withdraw/<post_id>', methods=['GET','POST'])
def withdraw(post_id):
    thePost = Post.query.filter_by(id = post_id).first()
    current_user.withdraw(thePost)
    return redirect(url_for("routes.s_index"))

@bp_routes.route('/allposts', methods=['GET', 'POST'])
@login_required
def allposts():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('faculty_home.html', posts = posts,all_posts = 1)


