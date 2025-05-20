from App.database import db
from .student import Student
from .karma import Karma  # Import Karma model
from datetime import datetime
from sqlalchemy import func

starValue = {
        0: -5,
        1:-3,
        2:-1,
        3:1,
        4:3,
        5:5
    }

class Review(db.Model):
    __tablename__ = 'review'
    ID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('student.ID', name='fk_review_student'))
    createdByStaffID = db.Column(db.Integer, db.ForeignKey('staff.ID', name='fk_review_staff'))
    dateCreated = db.Column(db.DateTime, server_default=func.now())
    starRating = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    details = db.Column(db.String(400), nullable=False)
    likes = db.Column(db.Integer, nullable=False, default=0)
    dislikes = db.Column(db.Integer, nullable=False, default=0)
    comments = db.relationship('Comment', backref='review', cascade="all, delete-orphan", passive_deletes=True)

    liked_by_staff = db.Column(db.String, default='')
    disliked_by_staff = db.Column(db.String, default='')

    liked_by_staff = db.Column(db.String, default='')
    disliked_by_staff = db.Column(db.String, default='')

    def __init__(self, staff, student, starRating, details):
        self.createdByStaffID = staff.ID
        self.studentID = student.ID
        self.starRating = starRating
        if (starValue[starRating]):
            self.value = starValue[starRating]
        else:
            self.value = 0
        self.details = details
        self.comments = []

    def get_id(self):
        return self.ID

    def to_json(self):
        return {
            "reviewID": self.ID,
            "studentID": self.studentID,
            "createdByStaffID": self.createdByStaffID,
            "dateCreated": self.dateCreated.strftime("%d-%m-%Y %H:%M"),  # Format the date/time
            "starRating": self.starRating,
            "likes": self.likes,
            "dislikes": self.dislikes,
            "details": self.details
        }