#import
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///ecommerce.db'

db = SQLAlchemy(app)

#Modeling
#Product (id, name, price, description)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)


@app.route('/api/products/add', methods=["POST"])
def add_product():
    data = request.json
    if "name" in data and "price" in data:
        product = Product(name=data['name'],price=data['price'],description=data.get('description',''))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message":"Product added successfully"})
    return jsonify({"message":"Invalid product data"}),400


@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
    #get product from db
    product=Product.query.get(product_id)
    #if valid
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message":"Product deleted successfully"})
    #if invalid
    return jsonify({"message":"Product not found"}),404


@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
    #get product from db
    product=Product.query.get(product_id)
    #if valid 
    if product:
        return jsonify({
            "id":product.id,
            "name":product.name,
            "price":product.price,
            "description":product.description
        })
    #if invalid
    return jsonify({"message":"Product not found"}),404

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == "__main__":
    app.run(debug=True)