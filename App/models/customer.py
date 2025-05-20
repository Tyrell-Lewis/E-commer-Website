from App.database import db
from .user import User

class Customer(User):
    __tablename__ = 'customer'
    ID = db.Column(db.Integer, db.ForeignKey('user.ID', name='fk_customer_user'), primary_key=True)
    # orders = db.relationship('Order', backref='regularDrils', lazy='joined')
    # favouriteDrills = db.relationship('Drill', secondary=favourite_drills, backref='favourited_by',lazy='joined')

    # regular.favouriteDrills: list of drills the regular favourited
    # drill.favourited_by: list of regulars who favourited the drill
    # This is how you access the favourite drills if anyone isnt sure.

    profile_pic = db.Column(db.Text, nullable=True)

    __mapper_args__ = {"polymorphic_identity": "customer"}

    def __init__(self, username, firstname, lastname, email, password):
        super().__init__(username=username,
                        firstname=firstname,
                        lastname=lastname,
                        email=email,
                        password=password)
        # self.favouriteDrills = []
        # self.drills =[]
        self.profile_pic = "https://st3.depositphotos.com/4111759/13425/v/600/depositphotos_134255634-stock-illustration-avatar-icon-male-profile-gray.jpg"

    



    def to_json(self):
        return {
            "staffID":self.ID,
            "username":self.username,
            "firstname":self.firstname,
            "lastname":self.lastname,
            "email":self.email
            # "favouriteDrills": [drill.to_json() for drill in self.favouriteDrills],
            # "Drills": [drill.to_json() for drill in self.drills]
        }

    def __repr__(self):
        return f'<Customer {self.ID} :{self.email}>'
