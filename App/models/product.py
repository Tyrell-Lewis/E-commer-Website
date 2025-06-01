from App.database import db

class Product(db.Model):
    __tablename__ = 'product'
    ID = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    colour = db.Column(db.String(120), nullable=True) #Change to allow for multiple colours later, for right now just one.
    size = db.Column(db.String(120), nullable=True)# Change to allow for multiple sizes later, right now just one
    clothing_type = db.Column(db.String(120), nullable=False)# Maybe allow for multiple clothing types, maybe not.
    price = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.Boolean, default=False)
    stock = db.Column(db.Integer, nullable=True)
    picture = db.Column(db.Text, nullable=True)
    # cartID = db.Column(db.Integer, db.ForeignKey('cart.ID', ondelete='CASCADE', name='fk_item_cart'), nullable = True)
    # cart_quantity = db.Column(db.Integer)

    def __init__(self, name, brand, description, colour, size, clothing_type, price, stock):
        self.name = name
        self.brand = brand
        self.description = description
        self.colour = colour
        self.size = size
        self.clothing_type = clothing_type
        self.price = price
        self.stock = stock
        
        self.picture = "/static/landingPageImages/asus.jpg"
        # self.stats_Affected = stats_Affected

    def get_id(self):
        return self.ID

    def get_json(self):
        return{
            'item_id': self.ID,
            'name': self.name,
            "brand": self.brand,
            'description': self.description,
            'colour': self.colour,
            'size': self.size,
            "clothing_type": self.clothing_type,  # Format the date/time
            'price': self.price,
            'stock': self.stock,
            'availability': self.availability,
            'picture': self.picture
        }
