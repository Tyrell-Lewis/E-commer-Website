from flask import Blueprint, jsonify, render_template, request, flash, send_from_directory, redirect, url_for, current_app
from flask_login import login_required, current_user
import textwrap
import stripe
import os
from App.database import db

from App.models import Customer, User, Order #,  Staff, Review
from App.controllers import(
    add_item_to_cart, remove_item_from_cart, update_item_in_cart,
    get_customer_cart, get_customer_cart_id, get_cart_by_id, 
    get_customer_by_id,
    create_order, update_order, get_all_orders, get_order_by_id
)

order_views = Blueprint('order_views',
                        __name__,
                        template_folder='../templates')
'''
Page/Action Routes
'''

@order_views.route("/ordersPage", methods=["GET"])
@login_required
def orders_page():
    orders = get_all_orders(current_user.get_id())
    print(f'The orders are: {orders}')
    return render_template("ordersPage.html", orders=orders)

@order_views.route("/success", methods=["GET"])
def checkout_success():

    return render_template("success.html")

@order_views.route("/cancel", methods=["GET"])

def checkout_cancel():

    return render_template("cancel.html")



@order_views.route('/checkout', methods=['POST'])
def create_checkout_session():

    #For right now, i hard encoded the data, i will make this dynamic to work with the data in
    # of the cart items and use that to populate the line items.

    customer_id = current_user.get_id()

    line_items = [{
            'price_data': {
                'currency': 'usd',
                'unit_amount': 2999,  # in cents is 29.99, Stripe uses integers so its 2999 to represent 29.99
                'product_data': {
                    'name': "blue dragon t-shirt",
                },
            },
            'quantity': 5,
        }]
    total_amount = 29.99

    # Create Stripe checkout session, just follow the stripe docs to make this and append to it in future.
    #Gitpod changes the url on new workspaces, so on erros, change these ur;s to mathc, and also change the stripe webhook destination to match.
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url='https://tyrelllewis-ecommerwebs-uyobk99u90l.ws-us120.gitpod.io/success',
        cancel_url='https://tyrelllewis-ecommerwebs-uyobk99u90l.ws-us120.gitpod.io/cancel',
    )

    #in addition to making the cart items dynamic, also pass the items for the order into this function so you can get it later for the order history.
    create_order(customer_id=customer_id, total_amount=total_amount, 
        stripe_session_id=checkout_session.id,
        stripe_payment_intent=checkout_session.payment_intent,
        status='Pending'
    )

    return redirect(checkout_session.url)

@order_views.route('/resume_payment/<int:order_id>', methods=['GET'])
def resume_payment(order_id):
    order = get_order_by_id(order_id)
    checkout_session = stripe.checkout.Session.retrieve(order.stripe_session_id)
    return redirect(checkout_session.url)

@order_views.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except stripe.error.SignatureVerificationError:
        return jsonify({"error": "Invalid signature"}), 400

    if event['type'] == 'checkout.session.completed':
        checkout_session = event['data']['object']
        checkout_session_id = checkout_session.get('id')
        print("In paid")
        #Current user does not work here, because this call is made remotely from stripe, not taking into account 
        update_order(stripe_session_id=checkout_session_id, status='Paid')
    elif event['type'] == 'checkout.session.expired':
        checkout_session = event['data']['object']
        checkout_session_id = checkout_session.get('id')
        print("In cancelled")
        update_order(stripe_session_id=checkout_session_id, status='Cancelled')


    return jsonify({'status': 'success'})