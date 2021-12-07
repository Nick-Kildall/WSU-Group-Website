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
    user.set_password(passwd)
    interestStudent = Interest.query.filter_by(name = 'Data Science').first()
    user.interests.append(interestStudent)
    return user

def new_faculty(uname,uphn, ufirstname,ulastname,uwsuid, passwd):
    user = Faculty(username = uname, 
            phone_num = uphn, firstname = ufirstname,
            lastname = ulastname, wsu_id = uwsuid,
           user_type="Faculty")
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
    studentUser = new_student(uname = 'selina@wsu.edu',uphn = '1234', ufirstname = 'Selina',ulastname = 'Nguyen',uwsuid = '1234567',
        umajor = 'Computer Science',ugpa= '4.0', ugraddate = 'May 2023',utechelectives = 'CS 121',
        ulanguages = 'C, C++, Python', upriorexp = 'TA for 121', passwd = '123')
    facultyUser = new_faculty(uname = "sakire@wsu.edu",uphn = "1234", ufirstname = "Sakire",ulastname = "Arslan Ay",uwsuid = "7891012", passwd="123")

    # Insert user data
    db.session.add(facultyUser)
    db.session.add(studentUser)
    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()

def test_student_register_page(test_client, init_database):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/register' page is requested (GET)
#     THEN check that the response is valid
#     """
# Create a test client using the Flask application configured for testing
    response = test_client.get('/student_registration')
    assert response.status_code == 200
    assert b"Submit" in response.data

