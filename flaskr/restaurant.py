from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from flask import request

from flaskr.auth import login_required
from flaskr.db import get_db


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
    """
    <a class="action" href="{{ url_for('restaurant.add_to_cart', id=dish.id) }}?next=">Add to Cart</a>
    """
    return render_template(
        "restaurant/menu.html", dishes=dishes, restaurant_name=restaurant_name
    )


from flask import session


@bp.route("/<dish>/add_to_cart")
def add_to_cart(dish):
    # request
    # import ipdb;ipdb.set_trace()
    print(session["cart_items"])
    if "cart_items" in session:
        session["cart_items"].append(dish)
    else:
        session["cart_items"] = [dish]
    session.modified = True
    return redirect(request.args.get('next'))


def place_order():
    pass
