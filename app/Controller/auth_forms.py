from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Length,Email
from wtforms.widgets.core import CheckboxInput, ListWidget
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from app.Model.models import Faculty, Interest

def get_interests():
    return Interest.query.all()
 
def get_interestLabel(interest):
    return interest.name

class FacultyRegForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    username=StringField('Username', validators=[DataRequired()])
   # email = StringField('Email', validators=[DataRequired(), Email()])
    phone_num = StringField('Phone Number',  validators=[DataRequired()])
    wsu_id = StringField('WSU ID', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Submit')

    # def validate_email(self, email):
    #     faculty=Faculty.query.filter_by(email=email.data).first()
    #     if faculty is not None:
    #         raise ValidationError('The email already exists! Please use a different email address.')

    def validate_username(self, username):
        faculty=Faculty.query.filter_by(username=username.data).first()
        if faculty is not None:
                raise ValidationError('The username already exists! Please use a different username.')

    def validate_wsuId(self, wsu_id):
        faculty=Faculty.query.filter_by(wsu_id=wsu_id.data).first()
        if faculty is not None:
                raise ValidationError('The WSU ID already exists!.')

class StudentRegForm(FlaskForm):
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
    interest = QuerySelectMultipleField( 'Interest',
        query_factory= get_interests,
        get_label= get_interestLabel,
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput() )
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')