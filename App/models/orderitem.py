from App.database import db

class OrderItem(db.Model):
    __tablename__ = 'order_item'
    ID = db.Column(db.Integer, primary_key=True)

    orderID = db.Column(db.Integer, db.ForeignKey('order.ID', ondelete='CASCADE', name='fk_item_order'), nullable = False)
    productID = db.Column(db.Integer, db.ForeignKey('product.ID', name='fk_order_item_product'), nullable = False)
    order_quantity = db.Column(db.Integer)
    price_at_purchase = db.Column(db.Float, nullable=False)
    product_name = db.Column(db.String(120), nullable=False)
    product = db.relationship('Product')

    def __init__(self, orderID, productID, product_name, order_quantity, price_at_purchase):#, colour, size, clothing_type, price, stock):
        self.orderID = orderID
        self.productID = productID
        self.product_name = product_name
        self.order_quantity = order_quantity
        self.price_at_purchase = price_at_purchase


    def get_id(self):
        return self.ID

    def get_json(self):
        return{
            'item_id': self.ID,
            'orderID': self.orderID,
            "productID": self.productID,
            'product_name': self.product_name,
            'price_at_purchase': self.price_at_purchase,
            'order_quantity': self.order_quantity

        }
