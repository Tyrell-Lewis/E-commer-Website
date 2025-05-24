from App.database import db

class CartItem(db.Model):
    __tablename__ = 'cart_item'
    ID = db.Column(db.Integer, primary_key=True)

    cartID = db.Column(db.Integer, db.ForeignKey('cart.ID', ondelete='CASCADE', name='fk_item_cart'), nullable = False)
    productID = db.Column(db.Integer, db.ForeignKey('product.ID', name='fk_item_product'), nullable = False)
    cart_quantity = db.Column(db.Integer)
    product = db.relationship('Product')

    def __init__(self, cartID, productID, cart_quantity):#, colour, size, clothing_type, price, stock):
        self.cartID = cartID
        self.productID = productID
        self.cart_quantity = cart_quantity


    def get_id(self):
        return self.ID

    def get_json(self):
        return{
            'item_id': self.ID,
            'cartID': self.cartID,
            "productID": self.productID,
            'cart_quantity': self.cart_quantity

        }
