from App.database import db


class Cart(db.Model):
    __tablename__ = 'cart'
    ID = db.Column(db.Integer, primary_key=True)
    #
    customerID = db.Column(db.Integer, db.ForeignKey('customer.ID', name='fk_cart_customer',
                                                     ondelete='CASCADE'), unique=True, nullable=False)
    items = db.relationship('CartItem', backref='in_cart', cascade="all, delete-orphan", passive_deletes=True)
    cartPrice = db.Column(db.Integer, nullable=False, default=0.0)




    def __init__(self, customerID=customerID):
        self.customerID = customerID
        self.items = []


    def get_id(self):
        return self.ID

    def get_json(self):
        return{
            'cart_id': self.id,
            'customerID': self.customerID,
            "cartPrice": self.cartPrice

        }

