from config import db  # Import the initialized db
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    restaurant_pizzas = db.relationship("RestaurantPizza", back_populates="restaurant", cascade="all, delete-orphan")
    serialize_rules = ("-restaurant_pizzas.restaurant",)

    pizzas = association_proxy("restaurant_pizzas", "pizza", creator=lambda pizza_obj: RestaurantPizza(pizza=pizza_obj))

    def __repr__(self):
        return f"<Restaurant {self.name}>"

class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    restaurant_pizzas = db.relationship("RestaurantPizza", back_populates="pizza", cascade="all, delete-orphan")
    serialize_rules = ("-restaurant_pizzas.pizza",)

    restaurants = association_proxy("restaurant_pizzas", "restaurant", creator=lambda restaurant_obj: RestaurantPizza(restaurant=restaurant_obj))

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"))

    restaurant = db.relationship("Restaurant", back_populates="restaurant_pizzas")
    pizza = db.relationship("Pizza", back_populates="restaurant_pizzas")

    serialize_rules = ("-restaurant.restaurant_pizzas", "-pizza.restaurant_pizzas")

    @validates("price")
    def validate_price(self, key, price):
        if not (1 <= price <= 30):
            raise ValueError("Price must be between 1 and 30")
        return price

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
