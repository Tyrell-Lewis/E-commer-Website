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
    get_customer_by_id
)

order_views = Blueprint('order_views',
                        __name__,
                        template_folder='../templates')
'''
Page/Action Routes
'''

# stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

# @stripe_routes.route('/payment-success')
# def payment_success():
#     session_id = request.args.get('session_id')
#     session = stripe.checkout.Session.retrieve(session_id)
    
#     # Mark order as paid
#     order = Order.query.filter_by(stripe_session_id=session_id).first()
#     if order:
#         order.status = 'paid'
#         db.session.commit()

#     return "Payment successful! Thank you for your order."

@order_views.route("/success", methods=["GET"])
def checkout_success():

    return render_template("success.html")

@order_views.route("/cancel", methods=["GET"])
def checkout_cancel():

    return render_template("cancel.html")



@order_views.route('/checkout', methods=['POST'])
def create_checkout_session():
    #data = request.get_json()
    #cart_items = data.get('items')  # Format: list of dicts [{name, price, quantity}]
    #customer_id = data.get('customer_id')
    customer_id = current_user.get_id()

    try:
        # Transform cart items into Stripe line items
        line_items = [{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': 2999,  # in cents
                    'product_data': {
                        'name': "blue dragon t-shirt",
                    },
                },
                'quantity': 2,
            }]
        total_amount = 29.99
        # for item in cart_items:
        #     line_items.append({
        #         'price_data': {
        #             'currency': 'usd',
        #             'unit_amount': 2999,  # in cents
        #             'product_data': {
        #                 'name': "blue dragon t-shirt",
        #             },
        #         },
        #         'quantity': 2,
        #     })
        #     total_amount = 29.99

        # Create Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='https://8080-tyrelllewis-ecommerwebs-cqoufjyjoyv.ws-us119.gitpod.io/success',
            cancel_url='https://8080-tyrelllewis-ecommerwebs-cqoufjyjoyv.ws-us119.gitpod.io/cancel',
        )

        # Store order in DB (status = pending)
        new_order = Order(
            customerID=customer_id,
            total_amount=total_amount,
            stripe_session_id=checkout_session.id,
            stripe_payment_intent=checkout_session.payment_intent,
            status='pending'
        )
        db.session.add(new_order)
        db.session.commit()

        return redirect(checkout_session.url)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@order_views.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET_TEST")

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

        order = Order.query.filter_by(stripe_session_id=checkout_session_id).first()
        if order:
            order.status = 'paid'
            db.session.commit()

    return jsonify({'status': 'success'})