# blue prints are imported 
# explicitly instead of using *
from .index import index_views
from .auth import auth_views
from .customer import customer_views
from .favourites import favourite_views
from .settings import settings_views
from .cart import cart_views


views = [index_views, auth_views, customer_views, favourite_views, settings_views, cart_views]

# blueprints must be added to this list
