# from .user import create_user
# from .customer import create_regular
from App.database import db
from App.controllers import (
    create_item, create_customer, create_cart

)


def initialize():
    db.drop_all()
    db.create_all()

    create_customer(username="bob", firstname="Bob", lastname="Johnson", email="bob@mail.com", password="bobpass")
    create_cart(1)

    create_item(name="Storm Gray Hoodie", brand="UrbanEdge", description="Cozy storm gray hoodie perfect for chilly evenings.",
            colour="gray", size="large", clothing_type="hoodies", price=3999, stock=15)

    create_item(name="Sunset Orange T-Shirt", brand="StyleStreet", description="Bright and bold t-shirt for casual wear.",
                colour="orange", size="medium", clothing_type="t-shirt", price=2499, stock=20)

    create_item(name="Midnight Black Pants", brand="FlexWear", description="Sleek black pants for everyday comfort and style.",
                colour="black", size="large", clothing_type="pants", price=3499, stock=12)

    create_item(name="Crystal White Sneakers", brand="TrackStar", description="Comfortable white sneakers for running or casual outings.",
                colour="white", size="medium", clothing_type="shoes", price=4999, stock=18)

    create_item(name="Olive Green Hoodie", brand="TrailBlaze", description="Stylish olive hoodie with soft fleece lining.",
                colour="olive", size="small", clothing_type="hoodies", price=3899, stock=10)

    create_item(name="Sky Blue T-Shirt", brand="NextGen", description="Lightweight t-shirt ideal for summer days.",
                colour="blue", size="small", clothing_type="t-shirt", price=2199, stock=25)

    create_item(name="Charcoal Jogger Pants", brand="MoveMore", description="Stretch-fit joggers designed for both workouts and lounging.",
                colour="charcoal", size="medium", clothing_type="pants", price=3299, stock=14)

    create_item(name="Crimson Red Sneakers", brand="FastLane", description="High-performance red sneakers with breathable fabric.",
                colour="red", size="large", clothing_type="shoes", price=4799, stock=9)

    create_item(name="Tan Brown Hoodie", brand="CozyCore", description="Warm tan hoodie with kangaroo pocket and drawstring hood.",
                colour="brown", size="medium", clothing_type="hoodies", price=4099, stock=13)

    create_item(name="Mint Green T-Shirt", brand="BreezeFit", description="Fresh mint green tee made from organic cotton.",
                colour="green", size="large", clothing_type="t-shirt", price=2299, stock=17)

