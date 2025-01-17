from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transactions.db'  # Correct key and path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # Initialize SQLAlchemy with Flask

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)        # Auto-incrementing primary primary_key
    date = db.Column(db.String(10), nullable=False)     # Transaction date (e.g., "2025-01-09")
    amount = db.Column(db.Float, nullable=False)        # Transaction amount (e.g., $19.99)
    category = db.Column(db.String(100), nullable=False)     # Transaction category (e.g., "Grocery")
    description = db.Column(db.String(200), nullable=True)   # Transaction description (e.g., "For dinner")

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
    "id", t.id,
    "date", t.date,
    "amount", t.amount,
    "category", t.category,
    "description", t.description
    } for t in transactions])

@app.route("/transactions", methods=["POST"])
def create_transaction():
    data = request.json
    new_transaction = Transaction(
    date=data["date"]),
    amount=data["amount"],
    grocery=data["grocery"],
    description=data.get("description")
    )

    db.session

@app.route("/transactions/<int:transaction_id>", methods=["PUT"])
def update_transaction(transaction_id):
    # Update an existing transaction
    for transaction in transactions:
        if transaction["id"] == transaction_id:
            transaction.update(request.json)
            return jsonify(transaction)
    return jsonify({"error": "Transaction not found"}), 404

@app.route("/transactions/<int:transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    # Delete a transaction by ID
    global transactions
    transactions = [t for t in transactions if t["id"] != transaction_id]
    return jsonify({"message": "Transaction deleted"})

if __name__ == "__main__":
    app.run(debug=True)  # Start the Flask app in debug mode
