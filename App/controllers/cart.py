from App.models import Cart, Customer
from App.database import db
from sqlalchemy.exc import SQLAlchemyError

from .customer import(
    get_customer_by_id
)

def get_cart_by_id(cart_id):
    try:
        cart = Cart.query.filter_by(ID=cart_id).first()

        if cart:
            return cart
        else:
            return None
    except SQLAlchemyError as e:
        print(f'[DB_ERROR] get_cart_by_id: {e}')
        return None

def create_cart(customer_id):

    try:
        existing_cart = get_cart_by_id(customer_id)

        existing_customer = get_customer_by_id(customer_id)

        if not existing_customer:
            print ("Not existing customer")
            return None

        if existing_cart:
            print("cart exists already")
            return None
        else:
            new_cart = Cart(customerID=customer_id)
            new_cart.items =[]

            if new_cart:
                db.session.add(new_cart)
                db.session.commit()
                print(f'Successfulyl made a cart, with the id: {existing_customer.customerCart.ID}')
                return new_cart
            else:
                print("Not successfull making a cart")
                return None
    except SQLAlchemyError as e:
        print(f'[DB_ERROR] create_cart: {e}')
        return None

