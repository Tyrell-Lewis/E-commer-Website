from flask import Blueprint, jsonify, render_template, request, flash, send_from_directory, redirect, url_for
from flask_login import login_required, current_user
import textwrap

from App.models import Customer, User #,  Staff, Review
from App.controllers import (
  get_all_items,
)

customer_views = Blueprint('customer_views',
                        __name__,
                        template_folder='../templates')
'''
Page/Action Routes
'''



@customer_views.route("/profile", methods=["GET"])
@login_required
def profile_page():
    
    return render_template("profilePage.html")