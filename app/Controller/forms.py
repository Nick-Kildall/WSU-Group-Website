from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import  ValidationError, Length, DataRequired, Email, EqualTo
from flask_login import current_user
from app.Model.models import Faculty

class StudentRegistrationForm(FlaskForm):
    username = StringField('Username - Enter your WSU Email',  validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',validators=[DataRequired(), EqualTo('password')])
    phone_num = StringField('Phone Number',  validators=[DataRequired()])
    first_name = StringField('First Name',  validators=[DataRequired()])
    last_name = StringField('Last Name',  validators=[DataRequired()])
    wsu_id = StringField('WSU ID',  validators=[DataRequired()])
    major = StringField('Major',  validators=[DataRequired()])
    gpa = StringField('GPA',  validators=[DataRequired()])
    grad_date = StringField('Graduation Date',  validators=[DataRequired()])
    tech_electives = StringField('Technical Electives',  validators=[DataRequired()])
    languages = StringField('Languages',  validators=[DataRequired()])
    prior_exp = StringField('Prior Experience',  validators=[DataRequired()])
    # Add interests
    submit = SubmitField('Submit')

class FacultyEditForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',validators=[DataRequired(),EqualTo('password')])
    phone_num = StringField('Phone Number',  validators=[DataRequired()])
    submit = SubmitField('Submit')

class StudentEditForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',validators=[DataRequired(), EqualTo('password')])
    phone_num = StringField('Phone Number',  validators=[DataRequired()])
    major = StringField('Major',  validators=[DataRequired()])
    gpa = StringField('GPA',  validators=[DataRequired()])
    grad_date = StringField('Graduation Date',  validators=[DataRequired()])
    tech_electives = StringField('Technical Electives',  validators=[DataRequired()])
    languages = StringField('Languages',  validators=[DataRequired()])
    prior_exp = StringField('Prior Experience',  validators=[DataRequired()])
    # Add interests
    submit = SubmitField('Submit')
