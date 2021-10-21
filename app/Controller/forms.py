from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import  ValidationError, Length, DataRequired, Email, EqualTo
from flask_login import current_user
from app.Model.models import Faculty


class FacultyEditForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',validators=[DataRequired(),EqualTo('password')])
    phone_num = StringField('Phone Number',  validators=[DataRequired()])
    submit = SubmitField('Submit')

    

