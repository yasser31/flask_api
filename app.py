from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os 


app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': 'YASSERfriha31',
    'db': 'test',
    'host': 'localhost',
    'port': '5432',
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)

class Product(db.Model):
    __tablename__ = 'Prodcut'
    id = db.Column(db.Integer, primary_key = True)
    name= db.Column(db.String(100), unique=True)
    description=db.Column(db.String(200))
    category=db.Column(db.Text)
    
    def __init__(self, name, description, category):
        self.name = name
        self.description = description
        self.category = category 
    
    def __str__(self):
       return self.name

class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "category")

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@app.route("/product", methods=["POST"])
def add():
    name = request.json["name"]
    description = request.json["description"]
    category = request.json["category"]
    
    new_product = Product(name, description, category)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)

@app.route("/product", methods=["GET"])
def get_all():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result.data)

@app.route("/product/<int:product_id>/", methods=["DELETE"])
def delete(product_id):
    product = Product.query.get(id=product_id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)

@app.route("/product/<int:product_id>", methods=["GET"])
def get_one(product_id):
    product = Product.query.get(id=product_id)
    return product_schema.jsonify(product)

@app.route("/product/<int:product_id>", methods=["PUT"])
def Update(product_id):
    product = Product.query.get(id=product_id)
    name = request.json["name"]
    description = request.json["description"]
    category = request.json["category"]
    product.name = name
    product.description = description
    db.session.commit()
    return product_schema.jsonify(new_product)

if __name__ == "__main__":
    app.run(debug=True)