from . import db 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(500), nullable=True)
    upc = db.Column(db.String(50), nullable=False)
    product_type = db.Column(db.String(50), nullable=False)
    price_excl_tax = db.Column(db.Float, nullable=False)
    price_incl_tax = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)
    availability = db.Column(db.String(50), nullable=False)
    number_of_reviews = db.Column(db.String(20), nullable=False)
    in_stock = db.Column(db.Integer, nullable=False)

