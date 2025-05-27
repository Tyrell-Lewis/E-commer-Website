from flask import Blueprint, jsonify, render_template, request, flash, send_from_directory, redirect, url_for
from flask_login import login_required, current_user
import textwrap
from sqlalchemy import or_

from App.models import Customer, User, Product #,  Staff, Review
from App.controllers import (
    sell_item, get_all_items
)


item_views = Blueprint('item_views',
                        __name__,
                        template_folder='../templates')
'''
Page/Action Routes
'''

@item_views.route("/Home", methods=["GET"])
def index_page():
    flash(f"Message pop up works!")

    items = get_all_items()
    return render_template("landingPage.html", items=items)

@item_views.route("/cartPage", methods=["GET"])
def cart_page():
    
    return render_template("cartPage.html")

@item_views.route("/reduce_stock/<int:item_id>", methods=["GET"])
def reduce_stock_action(item_id):
    sell_item(item_id, 2) #Replace 2 with the a varibale for quantity, which we get from some form or number picker.
    return redirect(request.referrer)


@item_views.route("/search", methods=["GET"])
def search():
    query = request.args.get('searchQuery', '').strip()

    if not query:
        return redirect (request.referrer)

    #Search working with page reload right now. How it works is that it gets the form query for searching, and uses what is there to match against all instances in the product model.
    search_filter = or_(
        Product.name.ilike(f'%{query}%'),
        Product.brand.ilike(f'%{query}%'),
        Product.colour.ilike(f'%{query}%'),
        Product.clothing_type.ilike(f'%{query}%'),
        #Product.description.ilike(f'%{query}%') Maybe have description but doesnt make senes right now, since the descriptions are all the same for testing.
    )

    results = Product.query.filter(search_filter).all()

    return render_template("landingPage.html", items=results)