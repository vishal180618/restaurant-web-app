from flask import Blueprint, url_for
from flask import redirect
from flask import render_template
from flask import request

from flaskr.db import get_db
from flask import session

bp = Blueprint("restaurant", __name__, url_prefix="/restaurant")


@bp.route("/list")
def list_restaurants():
    db = get_db()
    restaurants = db.collection("restaurant").stream()
    return render_template("restaurant/list_restaurant.html", restaurants=restaurants,)


@bp.route("/<restaurant_name>/menu")
def see_menu(restaurant_name):
    db = get_db()
    dishes = (
        db.collection("menu").where("restaurant_id", "==", restaurant_name).stream()
    )
    if session.get("cart_items"):
        order = True
    return render_template(
        "restaurant/menu.html", dishes=dishes, restaurant_name=restaurant_name, order=True,
    )


@bp.route("/<dish>/add_to_cart")
def add_to_cart(dish):
    if "cart_items" in session:
        session["cart_items"].append(dish)
    else:
        session["cart_items"] = [dish]
    session.modified = True
    return redirect(request.args.get("next"))

@bp.route("/order")
def place_order():
    db = get_db()
    import ipdb;ipdb.set_trace()
    order = {
        "user_id": 0,
        "total_price" : 0,
        "items": []
    }
    for dish in db.collection("menu").where('id', 'in', session["cart_items"]).stream():
        order['total_price'] += dish.price
        order['items'].append(dish.to_dict())
    db.collection("orders").add(order)
    return redirect(url_for('restaurant.list_restaurants'))



