from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Customer, Invoice
from flasgger import Swagger
from datetime import datetime
import os

app = Flask(__name__)

# Configuración DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    "MYSQL_URI", "mysql://root:root@mysql-db:3306/shopdb"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Swagger
swagger = Swagger(app)

with app.app_context():
    db.create_all()

# ----------------- CUSTOMERS CRUD -----------------
@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "email": c.email,
        "address": c.address,
        "phone": c.phone
    } for c in customers])

@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    c = Customer.query.get(id)
    if not c:
        return jsonify({"message": "Customer not found"}), 404
    return jsonify({
        "id": c.id,
        "name": c.name,
        "email": c.email,
        "address": c.address,
        "phone": c.phone
    })

@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.json
    new_cust = Customer(
        name=data['name'],
        email=data['email'],
        address=data['address'],
        phone=data['phone']
    )
    db.session.add(new_cust)
    db.session.commit()
    return jsonify({"message": "Customer created successfully"}), 201

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    c = Customer.query.get(id)
    if not c:
        return jsonify({"message": "Customer not found"}), 404
    data = request.json
    c.name = data.get("name", c.name)
    c.email = data.get("email", c.email)
    c.address = data.get("address", c.address)
    c.phone = data.get("phone", c.phone)
    db.session.commit()
    return jsonify({"message": "Customer updated successfully"})

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    c = Customer.query.get(id)
    if not c:
        return jsonify({"message": "Customer not found"}), 404
    db.session.delete(c)
    db.session.commit()
    return jsonify({"message": "Customer deleted successfully"})

# ----------------- INVOICES CRUD -----------------
@app.route('/invoices', methods=['GET'])
def get_invoices():
    invoices = Invoice.query.all()
    return jsonify([{
        "id": i.id,
        "customer_id": i.customer_id,
        "total_amount": i.total_amount,
        "date": str(i.date)
    } for i in invoices])

@app.route('/invoices/<int:id>', methods=['GET'])
def get_invoice(id):
    i = Invoice.query.get(id)
    if not i:
        return jsonify({"message": "Invoice not found"}), 404
    return jsonify({
        "id": i.id,
        "customer_id": i.customer_id,
        "total_amount": i.total_amount,
        "date": str(i.date)
    })

@app.route('/invoices', methods=['POST'])
def create_invoice():
    data = request.json
    new_inv = Invoice(
        customer_id=data['customer_id'],
        total_amount=data['total_amount'],
        date=datetime.strptime(data['date'], "%Y-%m-%d").date()
    )
    db.session.add(new_inv)
    db.session.commit()
    return jsonify({"message": "Invoice created successfully"}), 201

@app.route('/invoices/<int:id>', methods=['PUT'])
def update_invoice(id):
    i = Invoice.query.get(id)
    if not i:
        return jsonify({"message": "Invoice not found"}), 404
    data = request.json
    i.customer_id = data.get("customer_id", i.customer_id)
    i.total_amount = data.get("total_amount", i.total_amount)
    if "date" in data:
        i.date = datetime.strptime(data["date"], "%Y-%m-%d").date()
    db.session.commit()
    return jsonify({"message": "Invoice updated successfully"})

@app.route('/invoices/<int:id>', methods=['DELETE'])
def delete_invoice(id):
    i = Invoice.query.get(id)
    if not i:
        return jsonify({"message": "Invoice not found"}), 404
    db.session.delete(i)
    db.session.commit()
    return jsonify({"message": "Invoice deleted successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
