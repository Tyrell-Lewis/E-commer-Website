from flask import Blueprint, jsonify, render_template, request, flash, send_from_directory, redirect, url_for
from flask_login import login_required, current_user
import textwrap

from App.models import Customer, User #,  Staff, Review

from App.controllers import(
    get_favourite_products, toggle_favourite_product
)


favourite_views = Blueprint('favourite_views',
                        __name__,
                        template_folder='../templates')
'''
Page/Action Routes
'''

@favourite_views.route("/favourites", methods=["GET"])
@login_required
def favourites_page():
    favourites = get_favourite_products(current_user.get_id())
    print(f'The favourites are: {favourites}')
    return render_template("favouritesPage.html", favourites=favourites)

@favourite_views.route("/toggleFavourites/<int:item_id>", methods=["POST"])
@login_required
def toggle_favourites(item_id):
    toggle_favourite_product(customer_id=current_user.get_id(), product_id=item_id)
    return redirect (request.referrer)
