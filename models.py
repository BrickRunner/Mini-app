from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ВАЖНО!
    image_url = db.Column(db.String(200), nullable=False)
    tupe = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(10), nullable=True)
    special = db.Column(db.String(50), nullable=True)
    for_what = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    price_1 = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    price_2 = db.Column(db.Float, nullable=False)


    def __repr__(self):
        return f'<Product {self.title}>'
