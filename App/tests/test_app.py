import os, tempfile, pytest, logging, unittest, time
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Student, Staff, Review, Comment, Reply, Karma
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_username,
    update_email,
    update_faculty,
    update_name,
    update_password,
    
    create_student,
    get_karma,
    get_student_by_id,
    get_student_by_UniId,
    get_student_by_username,
    get_students_by_degree,
    get_students_by_faculty,
    get_all_students_json,
    update_admittedTerm,
    update_yearofStudy,
    update_degree,
    create_karma,

    create_staff,
    get_staff_by_id,
    get_staff_by_username,
    staff_create_review,
    staff_edit_review,
    #create_student,
    #get_student_by_username,

    get_review, get_reviews,


    #create_student,
    #create_staff,
    #get_staff_by_username,
    #get_staff_by_id,
    #get_student_by_id,
    #get_student_by_username,
    create_review,
    delete_review_work,
    edit_review_work,
    #get_review

    create_comment, edit_comment, delete_comment, get_all_comments, get_comment, get_comment_staff, get_all_comments_review,

    create_reply, edit_reply, delete_reply, get_reply, get_all_replies, get_all_replies_staff, get_all_replies_comment, get_parent_reply,

    get_root_parent_reply,

    get_karma, create_karma, like, dislike, get_karma_history

)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User(username="bob", firstname="Bob", lastname="Smith", password="bobpass", email="bob@example.com", faculty="FST")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User(username="bob", firstname="Bob", lastname="Smith", password="bobpass", email="bob@example.com", faculty="FST")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob", "firstname":"Bob", "lastname":"Smith", "email":"bob@example.com", "faculty":"FST"})

    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User(username="bob", firstname="Bob", lastname="Smith", password=password, email="bob@example.com", faculty="FST")
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User(username="bob", firstname="Bob", lastname="Smith", password=password, email="bob@example.com", faculty="FST")
        assert user.check_password(password)


class StudentUnitTests(unittest.TestCase):

    def test_new_student(self):
        student = Student(username="billy", firstname="Billy", lastname="John", email="billy@example.com", password="billypass", faculty="FST", admittedTerm="2022/2023", UniId="816000000", degree="BSc Computer Science", gpa="3.5")
        assert student.username == "billy"



class StaffUnitTests(unittest.TestCase):

    def test_new_staff(self):
        staff = Staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass", faculty="FST")
        assert staff.username == "joe"

    def test_get_json(self):
        staff = Staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass", faculty="FST")
        staff_json = staff.to_json()
        print(staff_json)
        self.assertDictEqual(staff_json, {"staffID": None,
            "username": "joe",
            "firstname": "Joe",
            "lastname": "Mama",
            "email": "joe@example.com",
            "faculty": "FST",
            "reviews": [],
            "reports": [],
            "pendingAccomplishments": []})


