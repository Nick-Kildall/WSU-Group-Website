from typing import NewType
import warnings

warnings.filterwarnings("ignore")
import os
basedir = os.path.abspath(os.path.dirname(__file__))

from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.Model.models import Faculty, Student, Post, User, Application, Apply, Interest
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ROOT_PATH = '..//' + basedir
    
class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        newStudent = Student(username = "ted4ever@wsu.edu", 
            phone_num = "3402045009", firstname = "Ted",
            lastname = "Evergreen", wsu_id = "1990464",
            major = "CS", gpa = "3.94",
            grad_date = "01/01/22", tech_electives = "Robotics club",
            languages = "Python, HTML, CSS, Ruby", prior_exp = "None", user_type="Student")
        newStudent.set_password('covid')
        self.assertFalse(newStudent.get_password('flu'))
        self.assertTrue(newStudent.get_password('covid'))
    
    ### Checking if posts initializes correectly
    def test_post_1(self):
        f1 = Faculty(username = "emily4ever@wsu.edu", 
            phone_num = "3402045068", firstname = "Emily",
            lastname = "Evergreen", wsu_id = "1990439",
            user_type="Faculty")
        db.session.add(f1)
        db.session.commit()
        self.assertEqual(f1.get_user_posts().all(), [])
        newPost = Post(title = "Summer Internship", startDate = "June 2022", 
            endDate = "August 2022", description = "Data Science",
            qualifications = "Prior internship experience",
            commitment = 40, faculty_id = f1.id)
        db.session.add(newPost)
        db.session.commit()
        self.assertEqual(f1.get_user_posts().count(), 1)
        self.assertEqual(f1.get_user_posts().first().title, 'Summer Internship')
        self.assertEqual(f1.get_user_posts().first().startDate, 'June 2022')
        self.assertEqual(f1.get_user_posts().first().endDate, 'August 2022')
        self.assertEqual(f1.get_user_posts().first().description, 'Data Science')
        self.assertEqual(f1.get_user_posts().first().qualifications, 'Prior internship experience')
        self.assertEqual(f1.get_user_posts().first().commitment, 40)

    ### Checking if posts initializes correectly with multiple users
    def test_post_2(self):
        f1 = Faculty(username = "emily4ever@wsu.edu", 
            phone_num = "3402045068", firstname = "Emily",
            lastname = "Evergreen", wsu_id = "1990439",
            user_type="Faculty")
        f2 = Faculty(username = "greg4ever@wsu.edu", 
            phone_num = "3402045078", firstname = "Greg",
            lastname = "Evergreen", wsu_id = "1990424",
            user_type="Faculty")
        db.session.add(f1)
        db.session.add(f2)
        db.session.commit()
        self.assertEqual(f1.get_user_posts().all(), [])
        self.assertEqual(f2.get_user_posts().all(), [])
        
        ### Two posts by first faculty user
        p1 = Post(title = "Summer Internship", startDate = "June 2022", 
            endDate = "August 2022", description = "Data Science",
            qualifications = "Prior internship experience",
            commitment = 40, faculty_id = f1.id)
        p2 = Post(title = "Fall Internship", startDate = "January 2022", 
            endDate = "March 2022", description = "Blockchain Developement",
            qualifications = "None required",
            commitment = 20, faculty_id = f1.id)
        ### One post by second faculty user
        p3 = Post(title = "Autumn Internship", startDate = "February 2022", 
            endDate = "May 2022", description = "Java Developement",
            qualifications = "Extensive Java portfolio",
            commitment = 40, faculty_id = f2.id)
        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.commit()

        self.assertEqual(f1.get_user_posts().count(), 2)
        self.assertEqual(f1.get_user_posts().all()[1].title, 'Fall Internship')
        self.assertEqual(f1.get_user_posts().all()[1].startDate, 'January 2022')
        self.assertEqual(f1.get_user_posts().all()[1].endDate, 'March 2022')
        self.assertEqual(f1.get_user_posts().all()[1].description, 'Blockchain Developement')
        self.assertEqual(f1.get_user_posts().all()[1].qualifications, 'None required')
        self.assertEqual(f1.get_user_posts().all()[1].commitment, 20)

        self.assertEqual(f2.get_user_posts().count(), 1)
        self.assertEqual(f2.get_user_posts().all()[0].title, 'Autumn Internship')
        self.assertEqual(f2.get_user_posts().all()[0].startDate, 'February 2022')
        self.assertEqual(f2.get_user_posts().all()[0].endDate, 'May 2022')
        self.assertEqual(f2.get_user_posts().all()[0].description, 'Java Developement')
        self.assertEqual(f2.get_user_posts().all()[0].qualifications, 'Extensive Java portfolio')
        self.assertEqual(f2.get_user_posts().all()[0].commitment, 40)

    ### Testing apply and withdraw functionalitiy
    def test_application(self):
        f1 = Faculty(username = "emily4ever@wsu.edu", 
            phone_num = "3402045068", firstname = "Emily",
            lastname = "Evergreen", wsu_id = "1990439",
            user_type="Faculty")
        s1 = Student(username = "ted4ever@wsu.edu", 
            phone_num = "3402045009", firstname = "Ted",
            lastname = "Evergreen", wsu_id = "1990464",
            major = "CS", gpa = "3.94",
            grad_date = "01/01/22", tech_electives = "Robotics club",
            languages = "Python, HTML, CSS, Ruby", prior_exp = "None", user_type="Student")
        db.session.add(f1)
        db.session.add(s1)
        db.session.commit()
        self.assertEqual(f1.get_user_posts().all(), [])
        p1 = Post(title = "Summer Internship", startDate = "June 2022", 
            endDate = "August 2022", description = "Data Science",
            qualifications = "Prior internship experience",
            commitment = 40, faculty_id = f1.id)
        db.session.add(p1)
        db.session.commit()
        self.assertEqual(f1.get_user_posts().count(), 1)
        self.assertEqual(f1.get_user_posts().first().title, 'Summer Internship')
        self.assertEqual(f1.get_user_posts().first().startDate, 'June 2022')
        self.assertEqual(f1.get_user_posts().first().endDate, 'August 2022')
        self.assertEqual(f1.get_user_posts().first().description, 'Data Science')
        self.assertEqual(f1.get_user_posts().first().qualifications, 'Prior internship experience')
        self.assertEqual(f1.get_user_posts().first().commitment, 40)

        ### apply to post
        s1.apply(p1)
        db.session.commit()

        a1 = Application(student_id = s1.id, post_id = p1.id,
            studentDescription = "Interested in Tech", reference_name = "Greg Evergreen",
            reference_email = "grege@wsu.edu", title = "Summer Internship", startDate = "June 2022", 
            endDate = "August 2022", description = "Data Science",
            qualifications = "Prior internship experience", commitment = 40, username = "ted4ever@wsu.edu", 
            firstname = "Ted", lastname = "Evergreen", 
            gpa = "3.94", tech_electives = "Robotics club",
            languages = "Python, HTML, CSS, Ruby", prior_exp = "None",
            interests = "Blockchain, Data Science", status = "Applied")
    
        db.session.add(a1)
        db.session.commit()

        self.assertEqual(s1.is_applied(p1), True)

        ### withdraw from post
        s1.withdraw(p1)
        db.session.commit()

        self.assertEqual(s1.is_applied(p1), False)

    
    def test_interests(self):
        f1 = Faculty(username = "emily4ever@wsu.edu", 
            phone_num = "3402045068", firstname = "Emily",
            lastname = "Evergreen", wsu_id = "1990439",
            user_type="Faculty")
        db.session.add(f1)
        db.session.commit()
        self.assertEqual(f1.get_user_posts().all(), [])

        ### Post Interests
        p1 = Post(title = "Summer Internship", startDate = "June 2022", 
            endDate = "August 2022", description = "Data Science",
            qualifications = "Prior internship experience",
            commitment = 40, faculty_id = f1.id)

        i1 = Interest(name = "AI")
        p1.interests.append(i1)

        i2 = Interest(name = "Blockchain")
        p1.interests.append(i2)

        db.session.add(p1)
        db.session.commit()

        self.assertEqual(p1.get_interests()[0].name, "AI")
        self.assertEqual(p1.get_interests()[1].name, "Blockchain")

        ### Student Interests
        s1 = Student(username = "ted4ever@wsu.edu", 
            phone_num = "3402045009", firstname = "Ted",
            lastname = "Evergreen", wsu_id = "1990464",
            major = "CS", gpa = "3.94",
            grad_date = "01/01/22", tech_electives = "Robotics club",
            languages = "Python, HTML, CSS, Ruby", prior_exp = "None", user_type="Student")

        db.session.add(s1)
        db.session.commit()

        i1 = Interest(name = "AI")
        s1.interests.append(i1)

        db.session.add(s1)
        db.session.commit()

        self.assertEqual(s1.interests[0].name, "AI")



        
        

