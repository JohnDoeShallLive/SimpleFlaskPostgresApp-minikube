from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import text

from app import db
from models import Account, Item


web_bp = Blueprint("web", __name__)


@web_bp.route("/", methods=["GET"])
def index():
    accounts = Account.query.order_by(Account.created.desc()).all()
    items = Item.query.order_by(Item.created.desc()).all()

    db_connected = True
    try:
        db.session.execute(text("SELECT 1"))
    except Exception:
        db_connected = False

    return render_template(
        "index.html",
        accounts=accounts,
        items=items,
        db_connected=db_connected,
    )


@web_bp.route("/health", methods=["GET"])
def health():
    return {"status": "healthy"}, 200


@web_bp.route("/accounts/create", methods=["POST"])
def create_account():
    try:
        dob_value = request.form.get("dob")
        dob = datetime.strptime(dob_value, "%Y-%m-%d").date() if dob_value else None

        account = Account(
            username=request.form.get("username", "").strip(),
            email=request.form.get("email", "").strip(),
            country=request.form.get("country", "").strip() or None,
            phone_number=request.form.get("phone_number", "").strip() or None,
            dob=dob,
        )
        db.session.add(account)
        db.session.commit()
        flash("Account created successfully.", "success")
    except Exception as exc:
        db.session.rollback()
        flash(f"Failed to create account: {exc}", "danger")

    return redirect(url_for("web.index"))


@web_bp.route("/accounts/<account_id>/edit", methods=["POST"])
def edit_account(account_id):
    account = Account.query.get_or_404(account_id)
    try:
        dob_value = request.form.get("dob")
        account.username = request.form.get("username", "").strip()
        account.email = request.form.get("email", "").strip()
        account.country = request.form.get("country", "").strip() or None
        account.phone_number = request.form.get("phone_number", "").strip() or None
        account.dob = datetime.strptime(dob_value, "%Y-%m-%d").date() if dob_value else None

        db.session.commit()
        flash("Account updated successfully.", "success")
    except Exception as exc:
        db.session.rollback()
        flash(f"Failed to update account: {exc}", "danger")

    return redirect(url_for("web.index"))


@web_bp.route("/accounts/<account_id>/delete", methods=["POST"])
def delete_account(account_id):
    account = Account.query.get_or_404(account_id)
    try:
        db.session.delete(account)
        db.session.commit()
        flash("Account deleted successfully.", "success")
    except Exception as exc:
        db.session.rollback()
        flash(f"Failed to delete account: {exc}", "danger")
    return redirect(url_for("web.index"))


@web_bp.route("/items/create", methods=["POST"])
def create_item():
    try:
        item = Item(
            name=request.form.get("name", "").strip(),
            price=float(request.form.get("price", 0) or 0),
            description=request.form.get("description", "").strip() or None,
            image_link=request.form.get("image_link", "").strip() or None,
            account_id=request.form.get("account_id"),
        )
        db.session.add(item)
        db.session.commit()
        flash("Item created successfully.", "success")
    except Exception as exc:
        db.session.rollback()
        flash(f"Failed to create item: {exc}", "danger")
    return redirect(url_for("web.index"))


@web_bp.route("/items/<item_id>/delete", methods=["POST"])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    try:
        db.session.delete(item)
        db.session.commit()
        flash("Item deleted successfully.", "success")
    except Exception as exc:
        db.session.rollback()
        flash(f"Failed to delete item: {exc}", "danger")
    return redirect(url_for("web.index"))
