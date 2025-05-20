from App.models import Customer#, Drill
from App.database import db 
import os
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError


# from .drill import (
#     create_drill,
#     get_drill, get_drill_by_name
# )


def create_customer(username, firstname, lastname, email, password):
    newCustomer = Customer(username, firstname, lastname, email, password)
    db.session.add(newCustomer)
    
    try:
        db.session.commit()
        return True
    except Exception as e:
        print("[customer.create_customer] Error occurred while creating new customer: ", str(e))
        db.session.rollback()
        return False

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


# def customer_create_drill(customer, name, details, difficulty, category):
#     try:
#         if create_drill(customer, name, details, difficulty, category):
#             return True
#         else:
#             return False
#     except Exception as e:
#         print("[customer.customer_create_drill] Error occurred while creating drill:", str(e))
#         return False



# def add_favourite_drill(customer_id, drill_id,):
#     try:

#         customer = get_customer_by_id(customer_id)
#         drill = get_drill(drill_id)

        

#         if customer:
#             if drill:
#                 if drill in customer.favouriteDrills:
#                     customer.favouriteDrills.remove(drill)
#                     drill.favouriteStatus = False
#                     db.session.commit()
#                     return drill
#                 else:
#                     customer.favouriteDrills.append(drill)
#                     drill.favouriteStatus = True
#                     db.session.commit()
#                     return drill
#             else:
#                 return None
#         else:
#             return None


#     except SQLAlchemyError as e:
#         print(f"[DB ERROR] add_favourite_drill: {e}")
#         db.session.rollback()
#         return None


# def get_favourite_drills(customerID):
#   try:
#     customer = Customer.query.filter_by(ID=customerID).first()
#     if customer:
#         return customer.favouriteDrills
#     else:
#         None
#   except SQLAlchemyError as e:
#     print(f"[DB ERROR] get_favourite_drills: {e}")
#     return []