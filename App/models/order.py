from datetime import datetime
from App.database import db

class Order(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    customerID = db.Column(db.Integer, db.ForeignKey('customer.ID', name='fk_order_customer',
                                                     ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'paid', 'cancelled'
    stripe_session_id = db.Column(db.String(120), unique=True)  # to track Stripe session
    stripe_payment_intent = db.Column(db.String(120), unique=True)  
    total_amount = db.Column(db.Integer, nullable=False)  # store in cents (Stripe best practice) store $19.99 as 1999
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = db.relationship('OrderItem', backref='order', cascade="all, delete-orphan", passive_deletes=True)

    def __init__(self, customerID, total_amount, status, stripe_session_id=None, stripe_payment_intent=None):#, colour, size, clothing_type, price, stock):
        self.customerID = customerID
        self.total_amount = total_amount
        self.status = status
        self.stripe_session_id = stripe_session_id
        self.stripe_payment_intent = stripe_payment_intent


    def get_id(self):
        return self.ID

    def get_json(self):
        return{
            'order_id': self.ID,
            'customerID': self.customerID,
            "total_amount": self.total_amount,
            'status': self.status,
            'stripe_session_id': self.stripe_session_id,
            'stripe_payment_intent': self.stripe_payment_intent

        }
