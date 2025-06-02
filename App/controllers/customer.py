from App.models import Customer, FavouriteItem#, Drill
from App.database import db 
import os
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError


# from .product import (
#     get_item_by_id
# )


def create_customer(username, firstname, lastname, email, password):
    try:
        newCustomer = Customer(username, firstname, lastname, email, password)
        db.session.add(newCustomer)
    
    
        db.session.commit()
        return True
    except Exception as e:
        print("[customer.create_customer] Error occurred while creating new customer: ", str(e))
        db.session.rollback()
        return False


def get_customer_cart_id(customer_id):
    try:
        customer = get_customer_by_id(customer_id)

        if customer:
            if customer.customerCart:

                # print("should return the id properly")
                return customer.customerCart.ID
            else:
                print("No customer cart!")
                return None
        else:
            print("Not a customer!")
            return None
    except SQLAlchemyError as e:
        print("[customer.get_customer_cart_id] Error occurred while creating new customer: ", str(e))
        return None

def get_customer_cart(customer_id):
    try:
        customer = get_customer_by_id(customer_id)

        if customer:
            # print("should return the id properly")
            return customer.customerCart
        else:
            print("Not a customer!")
            return None
    except SQLAlchemyError as e:
        print("[customer.get_customer_cart_id] Error occurred while creating new customer: ", str(e))
        return None

def get_customer_by_id(id):
    try:
        customer = Customer.query.filter_by(ID=id).first()
        if customer:
            return customer
        else:
            return None
    except Exception as e:
        print(f"[customer.get_customer_by_id] Error occurred while fetching customer by ID {id}: ", str(e))
        return None


def get_customer_by_name(firstname, lastname):
    try:
        customer = Customer.query.filter_by(firstname=firstname, lastname=lastname).first()
        if customer:
            return customer
        else:
            return None
    except Exception as e:
        print(f"[customer.get_customer_by_name] Error occurred while fetching customer by name {firstname} {lastname}: ", str(e))
        return None


def get_customer_by_username(username):
    try:
        customer = Customer.query.filter_by(username=username).first()
        if customer:
            return customer
        else:
            return None
    except Exception as e:
        print(f"[customer.get_customer_by_username] Error occurred while fetching customer by username {username}: ", str(e))
        return None


def update_customer_profile(customer_id, firstname, lastname, email, profile_pic=None):
    try:
        customer = Customer.query.get(customer_id)

        if not customer:
            raise ValueError("Customer not found")

        customer.firstname = firstname
        customer.lastname = lastname
        customer.email = email

        if profile_pic and profile_pic.filename:
            filename = secure_filename(profile_pic.filename)
            upload_dir = os.path.join('App', 'static', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)

            upload_path = os.path.join(upload_dir, filename)
            profile_pic.save(upload_path)

            customer.profile_pic = f'/static/uploads/{filename}'

        db.session.commit()
    except Exception as e:
        print(f"[customer.update_customer_profile] Error occurred while updating customer profile: {str(e)}")
        db.session.rollback()
        raise

