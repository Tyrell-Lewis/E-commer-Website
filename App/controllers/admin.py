from App.models import Admin
from App.database import db 
from App.controllers import (
    create_staff,
    create_student,
    update_admittedTerm,
    update_degree,
    update_email,
    update_name,
    update_username,
    update_yearofStudy,
    update_faculty,
    update_password
)


def create_admin(username,firstname, lastname, email, password, faculty):
  newAdmin = Admin(username,firstname, lastname, email, password, faculty)
  db.session.add(newAdmin)
  try:
    db.session.commit()
    return True
    # can return if we need
    # return newStaff
  except Exception as e:
    print("[admin.create_admin] Error occurred while creating new admin: ", str(e))
    db.session.rollback()
    return False
    
def add_teacher(username,firstname, lastname, email, password, faculty):
    if create_staff(username,firstname, lastname, email, password, faculty):
        return True
    else:
        print("[admin.add_teacher] Error occurred while creating new staff: ")
        return False

def add_student(username, firstname, lastname, email, password, faculty, admittedTerm, yearofStudy, degree, gpa):
    if create_student(username, firstname, lastname, email, password, faculty, admittedTerm, yearofStudy, degree, gpa):
        return True
    else:
        print("[admin.add_student] Error occurred while creating new student: ")
        return False

def admin_update_name(userID, firstname, lastname):
    if update_name(userID, firstname, lastname):
        return True
    else:
        print("[admin_update_name] Error occurred while updating the name of user: "+userID)
        return False

def admin_update_username(userID, username):
    if update_username(userID, username):
        return True
    else:
        print("[admin_update_name] Error occurred while updating the username of user: "+userID)
        return False

def admin_update_email(userID, email):
    if update_email(userID, email):
        return True
    else:
        print("[admin_update_name] Error occurred while updating the email of user: "+userID)
        return False

def admin_update_password(userID, password):
    if update_password(userID, password):
        return True
    else:
        print("[admin_update_name] Error occurred while updating the password of user: "+userID)
        return False

def admin_update_faculty(userID, faculty):
    if update_faculty(userID, faculty):
        return True
    else:
        print("[admin_update_name] Error occurred while updating the faculty of user: "+userID)
        return False

def admin_update_student_admittedTerm(studentID, admittedTerm):
    if update_admittedTerm(studentID, admittedTerm):
        return True
    else:
        print("[admin_update_name] Error occurred while updating the admitted term of student: "+studentID)
        return False

def admin_update_student_yearOfStudy(studentID, yearofStudy):
    if update_yearofStudy(studentID, yearofStudy):
        return True
    else:
        print("[admin_update_name] Error occurred while updating the year of study of student: "+studentID)
        return False

def admin_update_student_degree(studentID, degree):
    if update_degree(studentID, degree):
        return True
    else:
        print("[admin_update_name] Error occurred while updating the degree of student: "+studentID)
        return False

