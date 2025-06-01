from App.models import Order, OrderItem
from App.database import db
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required, current_user

from .customer import(
    get_customer_by_id, get_customer_cart_id
)

from .product import(
    sell_item, remove_item_from_cart
)

from .cart import(
    get_cart_by_id
)

def get_all_orders(customer_id):
    try:
        existing_customer = get_customer_by_id(customer_id)

        if not existing_customer:
            return None

        orders = Order.query.filter_by(customerID=existing_customer.ID).all()

        if orders:
            return orders
        else:
            return None
    except SQLAlchemyError as e:
        print(f'[DB_ERROR] create_order: {e}')
        return None


def get_order_by_id(order_id):
    try:
        order = Order.query.filter_by(ID=order_id).first()

        if order:
            return order
        else:
            return None
    except SQLAlchemyError as e:
        print(f'[DB_ERROR] get_order_by_id: {e}')
        return None


def create_order (customer_id, total_amount, status, stripe_session_id, stripe_payment_intent, line_items):

    try:
        existing_customer = get_customer_by_id(customer_id)

        if not existing_customer:
            return None

        if total_amount <= 0:
            return None

        new_order = Order(
            customerID=customer_id,
            total_amount=total_amount,
            stripe_session_id=stripe_session_id,
            stripe_payment_intent=stripe_payment_intent,
            status=status
        )

        db.session.add(new_order)
        db.session.flush()

        if new_order:

            for item in line_items:

                product_id = item['price_data']['product_data']['name']
                product_name = item['price_data']['product_data']['description']
                quantity = item['quantity']
                unit_amount = item['price_data']['unit_amount']

                existing_order_item = OrderItem.query.filter_by(orderID=new_order.ID, productID=product_id).first()

                if not existing_order_item:
                    new_order_item = OrderItem(
                        orderID=new_order.ID,
                        productID=product_id,
                        product_name=product_name,
                        order_quantity=quantity,
                        price_at_purchase=unit_amount
                    )
                    db.session.add(new_order_item)
            db.session.commit()
            return new_order
        else:
            return None
    except SQLAlchemyError as e:
        print(f'[DB_ERROR] create_order: {e}')
        db.session.rollback()
        return None

def check_stock(stripe_session_id):
    try:
        
        existing_order = Order.query.filter_by(stripe_session_id=stripe_session_id).first()

        if not existing_order:
            return None

        for item in existing_order.items:
            if item.product.stock < item.order_quantity:
                return False

        for item in existing_order.items:
            sell_item(item_id=item.product.ID, quantity=item.order_quantity)
        
        return True
    except SQLAlchemyError as e:
        print(f'[DB_ERROR] check_stock: {e}')
        return None

def update_order (stripe_session_id, status):

    try:
        # existing_customer = get_customer_by_id(customer_id)

        # if not existing_customer:
        #     return None

        existing_order = Order.query.filter_by(stripe_session_id=stripe_session_id).first()
        if existing_order:
            existing_order.status = status
            db.session.commit()
            return existing_order
        else:
            return None
    except SQLAlchemyError as e:
        print(f'[DB_ERROR] update_order: {e}')
        db.session.rollback()
        return None