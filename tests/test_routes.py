"""
This file contains the functional tests for the routes.
These tests use GETs and POSTs to different URLs to check for the proper behavior.
Resources:
    https://flask.palletsprojects.com/en/1.1.x/testing/ 
    https://www.patricksoftwareblog.com/testing-a-flask-application-using-pytest/ 
"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))
import pytest
from app import create_app, db
from app.Model.models import User, Student, Faculty, Post, Interest, Apply, Application
from config import Config


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://' # + os.path.join(basedir, 'r_connect.db')
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
    #interestStudent = Interest('Data Science')
    #db.session.add(interestStudent)
    interestStudent = Interest.query.filter_by(name = 'Data Science').first()
    user.interests.append(interestStudent)
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
    studentUser = new_student(uname = 'selina@wsu.edu',uphn = '1234', ufirstname = 'Selina',ulastname = 'Nguyen',uwsuid = '1234567',umajor = 'Computer Science',ugpa= '4.0', ugraddate = 'May 2023',utechelectives = 'CS 121',ulanguages = 'C, C++, Python', upriorexp = 'TA for 121', passwd = '123')
    # Insert user data
    db.session.add(studentUser)
    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()

def test_register_page(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is requested (GET)
    THEN check that the response is valid
    """
    #https://gehrcke.de/2015/05/in-memory-sqlite-database-and-flask-a-threading-trap/
    # Create a test client using the Flask application configured for testing
    response = test_client.get('/student_registration')
    assert response.status_code == 200
    assert b"Submit" in response.data

def test_register(test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.post('/student_registration', 
                          data=dict(username = 'sejal@wsu.edu',phone_num = '1234', 
                          firstname = 'Sejal',lastname = 'Welankar',
                          wsu_id = '789012345',major = 'Computer Science',
                          gpa= '4.0', grad_date = 'May 2023',
                          tech_electives = 'CS 121',languages = 'C, C++, Python', 
                          prior_exp = 'TA for 121', password = '123', password2 = '123'),
                          follow_redirects = True)
    assert response.status_code == 200

    s = db.session.query(Student).filter(Student.username =='sejal@wsu.edu')
    assert s.first().wsu_id == '789012345'
    assert s.count() == 1
    assert b"Click to Register" in response.data   
    assert b"Please log in to access this page." in response.data