def test_faculty_register_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is requested (GET)
    THEN check that the response is valid
    """
    #https://gehrcke.de/2015/05/in-memory-sqlite-database-and-flask-a-threading-trap/
    # Create a test client using the Flask application configured for testing
    response = test_client.get('/faculty_registration')
    assert response.status_code == 200
    assert b"Submit" in response.data

def test_faculty_edit(test_client, init_database):
    
    response = test_client.post('/login', 
                          data=dict(username='sakire@wsu.edu', password='123',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Research Connect!" in response.data

    response = test_client.get('/f_edit_profile')
    assert response.status_code == 200
    assert b"Edit Faculty Profile" in response.data

    response = test_client.post('/f_edit_profile', 
                          data=dict(phone_num="3602928820" ),
                          follow_redirects = True)
    s = db.session.query(Faculty).filter(Faculty.username=='sakire@wsu.edu')
    assert s.first().phone_num =="3602928820"
    assert b"Welcome to Research Connect!" in response.data

    response = test_client.get('/logout',                       
                          follow_redirects = True)
    print(response.data)
    assert response.status_code == 200
    assert b"Sign In" in response.data


def test_student_edit(test_client, init_database):
    
    response = test_client.post('/login',
                                data=dict(username='selina@wsu.edu', password='123', remember_me=False),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome to Research Connect!" in response.data
    
    response = test_client.get('/s_edit_profile')
    assert response.status_code == 200
    assert b"Student Edit Form" in response.data

    response = test_client.get('/logout',                       
                          follow_redirects = True)
    print(response.data)
    assert response.status_code == 200
    assert b"Sign In" in response.data


def test_faculty_register(test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    #uname = "sakire@wsu.edu",uphn = "1234", ufirstname = "Sakire",ulastname = "Arslan Ay",uwsuid = "7891012", passwd="123"
    # Create a test client using the Flask application configured for testing
    response = test_client.post('/faculty_registration', 
                          data=dict(username = "nick@wsu.edu", firstname = "Sakire", lastname = "Arslan Ay", phone_num = "1234", wsu_id = "66666696969",password = '123', password2 = '123' ),
                          follow_redirects = True)
    assert response.status_code == 200

    s = db.session.query(Faculty).filter(Faculty.username=='nick@wsu.edu')
    assert s.first().username == 'nick@wsu.edu'
    assert s.count() == 1
    print(s.count())
    assert b"Sign In" in response.data   
    assert b"Please log in to access this page." in response.data

def test_student_withdrawal(test_client, init_database):
   
    response = test_client.post('/login', 
                          data=dict(username='sakire@wsu.edu', password='123',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Research Connect!" in response.data

    response = test_client.get('/createpost')
    assert response.status_code == 200
    assert b"Post Research Opportunity" in response.data
    interests1 = list( map(lambda t: t.id, Interest.query.all()[:3]))  
    response = test_client.post('/createpost', 
                          data=dict(title='My third application test post', description='This is my third test post.',qualifications="testing qual",
                          start_date="test1", end_date = "test2", commitment = 1, interest = interests1 ),
                          follow_redirects = True)
    c = db.session.query(Post).filter(Post.title =='My third application test post')
    assert c.first().get_interests().count() == 3 #should have 3 tags
    assert c.count() == 1          
    assert response.status_code == 200
    assert b"Welcome to Research Connect!" in response.data
    assert b"My third application test post" in response.data 
    assert b"This is my third test post." in response.data


    response = test_client.get('/logout',                       
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Sign In" in response.data

    response = test_client.post('/login', 
                          data=dict(username='selina@wsu.edu', password='123',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Research Connect!" in response.data

    
    p = db.session.query(Post).filter(Post.title =='My third application test post')
    assert c.first().get_interests().count() == 3 #should have 3 tags
    assert c.count() == 1 
    response = test_client.post('/apply/'+str(p.first().id), 
                        data = dict(studentDescription = 'I am a CS major interested in cybersecurity', reference_name = 'Andy Fallon', reference_email = 'andyfallon@wsu.edu' ),
                        follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Research Connect" in response.data

    
    response =test_client.post('/withdraw/'+str(p.first().id), follow_redirects = True)
    assert response.status_code == 200
    assert b"Withdrew from post My third application test post" in response.data
    response = test_client.get('/logout',                       
                          follow_redirects = True)
    print(response.data)
    assert response.status_code == 200
    assert b"Sign In" in response.data
def test_createpost(test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' form is submitted (POST) with wrong credentials
    THEN check that the response is valid and login is refused 
    """
    response = test_client.post('/login', 
                          data=dict(username='sakire@wsu.edu', password='123',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Research Connect!" in response.data

    response = test_client.get('/createpost')
    assert response.status_code == 200
    assert b"Post Research Opportunity" in response.data
    response = test_client.post('/createpost', 
                          data=dict(title='My test post', description='This is my first test post.',qualifications="testing qual",
                          start_date="test1", end_date = "test2", commitment = 1 ),
                          follow_redirects = True)
    c = db.session.query(Post).filter(Post.title =='My test post')
    assert c.count() >= 1
    print(response.data)
    assert response.status_code == 200

    assert b"Welcome to Research Connect!" in response.data
    assert b"My test post" in response.data 
    assert b"This is my first test post." in response.data

    response = test_client.get('/logout',                       
                          follow_redirects = True)
    print(response.data)
    assert response.status_code == 200
    assert b"Sign In" in response.data

def test_faculty_login_logout(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' form is submitted (POST) with correct credentials
    THEN check that the response is valid and login is succesfull 
    """
    response = test_client.post('/login', 
                          data=dict(username='sakire@wsu.edu', password='123',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Research Connect!" in response.data

    response = test_client.get('/logout',                       
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Sign In" in response.data

def test_student_register(test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.post('/student_registration', 
                            data=dict(username = 'sejal@wsu.edu',phone_num = '1234', 
                            firstname = 'Sejal',lastname = 'Welankar',
                            wsu_id = '987654',major = 'Computer Science',
                            gpa= '4.0', grad_date = 'May 2023',
                            tech_electives = 'CS 121',languages = 'C, C++, Python', 
                            prior_exp = 'TA for 121', password = '123', password2 = '123'),
                            follow_redirects = True)

    assert response.status_code == 200

    s = db.session.query(Student).filter(Student.username =='sejal@wsu.edu')
    assert s.first().wsu_id == '987654'
    assert s.count() == 1
    assert b"Sign In" in response.data   
    assert b"Please log in to access this page." in response.data


def test_review_application(test_client, init_database):
    response = test_client.post('/login', 
                          data=dict(username='sakire@wsu.edu', password='123',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Research Connect!" in response.data

    response = test_client.get('/createpost')
    assert response.status_code == 200
    assert b"Post Research Opportunity" in response.data
    interests1 = list( map(lambda t: t.id, Interest.query.all()[:3]))  
    response = test_client.post('/createpost', 
                          data=dict(title='My fourth application test post', description='This is my third test post.',qualifications="testing qual",
                          start_date="test1", end_date = "test2", commitment = 1, interest = interests1 ),
                          follow_redirects = True)
    c = db.session.query(Post).filter(Post.title =='My fourth application test post')
    assert c.first().get_interests().count() == 3 #should have 3 tags
    assert c.count() == 1          
    assert response.status_code == 200
    assert b"Welcome to Research Connect!" in response.data
    assert b"My fourth application test post" in response.data 
    assert b"This is my third test post." in response.data


    response = test_client.get('/logout',                       
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Sign In" in response.data

    response = test_client.post('/login', 
                          data=dict(username='selina@wsu.edu', password='123',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Research Connect!" in response.data

    
    p = db.session.query(Post).filter(Post.title =='My fourth application test post')
    assert c.first().get_interests().count() == 3 #should have 3 tags
    assert c.count() == 1 
    response = test_client.post('/apply/'+str(p.first().id), 
                        data = dict(studentDescription = 'I am a CS major interested in cybersecurity', reference_name = 'Andy Fallon', reference_email = 'andyfallon@wsu.edu' ),
                        follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Research Connect" in response.data

    response = test_client.get('/logout',                       
                          follow_redirects = True)
    print(response.data)
    assert response.status_code == 200
    assert b"Sign In" in response.data

    response = test_client.post('/login', 
                          data=dict(username='sakire@wsu.edu', password='123',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Research Connect!" in response.data
    p = db.session.query(Post).filter(Post.title =='My fourth application test post')
    # # /reviewApp/<app_id>
    response = test_client.get('/applicants/'+str(p.first().id),follow_redirects=True)
    assert response.status_code == 200
    assert b"Applicants" in response.data
    response= test_client.get('/reviewApp/'+str(p.first().students_applied),follow_redirects=True)
    assert response.status_code == 200
    assert b"My fourth application test post - Selina Nguyen"
    
    response = test_client.get('/logout',                       
                          follow_redirects = True)
    print(response.data)
    assert response.status_code == 200
    assert b"Sign In" in response.data


def test_apply(test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' form is submitted (POST) with wrong credentials
    THEN check that the response is valid and login is refused 
    """
    response = test_client.post('/login', 
                          data=dict(username='sakire@wsu.edu', password='123',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Research Connect!" in response.data

    response = test_client.get('/createpost')
    assert response.status_code == 200
    assert b"Post Research Opportunity" in response.data
    interests1 = list( map(lambda t: t.id, Interest.query.all()[:3]))  
    response = test_client.post('/createpost', 
                          data=dict(title='My second application test post', description='This is my third test post.',qualifications="testing qual",
                          start_date="test1", end_date = "test2", commitment = 1, interest = interests1 ),
                          follow_redirects = True)
    c = db.session.query(Post).filter(Post.title =='My second application test post')
    assert c.first().get_interests().count() == 3 #should have 3 tags
    assert c.count() == 1          
    assert response.status_code == 200
    assert b"Welcome to Research Connect!" in response.data
    assert b"My second application test post" in response.data 
    assert b"This is my third test post." in response.data


    response = test_client.get('/logout',                       
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Sign In" in response.data

    response = test_client.post('/login', 
                          data=dict(username='selina@wsu.edu', password='123',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Research Connect!" in response.data

    
    p = db.session.query(Post).filter(Post.title =='My second application test post')
    assert c.first().get_interests().count() == 3 #should have 3 tags
    assert c.count() == 1 
    response = test_client.post('/apply/'+str(p.first().id), 
                        data = dict(studentDescription = 'I am a CS major interested in cybersecurity', reference_name = 'Andy Fallon', reference_email = 'andyfallon@wsu.edu' ),
                        follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Research Connect" in response.data
    
    response = test_client.get('/logout',                       
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Sign In" in response.data


def test_student_login_logout(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' form is submitted (POST) with correct credentials
    THEN check that the response is valid and login is succesfull 
    """
    response = test_client.post('/login', 
                          data=dict(username='selina@wsu.edu', password='123',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Research Connect!" in response.data

    response = test_client.get('/logout',                       
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Sign In" in response.data

def test_invalid_credentials_login(test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' form is submitted (POST) with wrong credentials
    THEN check that the response is valid and login is refused 
    """
    response = test_client.post('/login', 
                        data=dict(username='sejal123@wsu.edu', password='123',remember_me=False),
                        follow_redirects = True)
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data


def test_apply_page(test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' form is submitted (POST) with wrong credentials
    THEN check that the response is valid and login is refused 
    """
    response = test_client.post('/login', 
                          data=dict(username='sakire@wsu.edu', password='123',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Research Connect!" in response.data

    response = test_client.get('/createpost')
    assert response.status_code == 200
    assert b"Post Research Opportunity" in response.data
    interests1 = list( map(lambda t: t.id, Interest.query.all()[:3]))  
    response = test_client.post('/createpost', 
                          data=dict(title='My application test post', description='This is my second test post.',qualifications="testing qual",
                          start_date="test1", end_date = "test2", commitment = 1, interest = interests1 ),
                          follow_redirects = True)
    c = db.session.query(Post).filter(Post.title =='My application test post')
    assert c.first().get_interests().count() == 3 #should have 3 tags
    assert c.count() == 1          
    print(response.data)
    assert response.status_code == 200
    assert b"Welcome to Research Connect!" in response.data
    assert b"My application test post" in response.data 
    assert b"This is my second test post." in response.data


    response = test_client.get('/logout',                       
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Sign In" in response.data

    response = test_client.post('/login', 
                          data=dict(username='selina@wsu.edu', password='123',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Research Connect!" in response.data

    
    p = db.session.query(Post).filter(Post.title =='My application test post')
    assert c.first().get_interests().count() == 3 #should have 3 tags
    assert c.count() == 1 
    response = test_client.get('/apply/'+str(p.first().id),                       
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Apply to Research Opportunity" in response.data

    response = test_client.get('/logout',                       
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Sign In" in response.data


def test_delete(test_client, init_database):

    response = test_client.post('/login', 
                          data=dict(username='sakire@wsu.edu', password='123',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Research Connect!" in response.data

    response = test_client.get('/createpost')
    assert response.status_code == 200
    assert b"Post Research Opportunity" in response.data
    interests1 = list( map(lambda t: t.id, Interest.query.all()[:3]))  
    response = test_client.post('/createpost', 
                          data=dict(title='My fifth application test post', description='This is my fifth test post.',qualifications="testing qual",
                          start_date="test1", end_date = "test2", commitment = 1, interest = interests1 ),
                          follow_redirects = True)
    c = db.session.query(Post).filter(Post.title =='My fifth application test post')
    assert c.first().get_interests().count() == 3 #should have 3 tags
    assert c.count() == 1          
    assert response.status_code == 200
    assert b"Welcome to Research Connect!" in response.data
    assert b"My fifth application test post" in response.data 
    assert b"This is my fifth test post." in response.data

    c = db.session.query(Post).filter(Post.title =='My fifth application test post')
    assert c.first().get_interests().count() == 3 #should have 3 tags
    assert c.count() == 1          
    assert response.status_code == 200
    assert b"Welcome to Research Connect!" in response.data
    assert b"My fifth application test post" in response.data 
    assert b"This is my fifth test post." in response.data


    response = test_client.delete('/delete/'+str(c.first().id), follow_redirects = True)
    assert response.status_code == 200                

    m =  c = db.session.query(Post).filter(Post.title =='My fifth application test post')
    assert m.count() == 0
    response = test_client.get('/logout',                       
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Sign In" in response.data



















