"""
This file contains the functional tests for the routes.
These tests use GETs and POSTs to different URLs to check for the proper behavior.
Resources:
    https://flask.palletsprojects.com/en/1.1.x/testing/ 
    https://www.patricksoftwareblog.com/testing-a-flask-application-using-pytest/ 
"""
import os
import pytest
from app import create_app, db
from app.Model.models import User, Student, Faculty, Post, Interest, Apply, Application
from config import Config


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'bad-bad-key'
    WTF_CSRF_ENABLED = False
    DEBUG = True
    TESTING = True



@pytest.fixture(scope='module')
def test_client():
    # create the flask application ; configure the app for tests
    flask_app = create_app(config_class=TestConfig)

    db.init_app(flask_app)
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
 
    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
 
    yield  testing_client 
    # this is where the testing happens!
 
    ctx.pop()

def new_student(uname,uphn, ufirstname,ulastname,uwsuid,umajor,ugpa, ugraddate,utechelectives,ulanguages, upriorexp, passwd):
    user = Student(username = uname, 
            phone_num = uphn, firstname = ufirstname,
            lastname = ulastname, wsu_id = uwsuid,
            major = umajor, gpa = ugpa,
            grad_date = ugraddate, tech_electives = utechelectives,
            languages = ulanguages, prior_exp = upriorexp, user_type="Student")
    user.set_password(passwd)
    return user

def init_interests():
    # initialize the interests
    if Interest.query.count() == 0:
        interests = ['Artificial Intelligence/Machine Learning','Front End Developement', 'Back End Developement', 'Data Science', 'Software Engineering',
            'Web Development', 'Full Stack', 'Mobile Application', 'Game Development', 'Cybersecurity', 'Financial Analysis', 'Blockchain']
        for i in interests:
            db.session.add(Interest(name=i))
        db.session.commit()
    return None

@pytest.fixture
def init_database():
    # Create the database and the database table
    db.create_all()
    init_interests()
    
    #add a user    
    studentUser = new_student(uname = "selina@wsu.edu",uphn = "1234", ufirstname = "Selina",ulastname = "Nguyen",uwsuid = "1234567",umajor = "Computer Science",ugpa= "4.0", ugraddate = "May 2023",utechelectives = "CS 121",ulanguages = "C, C++, Python", upriorexp = " TA for 121", passwd = "123")
    # studentUser.interests.append("Data Science")
    # studentUser.interests.append("Full Stack")
    
    # Insert user data
    db.session.add(studentUser)
    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()

def test_register_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is requested (GET)
    THEN check that the response is valid
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.get('/student_registration')
    assert response.status_code == 200
    assert b"Student Registration" in response.data
