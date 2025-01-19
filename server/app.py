from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transactions.db'  # Correct key and path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # Initialize SQLAlchemy with Flask

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing primary key
    date = db.Column(db.String(10), nullable=False)  # Transaction date (e.g., "2025-01-09")
    amount = db.Column(db.Float, nullable=False)  # Transaction amount (e.g., $19.99)
    category = db.Column(db.String(100), nullable=False)  # Transaction category (e.g., "Grocery")
    description = db.Column(db.String(200), nullable=True)  # Optional description

# Create the database and tables
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "SQLite with Flask is ready to go!"

@app.route("/transactions", methods=["GET"])
def get_transactions():
    # Fetch all transactions from the database
    transactions = Transaction.query.all()
    return jsonify([{
        "id": t.id,
        "date": t.date,
        "amount": t.amount,
        "category": t.category,
        "description": t.description
    } for t in transactions])

@app.route("/transactions", methods=["POST"])
def create_transaction():
    data = request.json
    new_transaction = Transaction(
        date=data["date"],
        amount=data["amount"],
        category=data["category"],  # Corrected to match the model
        description=data.get("description")  # Optional field
    )
    db.session.add(new_transaction)  # Add new transaction to the database
    db.session.commit()  # Save changes
    return jsonify({
        "id": new_transaction.id,
        "date": new_transaction.date,
        "amount": new_transaction.amount,
        "category": new_transaction.category,
        "description": new_transaction.description
    }), 201

@app.route("/transactions/<int:transaction_id>", methods=["PUT"])
def update_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    data = request.json
    transaction.date = data.get("date", transaction.date)
    transaction.amount = data.get("amount", transaction.amount)
    transaction.category = data.get("category", transaction.category)
    transaction.description = data.get("description", transaction.description)
    db.session.commit()  # Save changes
    return jsonify({
        "id": transaction.id,
        "date": transaction.date,
        "amount": transaction.amount,
        "category": transaction.category,
        "description": transaction.description
    })

@app.route("/transactions/<int:transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    db.session.delete(transaction)  # Corrected to delete the fetched transaction object
    db.session.commit()
    return jsonify({"message": "Transaction deleted!"})

if __name__ == "__main__":
    app.run(debug=True)  # Start the Flask app in debug mode
