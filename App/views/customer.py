from flask import Blueprint, jsonify, render_template, request, flash, send_from_directory, redirect, url_for
from flask_login import login_required, current_user
import textwrap

from App.models import Customer, User #,  Staff, Review

# from App.controllers import (
#     get_student_by_UniId, get_student_by_id,
#     get_staff_by_id, get_staff_by_id, create_review, get_karma,
#     calculate_ranks, get_reviews, get_review, edit_review_work, delete_review_work,
#     create_comment, get_comment, get_comment_staff,
#     get_reply, create_reply, get_all_reviews, create_staff, get_student_review_index, get_karma_history,
#     like, dislike, update_staff_profile, get_all_students_json, get_staff_by_username, login_user)            #added get_reviews


customer_views = Blueprint('customer_views',
                        __name__,
                        template_folder='../templates')
'''
Page/Action Routes
'''

@customer_views.route("/Home", methods=["GET"])
def index_page():
    
    return render_template("landingPage.html")
