from flask import Blueprint, jsonify, render_template, request, flash, send_from_directory, redirect, url_for
from flask_login import login_required, current_user
import textwrap

from App.models import Customer, User #,  Staff, Review
from App.controllers import (
    sell_item
)


item_views = Blueprint('item_views',
                        __name__,
                        template_folder='../templates')
'''
Page/Action Routes
'''

@item_views.route("/cartPage", methods=["GET"])
def cart_page():
    
    return render_template("cartPage.html")

@item_views.route("/reduce_stock/<int:item_id>", methods=["GET"])
def reduce_stock_action(item_id):
    sell_item(item_id, 2) #Replace 2 with the a varibale for quantity, which we get from some form or number picker.
    return redirect(request.referrer)