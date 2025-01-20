from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate, ValidationError
from http import HTTPStatus

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transactions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Transaction model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)

# Marshmallow schema for input validation
class TransactionSchema(Schema):
    date = fields.String(required=True, validate=validate.Regexp(r"\d{4}-\d{2}-\d{2}"))
    amount = fields.Float(required=True, validate=lambda x: x > 0)
    category = fields.String(required=True, validate=validate.Length(min=1, max=100))
    description = fields.String(validate=validate.Length(max=200), missing=None)

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)

# Create the database and tables
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "SQLite with Flask is ready to go!"

@app.route("/transactions", methods=["GET"])
def get_transactions():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("limit", 10, type=int)
    transactions = Transaction.query.paginate(page=page, per_page=per_page, error_out=False)

    if not transactions.items:
        return jsonify({"message": "No transactions found on this page"}), HTTPStatus.NOT_FOUND

    return jsonify(transactions_schema.dump(transactions.items)), HTTPStatus.OK

@app.route("/transactions", methods=["POST"])
def create_transaction():
    try:
        data = transaction_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), HTTPStatus.BAD_REQUEST

    new_transaction = Transaction(**data)
    db.session.add(new_transaction)
    db.session.commit()

    return jsonify(transaction_schema.dump(new_transaction)), HTTPStatus.CREATED

@app.route("/transactions/<int:transaction_id>", methods=["PUT"])
def update_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        return jsonify({"error": f"Transaction with ID {transaction_id} not found"}), HTTPStatus.NOT_FOUND

    try:
        data = transaction_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), HTTPStatus.BAD_REQUEST

    transaction.date = data.get("date", transaction.date)
    transaction.amount = data.get("amount", transaction.amount)
    transaction.category = data.get("category", transaction.category)
    transaction.description = data.get("description", transaction.description)

    db.session.commit()
    return jsonify(transaction_schema.dump(transaction)), HTTPStatus.OK

@app.route("/transactions/<int:transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        return jsonify({"error": f"Transaction with ID {transaction_id} not found"}), HTTPStatus.NOT_FOUND

    db.session.delete(transaction)
    db.session.commit()
    return jsonify({"message": "Transaction deleted!"}), HTTPStatus.OK

if __name__ == "__main__":
    app.run(debug=True)
