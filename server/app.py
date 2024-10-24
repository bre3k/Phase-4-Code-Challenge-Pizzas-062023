#!/usr/bin/env python3
from flask import request, make_response
from config import app, db, api  
from models import Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
import os

# Initialize migrations
migrate = Migrate(app, db, render_as_batch=True)

db.init_app(app)

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route("/restaurants", methods=["GET", "POST"])
def restaurants():
    if request.method == "GET":
        restaurants = Restaurant.query.all()
        restaurants_dict = [restaurant.to_dict(rules=("-restaurant_pizzas",)) for restaurant in restaurants]
        response = make_response(restaurants_dict, 200, {"Content-Type": "application/json"})
        return response

    elif request.method == "POST":
        restaurant = Restaurant(
            name=request.get_json()["name"],
            address=request.get_json()["address"]
        )
        db.session.add(restaurant)
        db.session.commit()
        response = make_response(restaurant.to_dict(), 201, {"Content-Type": "application/json"})
        return response


@app.route("/restaurants/<int:id>", methods=["GET", "PATCH", "DELETE"])
def restaurant_by_id(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()

    if restaurant:
        if request.method == "GET":
            response = make_response(restaurant.to_dict(), 200, {"Content-Type": "application/json"})
            return response

        elif request.method == "PATCH":
            for attr in request.get_json():
                setattr(restaurant, attr, request.get_json()[attr])
            db.session.add(restaurant)
            db.session.commit()

            response = make_response(restaurant.to_dict(), 200, {"Content-Type": "application/json"})
            return response

        elif request.method == "DELETE":
            db.session.delete(restaurant)
            db.session.commit()
            response = make_response({}, 204)
            return response

    else:
        message = {"error": "Restaurant not found"}
        return make_response(message, 404)

# Similar cleanup for Pizza and RestaurantPizza routes...

if __name__ == "__main__":
    app.run(port=5555, debug=True)

