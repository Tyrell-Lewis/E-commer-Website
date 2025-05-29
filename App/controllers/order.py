from App.models import Order
from App.database import db
from sqlalchemy.exc import SQLAlchemyError

from .customer import(
    get_customer_by_id
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


def create_order (customer_id, total_amount, status, stripe_session_id, stripe_payment_intent):

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

        if new_order:
            db.session.add(new_order)
            db.session.commit()
            return new_order
        else:
            return None
    except SQLAlchemyError as e:
        print(f'[DB_ERROR] create_order: {e}')
        db.session.rollback()
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