class ReviewUnitTests(unittest.TestCase):

    def test_new_review(self):
        assert create_staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass", faculty="FST") == True
        assert create_student(username="billy",
                 firstname="Billy",
                 lastname="John",
                 email="billy@example.com",
                 password="billypass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816031160',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("billy")
        staff = get_staff_by_username("joe")
        review = Review(staff, student, 3, "Billy is good.")
        assert review is not None


class CommentUnitTests(unittest.TestCase):

    def test_new_comment(self):
        comment = Comment(reviewID=1, staffID=1, details="Best review I've read for this student!")
        assert comment.createdByStaffID == 1

        assert comment is not None



class ReplyUnitTests(unittest.TestCase):

    def test_new_reply(self):
        reply = Reply(commentID=1, staffID=10, details="Best review I've read for this student!")
        assert reply.createdByStaffID == 10

        assert reply is not None


class KarmaUnitTests(unittest.TestCase):

    def test_new_karma(self):
        karma = Karma(points=100, studentID=1, reviewID=1)
        assert karma.points == 100
        assert karma is not None



'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "Bob", "Smith", "bobpass", "bob@example.com", "FST")
    assert login("bob", "bobpass") != None

class UserIntegrationTests(unittest.TestCase):

    
    def test_create_user(self):
        user = create_user("rick", "Rick", "Grimes", "rickpass", "rick@example.com", "FST")
        assert user.username == "rick"


    
    def test_update_user(self):
        update_username(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"

    def test_update_name(self):
        update_name(1, "Bobby", "Jones")
        user = get_user(1)
        assert user.firstname == "Bobby"
        assert user.lastname == "Jones"

    def test_update_email(self):
        update_email(1, "newemail@example.com")
        user = get_user(1)
        assert user.email == "newemail@example.com"

    def test_update_password(self):
        update_password(1, "newpass")
        user = get_user(1)
        assert user.check_password("newpass")

    def test_update_faculty(self):
        update_faculty(1, "New Faculty")
        user = get_user(1)
        assert user.faculty == "New Faculty"



        

class StudentIntegrationTests(unittest.TestCase):

    def test_create_student(self):
        assert create_student(username="billy", firstname="Billy", lastname="John", email="billy@example.com", password="billypass", faculty="FST", admittedTerm="2022/2023", UniId="816000000", degree="BSc Computer Science", gpa="3.5") == True
        
    
    
    def test_get_student_by_name(self):
        create_student(username="Jae", firstname="Jae", lastname="Son", email="jae@example.com", password="jaepass", faculty="FST", admittedTerm="2022/2023", UniId="816000002", degree="BSc Computer Science", gpa="2.7")
        student = get_student_by_username("Jae")
        assert student.username == "Jae"

    def test_get_studens_by_degree(self):
        create_student(username="Jae", firstname="Jae", lastname="Son", email="jae@example.com", password="jaepass", faculty="FST", admittedTerm="2022/2023", UniId="816000002", degree="BSc Computer Science (Special)", gpa="2.7")
        students = get_students_by_degree("BSc Computer Science (Special)")

        expected_student = {
                "username":"Jae", 
                "firstname":"Jae", 
                "lastname":"Son", 
                "email":"jae@example.com", 
                "faculty":"FST", 
                "admittedTerm":"2022/2023", 
                "UniId":"816000002", 
                "degree":"BSc Computer Science (Special)", 
                "gpa":"2.7"
        }
        self.assertEqual(students[0].username, expected_student["username"])
        self.assertEqual(students[0].firstname, expected_student["firstname"])
        self.assertEqual(students[0].lastname, expected_student["lastname"])
        self.assertEqual(students[0].email, expected_student["email"])
        self.assertEqual(students[0].faculty, expected_student["faculty"])
        self.assertEqual(students[0].admittedTerm, expected_student["admittedTerm"])
        self.assertEqual(students[0].UniId, expected_student["UniId"])
        self.assertEqual(students[0].degree, expected_student["degree"])
        self.assertEqual(students[0].gpa, expected_student["gpa"])

    def test_get_students_by_faulty(self):
        create_student(username="Ryan", firstname="Ryan", lastname="Aire", email="ryan@example.com", password="ryanpass", faculty="FSS", admittedTerm="2022/2023", UniId="816000005", degree="Psychology", gpa="3.7")
        students = get_students_by_faculty("FSS")
        
        expected_student = {
                "username":"Ryan", 
                "firstname":"Ryan", 
                "lastname":"Aire", 
                "email":"ryan@example.com", 
                "faculty":"FSS", 
                "admittedTerm":"2022/2023", 
                "UniId":"816000005", 
                "degree":"Psychology", 
                "gpa":"3.7"
        }
        self.assertEqual(students[0].username, expected_student["username"])
        self.assertEqual(students[0].firstname, expected_student["firstname"])
        self.assertEqual(students[0].lastname, expected_student["lastname"])
        self.assertEqual(students[0].email, expected_student["email"])
        self.assertEqual(students[0].faculty, expected_student["faculty"])
        self.assertEqual(students[0].admittedTerm, expected_student["admittedTerm"])
        self.assertEqual(students[0].UniId, expected_student["UniId"])
        self.assertEqual(students[0].degree, expected_student["degree"])
        self.assertEqual(students[0].gpa, expected_student["gpa"])
    
    def test_get_students_json(self):
        students = get_all_students_json()
        assert students != []

   
    
    def test_get_student_by_UniId(self):
      student = get_student_by_UniId("816000000")
      assert student is not None
    
    


class StaffIntegrationTests(unittest.TestCase):

    def test_create_staff(self):
        assert create_staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass", faculty="FST") == True



    def test_get_staff_by_name(self):
        staff = get_staff_by_username("joe")
        assert staff.username == "joe"



class ReviewIntegrationTests(unittest.TestCase):

    def test_create_review(self):
        assert create_staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass", faculty="FST") == True
        assert create_student(username="billy",
                 firstname="Billy",
                 lastname="John",
                 email="billy@example.com",
                 password="billypass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816031161',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("billy")
        staff = get_staff_by_username("joe")
        review1 = create_review(staff=staff, student=student, starRating=3, details="Billy is Amazing.")

        review = get_review(review1.ID)

        expected_review = {
                "createdByStaffID":staff.ID, 
                "studentID":student.ID,
                "starRating":3, 
                "details":"Billy is Amazing."
        }

        self.assertEqual(review.createdByStaffID, expected_review["createdByStaffID"])
        self.assertEqual(review.studentID, expected_review["studentID"])
        self.assertEqual(review.starRating, expected_review["starRating"])
        self.assertEqual(review.details, expected_review["details"])


    def test_get_review(self):
        assert create_staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass", faculty="FST") == True
        assert create_student(username="billy",
                firstname="Billy",
                lastname="John",
                email="billy@example.com",
                password="billypass",
                faculty="FST",
                admittedTerm="",
                UniId='816031521',
                degree="",
                gpa="") == True
        student = get_student_by_username("billy")
        staff = get_staff_by_username("joe")
        review1 = create_review(staff=staff, student=student, starRating=3, details="Billy is Amazing.")

        review = get_review(review1.ID)
        review = get_review(2)
        #print(review.to_json(student=get_student_by_id(review.studentID), staff=get_staff_by_id(review.createdByStaffID)))
        assert review is not None

    

    def test_delete_review(self):
        

        assert create_staff(username="Mark",firstname="Mark", lastname="Grayson", email="mark@example.com", password="markpass", faculty="FST") == True
        assert create_student(username="Nolan",
                 firstname="Nolan",
                 lastname="Grayson",
                 email="nolan@example.com",
                 password="nolanpass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816031166',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("Nolan")
        staff = get_staff_by_username("Mark")
        review1 = create_review(staff=staff, student=student, starRating=5, details="THINK MARK, THINK!")

        review = get_review(review1.ID)

        expected_review = {
                "createdByStaffID":staff.ID, 
                "studentID":student.ID,
                "starRating":5, 
                "details":"THINK MARK, THINK!"
        }

        self.assertEqual(review.createdByStaffID, expected_review["createdByStaffID"])
        self.assertEqual(review.studentID, expected_review["studentID"])
        self.assertEqual(review.starRating, expected_review["starRating"])
        self.assertEqual(review.details, expected_review["details"])

        assert review is not None

        delete_review_work(review.ID, staff.ID)

        deleted_review = get_review(review.ID)
        assert deleted_review is None

    
    def test_delete_review2(self):
        # self.test_create_review()

        assert create_staff(username="Mark",firstname="Mark", lastname="Grayson", email="mark@example.com", password="markpass", faculty="FST") == True
        assert create_student(username="Nolan",
                 firstname="Nolan",
                 lastname="Grayson",
                 email="nolan@example.com",
                 password="nolanpass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816031198',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("Nolan")
        staff = get_staff_by_username("Mark")
        review1 = create_review(staff=staff, student=student, starRating=5, details="THINK MARK, THINK!")

        review = get_review(review1.ID)

        expected_review = {
                "createdByStaffID":staff.ID, 
                "studentID":student.ID,
                "starRating":5, 
                "details":"THINK MARK, THINK!"
        }

        self.assertEqual(review.createdByStaffID, expected_review["createdByStaffID"])
        self.assertEqual(review.studentID, expected_review["studentID"])
        self.assertEqual(review.starRating, expected_review["starRating"])
        self.assertEqual(review.details, expected_review["details"])

        assert review is not None

        wrong_id = staff.ID + 1

        delete_review_work(review.ID, wrong_id)

        deleted_review = get_review(review.ID)
        assert deleted_review is not None



    def test_edit_review(self):
        # self.test_create_review()

        assert create_staff(username="Mark",firstname="Mark", lastname="Grayson", email="mark@example.com", password="markpass", faculty="FST") == True
        assert create_student(username="Nolan",
                 firstname="Nolan",
                 lastname="Grayson",
                 email="nolan@example.com",
                 password="nolanpass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816035566',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("Nolan")
        staff = get_staff_by_username("Mark")
        review1 = create_review(staff=staff, student=student, starRating=5, details="THINK MARK, THINK!")

        review = get_review(review1.ID)

        expected_review = {
                "createdByStaffID":staff.ID, 
                "studentID":student.ID,
                "starRating":5, 
                "details":"THINK MARK, THINK!"
        }

        self.assertEqual(review.createdByStaffID, expected_review["createdByStaffID"])
        self.assertEqual(review.studentID, expected_review["studentID"])
        self.assertEqual(review.starRating, expected_review["starRating"])
        self.assertEqual(review.details, expected_review["details"])

        assert review is not None

        new_details = "Stand Ready for my arrival Worm!"
        new_starRating = 1

        edit_review_work(new_details, review.ID, staff.ID, new_starRating)

        edited_review = get_review(review.ID)


        expected_review_2 = {
                "createdByStaffID":staff.ID, 
                "studentID":student.ID,
                "starRating":1, 
                "details":"Stand Ready for my arrival Worm!"
        }

        self.assertEqual(edited_review.createdByStaffID, expected_review_2["createdByStaffID"])
        self.assertEqual(edited_review.studentID, expected_review_2["studentID"])
        self.assertEqual(edited_review.starRating, expected_review_2["starRating"])
        self.assertEqual(edited_review.details, expected_review_2["details"])

    
    def test_edit_review2(self):
        # self.test_create_review()

        assert create_staff(username="Mark",firstname="Mark", lastname="Grayson", email="mark@example.com", password="markpass", faculty="FST") == True
        assert create_student(username="Nolan",
                 firstname="Nolan",
                 lastname="Grayson",
                 email="nolan@example.com",
                 password="nolanpass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816031096',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("Nolan")
        staff = get_staff_by_username("Mark")
        review1 = create_review(staff=staff, student=student, starRating=5, details="THINK MARK, THINK!")

        review = get_review(review1.ID)

        expected_review = {
                "createdByStaffID":staff.ID, 
                "studentID":student.ID,
                "starRating":5, 
                "details":"THINK MARK, THINK!"
        }

        self.assertEqual(review.createdByStaffID, expected_review["createdByStaffID"])
        self.assertEqual(review.studentID, expected_review["studentID"])
        self.assertEqual(review.starRating, expected_review["starRating"])
        self.assertEqual(review.details, expected_review["details"])

        assert review is not None

        new_details = "Stand Ready for my arrival Worm!"
        new_starRating = 1

        wrong_id = staff.ID + 1

        test_edit_review_status = edit_review_work(new_details, review.ID, wrong_id, new_starRating)

        assert test_edit_review_status is None


class CommentIntegrationTests(unittest.TestCase):

    def test_create_comment(self):
        
        assert create_staff(username="Mark",firstname="Mark", lastname="Grayson", email="mark@example.com", password="markpass", faculty="FST") == True
        assert create_student(username="Nolan",
                 firstname="Nolan",
                 lastname="Grayson",
                 email="nolan@example.com",
                 password="nolanpass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816033566',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("Nolan")
        staff = get_staff_by_username("Mark")
        review1 = create_review(staff=staff, student=student, starRating=5, details="THINK MARK, THINK!")

        review = get_review(review1.ID)

        expected_review = {
                "createdByStaffID":staff.ID, 
                "studentID":student.ID,
                "starRating":5, 
                "details":"THINK MARK, THINK!"
        }

        self.assertEqual(review.createdByStaffID, expected_review["createdByStaffID"])
        self.assertEqual(review.studentID, expected_review["studentID"])
        self.assertEqual(review.starRating, expected_review["starRating"])
        self.assertEqual(review.details, expected_review["details"])

        assert review is not None

        new_comment = create_comment(reviewID=review.ID, staffID=staff.ID, details="This is a fantastic Review!")

        assert new_comment is not None

        expected_comment = {
                "createdByStaffID":staff.ID, 
                "reviewID":review.ID,
                "details":"This is a fantastic Review!"
        }

        self.assertEqual(new_comment.createdByStaffID, expected_comment["createdByStaffID"])
        self.assertEqual(new_comment.reviewID, expected_comment["reviewID"])
        self.assertEqual(new_comment.details, expected_comment["details"])

        review_comment = get_review(review.ID)

        assert review_comment is not None

        assert len(review_comment.comments) == 1

        assert review_comment.comments[0].details == "This is a fantastic Review!"


    def test_get_comment(self):
        assert create_staff(username="Mark",firstname="Mark", lastname="Grayson", email="mark@example.com", password="markpass", faculty="FST") == True
        assert create_student(username="Nolan",
                 firstname="Nolan",
                 lastname="Grayson",
                 email="nolan@example.com",
                 password="nolanpass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816031117',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("Nolan")
        staff = get_staff_by_username("Mark")
        review1 = create_review(staff=staff, student=student, starRating=5, details="THINK MARK, THINK!")

        review = get_review(review1.ID)

        expected_review = {
                "createdByStaffID":staff.ID, 
                "studentID":student.ID,
                "starRating":5, 
                "details":"THINK MARK, THINK!"
        }

        self.assertEqual(review.createdByStaffID, expected_review["createdByStaffID"])
        self.assertEqual(review.studentID, expected_review["studentID"])
        self.assertEqual(review.starRating, expected_review["starRating"])
        self.assertEqual(review.details, expected_review["details"])

        assert review is not None

        new_comment = create_comment(reviewID=review.ID, staffID=staff.ID, details="This review sucks")

        assert new_comment is not None

        expected_comment = {
                "createdByStaffID":staff.ID, 
                "reviewID":review.ID,
                "details":"This review sucks"
        }

        self.assertEqual(new_comment.createdByStaffID, expected_comment["createdByStaffID"])
        self.assertEqual(new_comment.reviewID, expected_comment["reviewID"])
        self.assertEqual(new_comment.details, expected_comment["details"])

        review_comment = get_review(review.ID)

        assert review_comment is not None

        assert len(review_comment.comments) == 1

        assert review_comment.comments[0].details == "This review sucks"


        comment = get_comment(new_comment.ID)

        assert comment is not None

        assert comment.details == "This review sucks"
    
    def test_get_all_comments_review(self):
        
        assert create_staff(username="Mark",firstname="Mark", lastname="Grayson", email="mark@example.com", password="markpass", faculty="FST") == True
        assert create_student(username="Nolan",
                 firstname="Nolan",
                 lastname="Grayson",
                 email="nolan@example.com",
                 password="nolanpass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816031857',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("Nolan")
        staff = get_staff_by_username("Mark")
        review1 = create_review(staff=staff, student=student, starRating=5, details="THINK MARK, THINK!")

        review = get_review(review1.ID)

        new_comment1 = create_comment(reviewID=review.ID, staffID=staff.ID, details="This is my 1st comment")
        new_comment2 = create_comment(reviewID=review.ID, staffID=staff.ID, details="This is my 2nd comment")
        new_comment3 = create_comment(reviewID=review.ID, staffID=staff.ID, details="This is my 3rd comment")

        comments = get_all_comments_review(review.ID)

        assert len(comments) == 3


    def test_get_all_comments_staff(self):
        
        assert create_staff(username="Debbie",firstname="Debbie", lastname="Grayson", email="debbie@example.com", password="debbiepass", faculty="FST") == True
        assert create_student(username="Nolan",
                 firstname="Nolan",
                 lastname="Grayson",
                 email="nolan@example.com",
                 password="nolanpass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816039816',
                 degree="",
                 gpa="") == True

        assert create_student(username="Amber",
                 firstname="Amber",
                 lastname="Doe",
                 email="amber@example.com",
                 password="amberpass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816031170',
                 degree="",
                 gpa="") == True
        student1 = get_student_by_username("Nolan")
        student2 = get_student_by_username("Amber")
        staff = get_staff_by_username("Debbie")
        review1 = create_review(staff=staff, student=student1, starRating=5, details="THINK MARK, THINK!")
        review2 = create_review(staff=staff, student=student2, starRating=3, details="Just uninteresting")

        review = get_review(review1.ID)
        review2nd = get_review(review2.ID)

        new_comment1 = create_comment(reviewID=review.ID, staffID=staff.ID, details="This is my 1st comment, by debbie")
        new_comment2 = create_comment(reviewID=review.ID, staffID=staff.ID, details="This is my 2nd comment, by debbie")
        new_comment3 = create_comment(reviewID=review.ID, staffID=staff.ID, details="This is my 3rd comment, by debbie")
        new_comment4 = create_comment(reviewID=review2nd.ID, staffID=staff.ID, details="This is my 4th comment, by debbie")
        new_comment5 = create_comment(reviewID=review2nd.ID, staffID=staff.ID, details="This is my 5th comment, by debbie")

        comment_teacher = get_comment_staff(staff.ID)

        assert len(comment_teacher) == 5
    
        

    def test_delete_comment(self):
        
        assert create_staff(username="Mark",firstname="Mark", lastname="Grayson", email="mark@example.com", password="markpass", faculty="FST") == True
        assert create_student(username="Nolan",
                 firstname="Nolan",
                 lastname="Grayson",
                 email="nolan@example.com",
                 password="nolanpass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816531166',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("Nolan")
        staff = get_staff_by_username("Mark")
        review1 = create_review(staff=staff, student=student, starRating=5, details="THINK MARK, THINK!")

        review = get_review(review1.ID)

        expected_review = {
                "createdByStaffID":staff.ID, 
                "studentID":student.ID,
                "starRating":5, 
                "details":"THINK MARK, THINK!"
        }

        self.assertEqual(review.createdByStaffID, expected_review["createdByStaffID"])
        self.assertEqual(review.studentID, expected_review["studentID"])
        self.assertEqual(review.starRating, expected_review["starRating"])
        self.assertEqual(review.details, expected_review["details"])

        assert review is not None

        new_comment = create_comment(reviewID=review.ID, staffID=staff.ID, details="This is a fantastic Review!")

        assert new_comment is not None

        expected_comment = {
                "createdByStaffID":staff.ID, 
                "reviewID":review.ID,
                "details":"This is a fantastic Review!"
        }

        self.assertEqual(new_comment.createdByStaffID, expected_comment["createdByStaffID"])
        self.assertEqual(new_comment.reviewID, expected_comment["reviewID"])
        self.assertEqual(new_comment.details, expected_comment["details"])

        review_comment = get_review(review.ID)

        assert review_comment is not None

        assert len(review_comment.comments) == 1

        assert review_comment.comments[0].details == "This is a fantastic Review!"

        status = delete_comment(new_comment.ID, staff.ID)

        assert status is True

        test_comment = get_comment(new_comment.ID)
        assert test_comment is None


    def test_edit_comment(self):
        
        assert create_staff(username="Mark",firstname="Mark", lastname="Grayson", email="mark@example.com", password="markpass", faculty="FST") == True
        assert create_student(username="Nolan",
                 firstname="Nolan",
                 lastname="Grayson",
                 email="nolan@example.com",
                 password="nolanpass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816031112',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("Nolan")
        staff = get_staff_by_username("Mark")
        review1 = create_review(staff=staff, student=student, starRating=5, details="THINK MARK, THINK!")

        review = get_review(review1.ID)

        expected_review = {
                "createdByStaffID":staff.ID, 
                "studentID":student.ID,
                "starRating":5, 
                "details":"THINK MARK, THINK!"
        }

        self.assertEqual(review.createdByStaffID, expected_review["createdByStaffID"])
        self.assertEqual(review.studentID, expected_review["studentID"])
        self.assertEqual(review.starRating, expected_review["starRating"])
        self.assertEqual(review.details, expected_review["details"])

        assert review is not None

        new_comment = create_comment(reviewID=review.ID, staffID=staff.ID, details="This is a fantastic Review!")

        assert new_comment is not None

        expected_comment = {
                "createdByStaffID":staff.ID, 
                "reviewID":review.ID,
                "details":"This is a fantastic Review!"
        }

        self.assertEqual(new_comment.createdByStaffID, expected_comment["createdByStaffID"])
        self.assertEqual(new_comment.reviewID, expected_comment["reviewID"])
        self.assertEqual(new_comment.details, expected_comment["details"])

        review_comment = get_review(review.ID)

        assert review_comment is not None

        assert len(review_comment.comments) == 1

        assert review_comment.comments[0].details == "This is a fantastic Review!"

        new_details = "This is not longer my favourite comment!"

        status = edit_comment(new_details, new_comment.ID, staff.ID)

        expected_comment_2 = {
                "createdByStaffID":staff.ID, 
                "reviewID":review.ID,
                "details":"This is not longer my favourite comment!"
        }

        self.assertEqual(new_comment.createdByStaffID, expected_comment_2["createdByStaffID"])
        self.assertEqual(new_comment.reviewID, expected_comment_2["reviewID"])
        self.assertEqual(new_comment.details, expected_comment_2["details"])

        assert status is True

        # test_comment = get_comment(new_comment.ID)
        # assert test_comment is None



class ReplyIntegrationTests(unittest.TestCase):

    def test_create_reply(self):
        
        assert create_staff(username="Mark",firstname="Mark", lastname="Grayson", email="mark@example.com", password="markpass", faculty="FST") == True
        assert create_student(username="Nolan",
                 firstname="Nolan",
                 lastname="Grayson",
                 email="nolan@example.com",
                 password="nolanpass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816032266',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("Nolan")
        staff = get_staff_by_username("Mark")
        review1 = create_review(staff=staff, student=student, starRating=5, details="THINK MARK, THINK!")

        review = get_review(review1.ID)

        expected_review = {
                "createdByStaffID":staff.ID, 
                "studentID":student.ID,
                "starRating":5, 
                "details":"THINK MARK, THINK!"
        }

        self.assertEqual(review.createdByStaffID, expected_review["createdByStaffID"])
        self.assertEqual(review.studentID, expected_review["studentID"])
        self.assertEqual(review.starRating, expected_review["starRating"])
        self.assertEqual(review.details, expected_review["details"])

        assert review is not None

        new_comment = create_comment(reviewID=review.ID, staffID=staff.ID, details="This is a fantastic Review!")

        assert new_comment is not None

        expected_comment = {
                "createdByStaffID":staff.ID, 
                "reviewID":review.ID,
                "details":"This is a fantastic Review!"
        }

        self.assertEqual(new_comment.createdByStaffID, expected_comment["createdByStaffID"])
        self.assertEqual(new_comment.reviewID, expected_comment["reviewID"])
        self.assertEqual(new_comment.details, expected_comment["details"])

        review_comment = get_review(review.ID)

        assert review_comment is not None

        assert len(review_comment.comments) == 1

        assert review_comment.comments[0].details == "This is a fantastic Review!"



        new_reply = create_reply(commentID=new_comment.ID, staffID=staff.ID, details="My first reply!")

        assert new_reply is not None

        expected_reply = {
                "createdByStaffID":staff.ID, 
                "commentID":new_comment.ID,
                "details":"My first reply!"
        }

        self.assertEqual(new_reply.createdByStaffID, expected_reply["createdByStaffID"])
        self.assertEqual(new_reply.commentID, expected_reply["commentID"])
        self.assertEqual(new_reply.details, expected_reply["details"])

        comment_reply = get_comment(new_comment.ID)

        assert comment_reply is not None

        assert len(comment_reply.replies) == 1

        assert comment_reply.replies[0].details == "My first reply!"


    def test_get_reply(self):
        assert create_staff(username="Mark",firstname="Mark", lastname="Grayson", email="mark@example.com", password="markpass", faculty="FST") == True
        assert create_student(username="Nolan",
                 firstname="Nolan",
                 lastname="Grayson",
                 email="nolan@example.com",
                 password="nolanpass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816031122',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("Nolan")
        staff = get_staff_by_username("Mark")
        review1 = create_review(staff=staff, student=student, starRating=5, details="THINK MARK, THINK!")

        review = get_review(review1.ID)

        expected_review = {
                "createdByStaffID":staff.ID, 
                "studentID":student.ID,
                "starRating":5, 
                "details":"THINK MARK, THINK!"
        }

        self.assertEqual(review.createdByStaffID, expected_review["createdByStaffID"])
        self.assertEqual(review.studentID, expected_review["studentID"])
        self.assertEqual(review.starRating, expected_review["starRating"])
        self.assertEqual(review.details, expected_review["details"])

        assert review is not None

        new_comment = create_comment(reviewID=review.ID, staffID=staff.ID, details="This review sucks")

        assert new_comment is not None

        expected_comment = {
                "createdByStaffID":staff.ID, 
                "reviewID":review.ID,
                "details":"This review sucks"
        }

        self.assertEqual(new_comment.createdByStaffID, expected_comment["createdByStaffID"])
        self.assertEqual(new_comment.reviewID, expected_comment["reviewID"])
        self.assertEqual(new_comment.details, expected_comment["details"])

        review_comment = get_review(review.ID)

        assert review_comment is not None

        assert len(review_comment.comments) == 1

        assert review_comment.comments[0].details == "This review sucks"

        new_reply = create_reply(commentID=new_comment.ID, staffID=staff.ID, details="My first reply!")

        assert new_reply is not None

        expected_reply = {
                "createdByStaffID":staff.ID, 
                "commentID":new_comment.ID,
                "details":"My first reply!"
        }

        self.assertEqual(new_reply.createdByStaffID, expected_reply["createdByStaffID"])
        self.assertEqual(new_reply.commentID, expected_reply["commentID"])
        self.assertEqual(new_reply.details, expected_reply["details"])



        reply = get_reply(new_reply.ID)

        assert reply is not None

        assert reply.details == "My first reply!"
    
    def test_get_all_replies_comment(self):
        
        assert create_staff(username="Mark",firstname="Mark", lastname="Grayson", email="mark@example.com", password="markpass", faculty="FST") == True
        assert create_student(username="Nolan",
                 firstname="Nolan",
                 lastname="Grayson",
                 email="nolan@example.com",
                 password="nolanpass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816036536',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("Nolan")
        staff = get_staff_by_username("Mark")
        review1 = create_review(staff=staff, student=student, starRating=5, details="THINK MARK, THINK!")

        review = get_review(review1.ID)

        new_comment1 = create_comment(reviewID=review.ID, staffID=staff.ID, details="This is my 1st comment")

        comment = get_comment(new_comment1.ID)

        new_reply1 = create_reply(commentID=comment.ID, staffID=staff.ID, details="My 1st reply!")
        new_reply2 = create_reply(commentID=comment.ID, staffID=staff.ID, details="My 2nd reply!")
        new_reply3 = create_reply(commentID=comment.ID, staffID=staff.ID, details="My 3rd reply!")
        new_reply4 = create_reply(commentID=comment.ID, staffID=staff.ID, details="My 4th reply!")

        replies = get_all_replies_comment(comment.ID)

        assert len(replies) == 4


    def test_get_all_replies_staff(self):
        
        assert create_staff(username="Jin",firstname="Jin", lastname="Woo", email="jin@example.com", password="jinpass", faculty="FST") == True
        assert create_student(username="Nolan",
                 firstname="Nolan",
                 lastname="Grayson",
                 email="nolan@example.com",
                 password="nolanpass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816030000',
                 degree="",
                 gpa="") == True

        assert create_student(username="Amber",
                 firstname="Amber",
                 lastname="Doe",
                 email="amber@example.com",
                 password="amberpass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816030002',
                 degree="",
                 gpa="") == True
        student1 = get_student_by_username("Nolan")
        student2 = get_student_by_username("Amber")
        staff = get_staff_by_username("Jin")
        review1 = create_review(staff=staff, student=student1, starRating=5, details="THINK MARK, THINK!")
        review2 = create_review(staff=staff, student=student2, starRating=3, details="Just uninteresting")

        review = get_review(review1.ID)
        review2nd = get_review(review2.ID)

        new_comment1 = create_comment(reviewID=review.ID, staffID=staff.ID, details="This is my 1st comment, by Jin")
        new_comment5 = create_comment(reviewID=review2nd.ID, staffID=staff.ID, details="This is my 5th comment, by Jin")


        comment = get_comment(new_comment1.ID)
        comment2nd = get_comment(new_comment5.ID)

        new_reply1 = create_reply(commentID=comment.ID, staffID=staff.ID, details="My 1st reply!")
        new_reply2 = create_reply(commentID=comment.ID, staffID=staff.ID, details="My 2nd reply!")
        new_reply3 = create_reply(commentID=comment.ID, staffID=staff.ID, details="My 3rd reply!")
        new_reply4 = create_reply(commentID=comment.ID, staffID=staff.ID, details="My 4th reply!")
        new_reply5 = create_reply(commentID=comment2nd.ID, staffID=staff.ID, details="My 5th reply!")
        new_reply6 = create_reply(commentID=comment2nd.ID, staffID=staff.ID, details="My 6th reply!")


        reply_teacher = get_all_replies_staff(staff.ID)

        assert len(reply_teacher) == 6
    
        

    def test_delete_reply(self):
        
        assert create_staff(username="Mark",firstname="Mark", lastname="Grayson", email="mark@example.com", password="markpass", faculty="FST") == True
        assert create_student(username="Nolan",
                 firstname="Nolan",
                 lastname="Grayson",
                 email="nolan@example.com",
                 password="nolanpass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816034466',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("Nolan")
        staff = get_staff_by_username("Mark")
        review1 = create_review(staff=staff, student=student, starRating=5, details="THINK MARK, THINK!")

        review = get_review(review1.ID)

        expected_review = {
                "createdByStaffID":staff.ID, 
                "studentID":student.ID,
                "starRating":5, 
                "details":"THINK MARK, THINK!"
        }

        self.assertEqual(review.createdByStaffID, expected_review["createdByStaffID"])
        self.assertEqual(review.studentID, expected_review["studentID"])
        self.assertEqual(review.starRating, expected_review["starRating"])
        self.assertEqual(review.details, expected_review["details"])

        assert review is not None

        new_comment = create_comment(reviewID=review.ID, staffID=staff.ID, details="This is a fantastic Review!")

        assert new_comment is not None

        expected_comment = {
                "createdByStaffID":staff.ID, 
                "reviewID":review.ID,
                "details":"This is a fantastic Review!"
        }

        self.assertEqual(new_comment.createdByStaffID, expected_comment["createdByStaffID"])
        self.assertEqual(new_comment.reviewID, expected_comment["reviewID"])
        self.assertEqual(new_comment.details, expected_comment["details"])

        review_comment = get_review(review.ID)

        assert review_comment is not None

        assert len(review_comment.comments) == 1

        assert review_comment.comments[0].details == "This is a fantastic Review!"


        new_reply1 = create_reply(commentID=new_comment.ID, staffID=staff.ID, details="My 1st reply!")

        reply = get_reply(new_reply1.ID)

        assert reply is not None

        status = delete_reply(reply.ID, staff.ID)

        assert status is True

        test_reply = get_reply(reply.ID)
        assert test_reply is None


    def test_edit_reply(self):
        
        assert create_staff(username="Mark",firstname="Mark", lastname="Grayson", email="mark@example.com", password="markpass", faculty="FST") == True
        assert create_student(username="Nolan",
                 firstname="Nolan",
                 lastname="Grayson",
                 email="nolan@example.com",
                 password="nolanpass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816036534',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("Nolan")
        staff = get_staff_by_username("Mark")
        review1 = create_review(staff=staff, student=student, starRating=5, details="THINK MARK, THINK!")

        review = get_review(review1.ID)

        expected_review = {
                "createdByStaffID":staff.ID, 
                "studentID":student.ID,
                "starRating":5, 
                "details":"THINK MARK, THINK!"
        }

        self.assertEqual(review.createdByStaffID, expected_review["createdByStaffID"])
        self.assertEqual(review.studentID, expected_review["studentID"])
        self.assertEqual(review.starRating, expected_review["starRating"])
        self.assertEqual(review.details, expected_review["details"])

        assert review is not None

        new_comment = create_comment(reviewID=review.ID, staffID=staff.ID, details="This is a fantastic Review!")

        assert new_comment is not None

        expected_comment = {
                "createdByStaffID":staff.ID, 
                "reviewID":review.ID,
                "details":"This is a fantastic Review!"
        }

        self.assertEqual(new_comment.createdByStaffID, expected_comment["createdByStaffID"])
        self.assertEqual(new_comment.reviewID, expected_comment["reviewID"])
        self.assertEqual(new_comment.details, expected_comment["details"])

        review_comment = get_review(review.ID)

        assert review_comment is not None

        assert len(review_comment.comments) == 1

        assert review_comment.comments[0].details == "This is a fantastic Review!"

        new_reply1 = create_reply(commentID=new_comment.ID, staffID=staff.ID, details="My 1st reply!")

        reply = get_reply(new_reply1.ID)

        assert reply is not None

        new_details = "Actually I change my mind on this comment!"

        status = edit_reply(new_details, reply.ID, staff.ID)

        expected_reply_2 = {
                "createdByStaffID":staff.ID, 
                "commentID":new_comment.ID,
                "details":"Actually I change my mind on this comment!"
        }

        self.assertEqual(reply.createdByStaffID, expected_reply_2["createdByStaffID"])
        self.assertEqual(reply.commentID, expected_reply_2["commentID"])
        self.assertEqual(reply.details, expected_reply_2["details"])

        assert status is True

        # test_comment = get_comment(new_comment.ID)
        # assert test_comment is None

    
    def test_get_parent_reply(self):

        assert create_staff(username="Mark",firstname="Mark", lastname="Grayson", email="mark@example.com", password="markpass", faculty="FST") == True
        assert create_student(username="Nolan",
                 firstname="Nolan",
                 lastname="Grayson",
                 email="nolan@example.com",
                 password="nolanpass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816031177',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("Nolan")
        staff = get_staff_by_username("Mark")
        review1 = create_review(staff=staff, student=student, starRating=5, details="THINK MARK, THINK!")

        review = get_review(review1.ID)

        new_comment1 = create_comment(reviewID=review.ID, staffID=staff.ID, details="This is my 1st comment")

        comment = get_comment(new_comment1.ID)

        new_reply1 = create_reply(commentID=comment.ID, staffID=staff.ID, details="My 1st reply!")
        new_reply2 = create_reply(commentID=comment.ID, staffID=staff.ID, details="My 2nd reply!", parentReplyID=new_reply1.ID)


        replies = get_all_replies_comment(comment.ID)

        assert len(replies) == 2

        parent_reply = get_parent_reply(new_reply2.ID)

        assert parent_reply is not None

        assert parent_reply == new_reply1


    
    def test_get_root_parent_reply(self):

        assert create_staff(username="Mark",firstname="Mark", lastname="Grayson", email="mark@example.com", password="markpass", faculty="FST") == True
        assert create_student(username="Nolan",
                 firstname="Nolan",
                 lastname="Grayson",
                 email="nolan@example.com",
                 password="nolanpass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816031556',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("Nolan")
        staff = get_staff_by_username("Mark")
        review1 = create_review(staff=staff, student=student, starRating=5, details="THINK MARK, THINK!")

        review = get_review(review1.ID)

        new_comment1 = create_comment(reviewID=review.ID, staffID=staff.ID, details="This is my 1st comment")

        comment = get_comment(new_comment1.ID)

        new_reply1 = create_reply(commentID=comment.ID, staffID=staff.ID, details="My 1st reply!")
        new_reply2 = create_reply(commentID=comment.ID, staffID=staff.ID, details="My 2nd reply!", parentReplyID=new_reply1.ID)
        new_reply3 = create_reply(commentID=comment.ID, staffID=staff.ID, details="My 3rd reply!", parentReplyID=new_reply2.ID)
        new_reply4 = create_reply(commentID=comment.ID, staffID=staff.ID, details="My 4th reply!", parentReplyID=new_reply3.ID)

        replies = get_all_replies_comment(comment.ID)

        assert len(replies) == 4

        parent_reply = get_root_parent_reply(new_reply4.ID)

        assert parent_reply is not None


        assert parent_reply == new_reply1






class KarmaIntegrationTests(unittest.TestCase):

    def test_create_karma(self):


        assert create_student(username="tobi", firstname="Tobi", lastname="Brown", email="tobi@example.com", password="tobipass", faculty="FST", admittedTerm="2022/2023", UniId="816000792", degree="BSc Computer Science", gpa="3.5") == True
        
        assert create_staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass", faculty="FST") == True
        
        staff = get_staff_by_username("joe")

        student = get_student_by_username("tobi")

        review1 = create_review(staff=staff, student=student, starRating=5, details="Tobi is Amazing.")

        karma_status = create_karma(points=5, studentID=student.ID, reviewID=review1.ID)

        assert karma_status is True

        karma = get_karma(student.ID)

        assert karma.points == 5


    def test_get_karma(self):


        assert create_student(username="billyjoel", firstname="Billyjoel", lastname="Johnson", email="billyjoel@example.com", password="billyjoelpass", faculty="FST", admittedTerm="2022/2023", UniId="81655555", degree="BSc Computer Science", gpa="3.5") == True
        
        assert create_staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass", faculty="FST") == True
        
        staff = get_staff_by_username("joe")


        student = get_student_by_username("billyjoel")
        

        review1 = create_review(staff=staff, student=student, starRating=5, details="Billy is Amazing.")

        karma_status = create_karma(points=5, studentID=student.ID, reviewID=review1.ID)

        assert karma_status is True

        karma = get_karma(student.ID)

        assert karma.points == 5
        assert karma is not None
        assert karma.studentID == student.ID

    
    def test_like_karma(self):

        assert create_student(username="billyjoel", firstname="Billyjoel", lastname="Johnson", email="billyjoel@example.com", password="billyjoelpass", faculty="FST", admittedTerm="2022/2023", UniId="816777777", degree="BSc Computer Science", gpa="3.5") == True
        
        assert create_staff(username="naruto",firstname="Naruto", lastname="Uzumaki", email="naruto@example.com", password="narutopass", faculty="FST") == True

        staff_testing = get_staff_by_username("naruto")

        student = get_student_by_username("billyjoel")

        

        assert create_staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass", faculty="FST") == True
        assert create_student(username="billy",
                 firstname="Billy",
                 lastname="John",
                 email="billy@example.com",
                 password="billypass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816037160',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("billy")
        staff = get_staff_by_username("joe")
        review1 = create_review(staff=staff, student=student, starRating=5, details="Billy is Amazing.")

        review = get_review(review1.ID)

        expected_review = {
                "createdByStaffID":staff.ID, 
                "studentID":student.ID,
                "starRating":5, 
                "details":"Billy is Amazing."
        }

        self.assertEqual(review.createdByStaffID, expected_review["createdByStaffID"])
        self.assertEqual(review.studentID, expected_review["studentID"])
        self.assertEqual(review.starRating, expected_review["starRating"])
        self.assertEqual(review.details, expected_review["details"])

        prev_karma = get_karma(student.ID)

        time.sleep(1) # This is done because change is karma is done by checking the timestamp for any changes made to the karma model,
                        #therefore, since the test are executed simultaneously at the same time, we need a time.sleep() to ensure the change is karma is recorded.

        like_status = like(review.ID, staff_testing.ID)

        assert like_status is True


        new_karma = get_karma(student.ID)

        time.sleep(1)

        assert prev_karma.points < new_karma.points


        like_status = like(review.ID, staff_testing.ID)

        assert like_status is False


        new_karma_1 = get_karma(student.ID)

        time.sleep(1)

        assert new_karma_1.points == new_karma.points



    def test_dislike_karma(self):

        assert create_student(username="billyjoel", firstname="Billyjoel", lastname="Johnson", email="billyjoel@example.com", password="billyjoelpass", faculty="FST", admittedTerm="2022/2023", UniId="816000777", degree="BSc Computer Science", gpa="3.5") == True
        
        assert create_staff(username="naruto",firstname="Naruto", lastname="Uzumaki", email="naruto@example.com", password="narutopass", faculty="FST") == True

        staff_testing = get_staff_by_username("naruto")

        student = get_student_by_username("billyjoel")

        


        assert create_staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass", faculty="FST") == True
        assert create_student(username="billy",
                 firstname="Billy",
                 lastname="John",
                 email="billy@example.com",
                 password="billypass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816043260',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("billy")
        staff = get_staff_by_username("joe")
        review1 = create_review(staff=staff, student=student, starRating=5, details="Billy is Amazing.")

        review = get_review(review1.ID)

        expected_review = {
                "createdByStaffID":staff.ID, 
                "studentID":student.ID,
                "starRating":5, 
                "details":"Billy is Amazing."
        }

        self.assertEqual(review.createdByStaffID, expected_review["createdByStaffID"])
        self.assertEqual(review.studentID, expected_review["studentID"])
        self.assertEqual(review.starRating, expected_review["starRating"])
        self.assertEqual(review.details, expected_review["details"])

        prev_karma = get_karma(student.ID)

        time.sleep(1) # This is done because change is karma is done by checking the timestamp for any changes made to the karma model,
                        #therefore, since the test are executed simultaneously at the same time, we need a time.sleep() to ensure the change is karma is recorded.

        dislike_status = dislike(review.ID, staff_testing.ID)

        assert dislike_status is True


        new_karma = get_karma(student.ID)

        time.sleep(1)

        assert prev_karma.points > new_karma.points


        dislike_status = dislike(review.ID, staff_testing.ID)

        assert dislike_status is False


        new_karma_1 = get_karma(student.ID)

        time.sleep(1)

        assert new_karma_1.points == new_karma.points
        

    
    def test_karma_history(self):

        assert create_student(username="billyjoel", firstname="Billyjoel", lastname="Johnson", email="billyjoel@example.com", password="billyjoelpass", faculty="FST", admittedTerm="2022/2023", UniId="816036363", degree="BSc Computer Science", gpa="3.5") == True
        
        assert create_staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass", faculty="FST") == True
        
        staff = get_staff_by_username("joe")


        student = get_student_by_username("billyjoel")
        

        review1 = create_review(staff=staff, student=student, starRating=5, details="Billy is Amazing.")
        review2 = create_review(staff=staff, student=student, starRating=4, details="Billy is Amazing2.")
        review3 = create_review(staff=staff, student=student, starRating=3, details="Billy is Amazing3.")
        review4 = create_review(staff=staff, student=student, starRating=2, details="Billy is Amazing4.")

        karma_status = create_karma(points=5, studentID=student.ID, reviewID=review1.ID)
        karma_status2 = create_karma(points=5, studentID=student.ID, reviewID=review2.ID)
        karma_status3 = create_karma(points=5, studentID=student.ID, reviewID=review3.ID)
        karma_status4 = create_karma(points=5, studentID=student.ID, reviewID=review4.ID)
    

        history = get_karma_history(student.ID)

        assert history is not None
    

      #assert parent_reply == new_reply1  

