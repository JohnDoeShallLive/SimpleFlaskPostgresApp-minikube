import uuid
from datetime import datetime

from app import db


class Account(db.Model):
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    created = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    country = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)

    items = db.relationship("Item", back_populates="account", cascade="all, delete-orphan")


class Item(db.Model):
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    created = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.00)
    description = db.Column(db.Text, nullable=True)
    image_link = db.Column(db.String(1000), nullable=True)

    account_id = db.Column(db.String(50), db.ForeignKey("account.id"), nullable=False)
    account = db.relationship("Account", back_populates="items")
