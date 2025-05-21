from App.database import db
from .user import Customer

class Item(db.Model):
    __tablename__ = 'item'
    ID = db.Column(db.Integer, db.ForeignKey('customer.ID', name='fk_customer_user'), primary_key=True)
    brand = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    colour = db.Column(db.String(120), nullable=True) #Change to allow for multiple colours later, for right now just one.
    size = db.Column(db.String(120), nullable=True)# Change to allow for multiple sizes later, right now just one
    clothing_type = db.Column(db.String(120), nullable=False)# Maybe allow for multiple clothing types, maybe not.
    price = db.Column(db.Float, nullable=False)
    availability = db.Column(db.Boolean, default=False)
    stock = db.Column(db.Integer, nullable=True)
    clothing_pic = db.Column(db.Text, nullable=True)

    def __init__(self, name, brand, description, colour, size, clothing_type, price, stock):
        self.name = name
        self.brand = brand
        self.descriModelption = description
        self.colour = colour
        self.size = size
        self.clothing_type = clothing_type
        self.price = price
        self.stock = stock
        
        self.clothing_pic = "https://raw.githubusercontent.com/Tyrell-Lewis/E-commer-Website/refs/heads/main/images/landingPageImages/asus.jpg"
        # self.stats_Affected = stats_Affected

    def get_id(self):
        return self.ID

    def get_json(self):
        return{
            'drill_id': self.id,
            'name': self.name,
            "createdByRegularID": self.createdByRegularID,
            'category': self.category,
            'difficulty': self.difficulty,
            'details': self.details,
            "dateCreated": self.dateCreated.strftime("%d-%m-%Y %H:%M"),  # Format the date/time
            'stats_Affected': self.stats_Affected,
        }
