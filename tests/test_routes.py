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

def test_faculty_register(test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    #uname = "sakire@wsu.edu",uphn = "1234", ufirstname = "Sakire",ulastname = "Arslan Ay",uwsuid = "7891012", passwd="123"
    # Create a test client using the Flask application configured for testing
    response = test_client.post('/faculty_registration', 
                          data=dict(username = "sakire@wsu.edu", firstname = "Sakire", lastname = "Arslan Ay", phone_num = "1234", wsu_id = "7891012", user_type = "Faculty" ),
                          follow_redirects = True)
    assert response.status_code == 200

    s = db.session.query(Faculty).filter(Faculty.username=='sakire@wsu.edu')
    assert s.first().username == 'sakire@wsu.edu'
    assert s.count() == 1
    assert b"Submit" in response.data  

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


# def test_post(test_client,init_database):
#     """
#     GIVEN a Flask application configured for testing , after user logs in,
#     WHEN the '/postsmile' page is requested (GET)  AND /PostForm' form is submitted (POST)
#     THEN check that response is valid and the class is successfully created in the database
#     """
#     #login
#     response = test_client.post('/login', 
#                         data=dict(username='sakire@wsu.edu', password='123',remember_me=False),
#                         follow_redirects = True)
#     assert response.status_code == 200
#     assert b"Welcome to Research Connect!" in response.data
    
#     #test the "PostSmile" form 
#     response = test_client.get('/createpost')
#     assert response.status_code == 200
#     assert b"Submit" in response.data
#     assert b"Post Research Opportunity" in response.data
    
#     #test posting a smile story
#     tags1 = list( map(lambda t: t.id, Interest.query.all()[:12]))  # should only pass 'id's of the tags. See https://stackoverflow.com/questions/62157168/how-to-send-queryselectfield-form-data-to-a-flask-view-in-a-unittest
#     print("TESTING********************: ", tags1)
#     response = test_client.post('/createpost', 
#                           data=dict(title='My test post', description='This is my first test post.',qualifications="testing qual",start_date="test1", end_date = "test2", commitment = 1 ),
#                           follow_redirects = True)
#     #print(response.data)
#     assert response.status_code == 200
#     assert b"Create Post - Research Connect" in response.data
#     assert b"My test post" in response.data 
#     assert b"This is my first test post." in response.data 

#     c = db.session.query(Post).filter(Post.title =='My test post')
#     # assert c.first().get_interests().count() == 12 #should have 3 tags
#     assert c.count() >= 1 #There should be at least one post with body "Here is another post."


    # tags2 = list( map(lambda t: t.id, Tag.query.all()[1:3]))  # should only pass 'id's of the tags. See https://stackoverflow.com/questions/62157168/how-to-send-queryselectfield-form-data-to-a-flask-view-in-a-unittest
    # print("TESTING********************: ", tags2)
    # response = test_client.post('/postsmile', 
    #                       data=dict(title='Second post', body='Here is another post.',happiness_level=1, tag = tags2),
    #                       follow_redirects = True)
    # assert response.status_code == 200
    # assert b"Welcome to Smile Portal!" in response.data
    # assert b"Second post" in response.data 
    # assert b"Here is another post." in response.data 

    # c = db.session.query(Post).filter(Post.body =='Here is another post.')
    # assert c.first().get_tags().count() == 2  # Should have 2 tags
    # assert c.count() >= 1 #There should be at least one post with body "Here is another post."

    # assert db.session.query(Post).count() == 2

    # #finally logout
    # response = test_client.get('/logout',                       
    #                       follow_redirects = True)
    # assert response.status_code == 200
    # assert b"Sign In" in response.data
    # assert b"Please log in to access this page." in response.data   
    


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
    assert b"Click to Register" in response.data   
    assert b"Please log in to access this page." in response.data


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
    interests1 = list( map(lambda t: t.id, Interest.query.all()[:3]))
    for i in interests1:
        print(i)
  # tags1 = list( map(lambda t: t.id, Tag.query.all()[:3]))  # should only pass 'id's of the tags. See https://stackoverflow.com/questions/62157168/how-to-send-queryselectfield-form-data-to-a-flask-view-in-a-unittest
  
    response = test_client.post('/createpost', 
                          data=dict(title='My test post', description='This is my first test post.',qualifications="testing qual",
                          start_date="test1", end_date = "test2", commitment = 1, interest = interests1 ),
                          follow_redirects = True)
    c = db.session.query(Post).filter(Post.title =='My test post')
    assert c.first().get_interests().count() == 3 #should have 3 tags
    assert c.count() == 1          
    print(response.data)
    assert response.status_code == 200

    assert b"Welcome to Research Connect!" in response.data

    assert b"My test post" in response.data 
    assert b"This is my first test post." in response.data







