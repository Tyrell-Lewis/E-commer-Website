from flask import Blueprint, jsonify, render_template, request, flash, send_from_directory, redirect, url_for
from flask_login import login_required, current_user
import textwrap

from App.models import Customer, User #,  Staff, Review
from App.controllers import(
    add_item_to_cart, remove_item_from_cart, update_item_in_cart,
    get_customer_cart, get_customer_cart_id, get_cart_by_id, 
    get_customer_by_id
)

cart_views = Blueprint('cart_views',
                        __name__,
                        template_folder='../templates')
'''
Page/Action Routes
'''

@cart_views.route("/cartPage", methods=["GET"])
@login_required
def cart_page():
    cart_id = get_customer_cart_id(current_user.get_id())

    customer = get_customer_by_id(current_user.get_id())
    print(f'This user {current_user.get_id()} has a cart id of: {cart_id} ')
    cart = get_cart_by_id(cart_id)
    return render_template("cartPage.html", cart=cart, customer=customer)

@cart_views.route("/addToCart/<int:item_id>", methods=["GET"])
@login_required
def add_to_cart_action(item_id):
    # customer = current_user.get_id()
    cart_id = get_customer_cart_id(current_user.get_id())

    #cart = get_customer_cart(current_user.get_id())


    add_item_to_cart(item_id=item_id, cart_id=cart_id, customer_id=current_user.get_id(), quantity=3)
    
    return redirect(request.referrer)


@cart_views.route("/removeFromCart/<int:item_id>", methods=["GET"])
@login_required
def remove_from_cart_action(item_id):
    # customer = current_user.get_id()
    cart_id = get_customer_cart_id(current_user.get_id())

    #cart = get_customer_cart(current_user.get_id())

    print(f'Removing cart_item: {item_id} from the cart: {cart_id}')

    remove_item_from_cart(item_id=item_id, cart_id=cart_id, customer_id=current_user.get_id())
    
    return redirect(request.referrer)


@cart_views.route("/updateInCart/<int:item_id>", methods=["GET"])
@login_required
def update_item_cart_action(item_id):
    # customer = current_user.get_id()
    cart_id = get_customer_cart_id(current_user.get_id())

    #cart = get_customer_cart(current_user.get_id())
    print(f'Updating cart_item: {item_id} from the cart: {cart_id}')

    update_item_in_cart(item_id=item_id, cart_id=cart_id, customer_id=current_user.get_id(), quantity=7)
    
    return redirect(request.referrer)


