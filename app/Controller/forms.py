from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.widgets.core import CheckboxInput, ListWidget
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import  ValidationError, Length, DataRequired, Email, EqualTo
from flask_login import current_user
from app.Model.models import Faculty, Interest

def get_interests():
    return Interest.query.all()
 
def get_interestLabel(interest):
    return interest.name

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
    interest = QuerySelectMultipleField( 'Interest',
        query_factory= get_interests,
        get_label= get_interestLabel,
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput() )
    submit = SubmitField('Submit')
