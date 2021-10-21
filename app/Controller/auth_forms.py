from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,BooleanField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Length,Email
from app.Model.models import Faculty

class FacultyRegForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    username=StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_num = StringField('Phone Number',  validators=[DataRequired()])
    wsu_id = StringField('WSU ID', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        faculty=Faculty.query.filter_by(email=email.data).first()
        if faculty is not None:
            raise ValidationError('The email already exists! Please use a different email address.')

    def validate_username(self, username):
        faculty=Faculty.query.filter_by(username=username.data).first()
        if faculty is not None:
                raise ValidationError('The username already exists! Please use a different username.')

    def validate_wsuId(self, wsu_id):
        faculty=Faculty.query.filter_by(wsu_id=wsu_id.data).first()
        if faculty is not None:
                raise ValidationError('The WSU ID already exists!.')
