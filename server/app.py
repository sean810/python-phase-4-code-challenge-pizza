from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from models import db, Restaurant, Pizza, RestaurantPizza
from flask_migrate import Migrate
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Home route (root URL)
@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Pizza API! Go to /restaurants or /restaurants/<id> to view the data."

# Route to get all restaurants
@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict() for restaurant in restaurants])

# Route to get a specific restaurant by ID
@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    return jsonify(restaurant.to_dict())

# Route to delete a specific restaurant by ID
@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    
    # Delete associated restaurant pizzas
    RestaurantPizza.query.filter_by(restaurant_id=id).delete()
    
    db.session.delete(restaurant)
    db.session.commit()
    
    return "", 204

# Route to get all pizzas
@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.to_dict() for pizza in pizzas])

# Route to create a new restaurant-pizza combination
@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()
    
    pizza = Pizza.query.get(data.get('pizza_id'))
    restaurant = Restaurant.query.get(data.get('restaurant_id'))
    
    if not pizza or not restaurant:
        return jsonify({"error": "Restaurant or Pizza not found"}), 404
    
    # Validate the price
    if 'price' not in data or not (1 <= data['price'] <= 30):
        return jsonify({"errors": ["Price must be between 1 and 30"]}), 400
    
    restaurant_pizza = RestaurantPizza(
        price=data['price'],
        pizza_id=data['pizza_id'],
        restaurant_id=data['restaurant_id']
    )
    
    db.session.add(restaurant_pizza)
    db.session.commit()
    
    return jsonify(restaurant_pizza.to_dict()), 201

if __name__ == "__main__":
    app.run(port=5555, debug=True)
