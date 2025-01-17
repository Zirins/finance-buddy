from flask import Flask, request, jsonify
from flash_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///transactions.db' # Database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False =
db = SQLAlchemy(app) #Initalize SQLAlchemy with Flask

class Transaction(db.model):
    id = db.Column(db.Integer, primary_key=True)        # Auto-incrementing primary primary_key
    date = db.Column(db.String(10), nullable=False)     # Transaction date (e.g., "2025-01-09")
    amount = db.Column(db.float, nullable=False)        # Transaction amount (e.g., $19.99)
    category = db.Column(db.String, nullable=False)     # Transaction category (e.g., "Grocery")
    description = db.Column(db.String, nullable=True)   # Transaction description (e.g., "For dinner")

# In-memory data storage
transactions = []

@app.route("/transactions", methods=["GET"])
def get_transactions():
    # Fetch all transactions
    return jsonify(transactions)

@app.route("/transactions", methods=["POST"])
def create_transaction():
    # Add a new transaction
    transaction = request.json
    transaction["id"] = len(transactions) + 1  # Auto-generate a unique ID
    transactions.append(transaction)
    return jsonify(transaction), 201  # Return the new transaction with a 201 status code

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
