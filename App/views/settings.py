from flask import Blueprint, jsonify, render_template, request, flash, send_from_directory, redirect, url_for
from flask_login import login_required, current_user
import textwrap

from App.models import Customer, User #,  Staff, Review



settings_views = Blueprint('settings_views',
                        __name__,
                        template_folder='../templates')
'''
Page/Action Routes
'''

@settings_views.route("/supportPage", methods=["GET"])
def settings_page():
    
    return render_template("supportPage.html")

@settings_views.route("/contactPage", methods=["GET"])
def contact_page():
    
    return render_template("contactPage.html")
