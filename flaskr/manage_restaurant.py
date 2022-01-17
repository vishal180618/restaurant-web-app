from collections import defaultdict
from datetime import datetime

from flask import Blueprint, url_for, jsonify
from flask import redirect
from flask import render_template
from flask import session, request

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("manage", __name__, url_prefix="/manage")


@bp.route("/order/count", methods=("GET",))
def get_today_order_count():
    db = get_db()
    count = 0
    current = datetime.now()
    TODAY = datetime(current.year, current.month, current.day)
    for _ in db.collection("orders").where("created", ">=", TODAY).stream():
        count += 1
    return count, 200


@bp.route("/order/info", methods=("GET",))
def get_today_order_info():
    db = get_db()

    current = datetime.now()
    TODAY = datetime(current.year, current.month, current.day)
    db.collection("orders").where("created", ">=", TODAY)


@bp.route("/order/update-status", methods=("PUT",))
def update_order_status(order_id, updated_status):
    db = get_db()

    _, ref = db.collection(f"orders/{order_id}/order_status").add(
        {"status": updated_status, "time": datetime.now(),}
    )
    return ref.to_dict(), 201


@bp.route("/menu/add-item", methods=("POST",))
def add_item_to_menu(restaurant_id, new_item):
    db = get_db()
    _, ref = db.collection(f"restaurant/{restaurant_id}/menu").add(new_item)
    return ref.to_dict(), 201


@bp.route("/menu/delete-item", methods=("POST",))
def delete_item_from_menu(restaurant_id, menu_item_id):
    db = get_db()
    db.collection(f"restaurant/{restaurant_id}/menu").document(menu_item_id).delete()
    # or set it to not active
    # db.collection(f"restaurant/{restaurant_id}/menu").document(menu_item_id).set(
    #     {"active": False}
    # )
    return {}, 200


@bp.route("/menu/change-item", methods=("PUT",))
def change_item_in_menu(restaurant_id, menu_item_id, attribute, change):
    db = get_db()
    db.collection(f"restaurant/{restaurant_id}/menu").document(menu_item_id).update(
        {attribute: change}
    )
    return {}, 200


@bp.route("/<restaurant_id>/order/status-summary", methods=("GET",))
def get_order_status_summary(restaurant_id):
    db = get_db()

    current = datetime.now()
    TODAY = datetime(current.year, current.month, current.day)
    db.collection("orders").where("created", ">=", TODAY)

    db.collection("orders").where("restaurant_id", "==", restaurant_id).where(
        "created", ">=", TODAY
    )


@bp.route("/<restaurant_id>/order/summary", methods=("GET",))
def get_order_summary(restaurant_id):
    db = get_db()
    menu_item_index = defaultdict(set)
    for document in (
        db.collection("orders").where("restaurant_id", "==", restaurant_id).stream()
    ):
        order_items = document.reference.collection("items").stream()
        for item in order_items:
            menu_item_index[item.get("name")].add(document.get("user_id"))

    menu_item_index = {k: len(v) for k, v in menu_item_index.items()}
    favoured_menu_items = sorted(
        menu_item_index.items(), key=lambda x: x[1], reverse=True
    )
    return dict(favoured_menu_items), 200


@bp.route("/<restaurant_id>/customer-info", methods=("GET",))
def get_customer_info(restaurant_id):
    db = get_db()
    start_date, end_date = request.args.get("start_date"), request.args.get("end_date")
    customers = [
        doc.get("user_id")
        for doc in db.collection("orders")
        .where("restaurant_id", "==", restaurant_id)
        .where("created", ">=", start_date)
        .where("created", "<=", end_date)
        .stream()
    ]
    return customers, 200


@bp.route("/<restaurant_id>/customer-expenditure-report", methods=("GET",))
def get_customer_expenditure(restaurant_id):
    db = get_db()
    user_expenditure = defaultdict(int)
    for document in (
        db.collection("orders").where("restaurant_id", "==", restaurant_id).stream()
    ):
        user_expenditure[document.get("user_id")] += document.get("total_price")
    return user_expenditure, 200
