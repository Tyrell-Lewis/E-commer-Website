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
    create_item(name="Blue dragon t-shirt", brand="brand name", description="Description for blue dragon t-shirt",
                 colour="blue", size="medium", clothing_type="t-shirt", price=29.99, stock=10)
    create_item(name="Red lion pants", brand="brand name", description="Description for Red lion pants",
                 colour="red", size="medium", clothing_type="pants", price=29.99, stock=10)
    create_item(name="green dragon t-shirt", brand="brand name", description="Description for green dragon t-shirt",
                 colour="green", size="medium", clothing_type="t-shirt", price=29.99, stock=10)
    create_item(name="purple dragon t-shirt", brand="brand name", description="Description for purple dragon t-shirt",
                 colour="purple", size="medium", clothing_type="t-shirt", price=29.99, stock=10)

