from App.models import Product, Cart, CartItem
from App.database import db
import ast
from sqlalchemy.exc import SQLAlchemyError

from .cart import(
    create_cart, get_cart_by_id
)

#Switch the names from itme to product eventually, just not right now
def create_item(name, brand, description, colour, size, clothing_type, price, stock):
    try:
        new_item = Product(name=name, brand=brand, description=description, colour=colour, size=size, clothing_type=clothing_type,
                        price=price, stock=stock)

        if new_item:
            new_item.availability = True
            db.session.add(new_item)
            db.session.commit()
            return new_item
    except SQLAlchemyError as e:
        print(f"[DB ERROR] create_item: {e}")
        db.session.rollback()
        return None

def sell_item(item_id, quantity):
    try:
        existing_item = get_item_by_id(item_id)

        if existing_item:
            if existing_item.stock >= quantity:
                existing_item.stock = existing_item.stock - quantity

                if existing_item.stock <= 0:
                    existing_item.stock = 0
                    existing_item.availability = False
                db.session.add(existing_item)
                db.session.commit()
                return True
            else:
                print("Not enough in stock")
                return False
        else:
            print("Not an item")
            return False
    except SQLAlchemyError as e:
        print(f"[DB_ERROR] decrease_item_stock: {e} ")
        db.session.rollback()
        return False



def get_all_items():
    try:
        items = Product.query.all()

        if items:
            return items
        else:
            return None
    except SQLAlchemyError as e:
        print(f"[DB ERROR] get_all_items: {e}")
        return []

def get_item_by_id(item_id):
    try:
        item = Product.query.filter_by(ID=item_id).first()

        if item:
            return item
        else:
            return None
    except SQLAlchemyError as e:
        print(f"[DB ERROR] get_item_by_id: {e}")
        return None


def add_item_to_cart(item_id, cart_id, customer_id, quantity):
    try:
        cart = get_cart_by_id(cart_id)

        if not cart:
            return False

        product = get_item_by_id(item_id)

        if not product:
            return False

        if product.stock < quantity:
            print("Not enough stock")
            return False

        existing_cart_item = CartItem.query.filter_by(cartID=cart.ID, productID=product.ID).first()

        if existing_cart_item:
            new_quantity = existing_cart_item.cart_quantity + quantity
            existing_cart_item.cart_quantity = min(new_quantity, product.stock)
            db.session.commit()
            print(f"Updated quantity for Product '{product.name}' in Cart {cart.ID}")
        else:
            new_cart_item = CartItem(cartID=cart.ID, productID=product.ID, cart_quantity=quantity)
            db.session.add(new_cart_item)
            db.session.commit()
            print(f"Added {quantity} of Product '{product.name}' to Cart {cart.ID}")
        return True
    except SQLAlchemyError as e:
        print(f"[DB ERROR] add_item_to_cart: {e}")
        db.session.rollback()
        return False


def remove_item_from_cart(item_id, cart_id, customer_id):
    try:
        cart = get_cart_by_id(cart_id)

        if not cart:
            return False

        product = get_item_by_id(item_id)

        if not product:
            return False

        existing_cart_item = CartItem.query.filter_by(cartID=cart.ID, productID=product.ID).first()

        if existing_cart_item:
            db.session.delete(existing_cart_item)
            db.session.commit()
            print(f"Removed Product '{product.name}' in Cart {cart.ID}")
            return True
        else:
            return False
    except SQLAlchemyError as e:
        print(f"[DB ERROR] add_item_to_cart: {e}")
        db.session.rollback()
        return False


def update_item_in_cart(item_id, cart_id, customer_id, quantity):
    # Right now, this is only being used for quantity, but should eventually also take into account updating the item 
    # to change the colour of the item if its in multiple colours, the size from smal, medium etc.
    try:
        cart = get_cart_by_id(cart_id)

        if not cart:
            return False

        product = get_item_by_id(item_id)

        if not product:
            return False

        if product.stock < quantity:
            print("Not enough stock")
            return False

        existing_cart_item = CartItem.query.filter_by(cartID=cart.ID, productID=product.ID).first()

        if existing_cart_item:
            new_quantity = quantity
            existing_cart_item.cart_quantity = min(new_quantity, product.stock)
            db.session.commit()
            print(f"Updated quantity for Product '{product.name}' in Cart {cart.ID}")
            return True
        else:
            return False
    except SQLAlchemyError as e:
        print(f"[DB ERROR] add_item_to_cart: {e}")
        db.session.rollback()
        return False