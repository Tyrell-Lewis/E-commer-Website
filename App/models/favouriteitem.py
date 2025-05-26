from App.database import db
from datetime import datetime

class FavouriteItem(db.Model):
    __tablename__ = 'favourite_item'
    ID = db.Column(db.Integer, primary_key=True)

    customerID = db.Column(db.Integer, db.ForeignKey('customer.ID', ondelete='CASCADE', name='fk_item_favourite'), nullable = False)
    productID = db.Column(db.Integer, db.ForeignKey('product.ID', name='fk_favourite_item_product'), nullable = False)
    #order_quantity = db.Column(db.Integer)
    #price_at_purchase = db.Column(db.Float, nullable=False)
    #product_name = db.Column(db.String(120), nullable=False)
    favourited_at = db.Column(db.DateTime, default=datetime.utcnow)


    product = db.relationship('Product')
    # customer = db.relationship('Customer')

    def __init__(self, customerID, productID):#, colour, size, clothing_type, price, stock):
        self.customerID = customerID
        self.productID = productID
        # self.product_name = product_name
        # self.order_quantity = order_quantity
        # self.price_at_purchase = price_at_purchase


    def get_id(self):
        return self.ID

    def get_json(self):
        return{
            'item_id': self.ID,
            'customerID': self.customerID,
            "productID": self.productID
            # 'product_name': self.product_name,
            # 'price_at_purchase': self.price_at_purchase,
            # 'order_quantity': self.order_quantity

        }
