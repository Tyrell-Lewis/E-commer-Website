from App.models import Staff, Review, Student
from App.database import db 
import os
from werkzeug.utils import secure_filename

from .review import (
    create_review,
    get_review
)
from .student import(
    get_student_by_id,
    get_student_by_username,
    get_students_by_degree,
    get_students_by_faculty
)

def create_staff(username, firstname, lastname, email, password, faculty):
    newStaff = Staff(username, firstname, lastname, email, password, faculty)
    db.session.add(newStaff)
    
    try:
        db.session.commit()
        return True
    except Exception as e:
        print("[staff.create_staff] Error occurred while creating new staff: ", str(e))
        db.session.rollback()
        return False
    

def get_staff_by_id(id):
    try:
        staff = Staff.query.filter_by(ID=id).first()
        if staff:
            return staff
        else:
            return None
    except Exception as e:
        print(f"[staff.get_staff_by_id] Error occurred while fetching staff by ID {id}: ", str(e))
        return None


def get_staff_by_name(firstname, lastname):
    try:
        staff = Staff.query.filter_by(firstname=firstname, lastname=lastname).first()
        if staff:
            return staff
        else:
            return None
    except Exception as e:
        print(f"[staff.get_staff_by_name] Error occurred while fetching staff by name {firstname} {lastname}: ", str(e))
        return None


def get_staff_by_username(username):
    try:
        staff = Staff.query.filter_by(username=username).first()
        if staff:
            return staff
        else:
            return None
    except Exception as e:
        print(f"[staff.get_staff_by_username] Error occurred while fetching staff by username {username}: ", str(e))
        return None


def staff_edit_review(id, details):
    try:
        review = get_review(id)
        if review is None:
            return False
        else:
            review.details = details
            db.session.commit()
            return True
    except Exception as e:
        print("[staff.staff_edit_review] Error occurred while editing review:", str(e))
        db.session.rollback()
        return False


def staff_create_review(staff, student, starRating, details):
    try:
        if create_review(staff, student, starRating, details):
            return True
        else:
            return False
    except Exception as e:
        print("[staff.staff_create_review] Error occurred while creating review:", str(e))
        return False


def update_staff_profile(staff_id, firstname, lastname, faculty, email, profile_pic=None):
    try:
        staff = Staff.query.get(staff_id)

        if not staff:
            raise ValueError("Staff not found")

        staff.firstname = firstname
        staff.lastname = lastname
        staff.faculty = faculty
        staff.email = email

        if profile_pic and profile_pic.filename:
            filename = secure_filename(profile_pic.filename)
            upload_dir = os.path.join('App', 'static', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)

            upload_path = os.path.join(upload_dir, filename)
            profile_pic.save(upload_path)

            staff.profile_pic = f'/static/uploads/{filename}'

        db.session.commit()
    except Exception as e:
        print(f"[staff.update_staff_profile] Error occurred while updating staff profile: {str(e)}")
        db.session.rollback()
        raise
