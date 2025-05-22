from App.models import Item, Cart
from App.database import db
import ast
from sqlalchemy.exc import SQLAlchemyError

from .cart import(
    create_cart, get_cart_by_id
)

def create_item(name, brand, description, colour, size, clothing_type, price, stock):
    try:
        new_item = Item(name=name, brand=brand, description=description, colour=colour, size=size, clothing_type=clothing_type,
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
        items = Item.query.all()

        if items:
            return items
        else:
            return None
    except SQLAlchemyError as e:
        print(f"[DB ERROR] get_all_items: {e}")
        return []

def get_item_by_id(item_id):
    try:
        item = Item.query.filter_by(ID=item_id).first()

        if item:
            return item
        else:
            return None
    except SQLAlchemyError as e:
        print(f"[DB ERROR] get_item_by_id: {e}")
        return None


def add_item_to_cart(item_id, cart_id, customer_id, quantity):
    try:
        existing_cart = get_cart_by_id(cart_id)

        if existing_cart:
            cart = existing_cart
        else:
            return False

        existing_item = get_item_by_id(item_id)

        if existing_item:
            if existing_item.stock >= quantity:
                existing_item.cart_quantity = quantity
                cart.items.append(existing_item)
                db.session.add(existing_item)
                db.session.commit()
                print(f'{existing_item.cart_quantity} of Item{existing_item.name} was added to cart: {cart.ID}')
                return True
            else:
                print("Not enough stock!")
                return False
        else:
            print("Not a valid item")
            return False
    except SQLAlchemyError as e:
        print(f"[DB ERROR] add_item_to_cart: {e}")
        return False

