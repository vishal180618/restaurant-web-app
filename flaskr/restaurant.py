from datetime import datetime

from flask import Blueprint, url_for, request
from flask import redirect
from flask import render_template
from flask import session

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("restaurant", __name__, url_prefix="/restaurant")


@bp.route("/list")
def list_restaurants():
    """
    address, email, contact number, joined_date, owner id/admin_id
    """
    db = get_db()
    restaurants = db.collection("restaurant").stream()
    return render_template("restaurant/list_restaurant.html", restaurants=restaurants,)


@bp.route("/<restaurant_id>/menu")
def see_menu(restaurant_id):
    """
    category(veg, non-veg), description, active
    """
    db = get_db()
    dishes = db.collection(f"restaurant/{restaurant_id}/menu").stream()
    if session.get("cart_items"):
        order = True
    return render_template(
        "restaurant/menu.html", dishes=dishes, restaurant_id=restaurant_id, order=True,
    )


@bp.route("/<restaurant_id>/<dish_id>/add_to_cart")
def add_to_cart(restaurant_id, dish_id):
    if "cart" not in session:
        session["cart"] = [{"restaurant_id": None, "items": []}]
    cart = session["cart"][0]
    if cart["restaurant_id"] and cart["restaurant_id"] != restaurant_id:
        cart = [{"restaurant_id": None, "items": []}]
    cart["restaurant_id"] = restaurant_id

    db = get_db()
    dish_info = (
        db.collection(f"restaurant/{restaurant_id}/menu")
        .document(dish_id)
        .get()
        .to_dict()
    )
    cart["items"].append(dish_info)

    session.modified = True
    print(session["cart"])
    return redirect(request.args.get("next"))


@bp.route("/order")
@login_required
def place_order():
    db = get_db()
    cart = session["cart"][0]
    order = {
        "user_id": session["user_id"],
        "total_price": 0,
        "items": [],
        "created": datetime.now(),
        "restaurant_id": cart['restaurant_id']
    }
    _, order_ref = db.collection("orders").add(order)
    for item in cart["items"]:
        order_ref.collection("items").add(item)
        order["total_price"] += item["price"]
    order_ref.update({"total_price": order["total_price"]})

    order_ref.collection("order_status").add(
        {"status": "placed", "time": datetime.now(),}
    )

    # batch = db.batch()
    # for item in cart['items']:
    #     batch.create(order_ref.collection("items"), item)
    #     # order_ref.collection("items").add(item)
    #     order['total_price'] += item['price']
    # order_ref.set({"total_price" : order['total_price']})
    # batch.commit()

    session.pop("cart")
    return redirect(url_for("restaurant.list_restaurants"))




