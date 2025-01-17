from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data storage
transactions []

@app.route("/transactions", methods=["GET"])
def get_transactions():
    return jsonify(transactions)

@app.route("/transactions", methods=["POST"])
def create_transactions():
    transactions = request.json
    transactions["id"]

@app.route("/transactions", methods=["PUT"])
def update_transactions(transactions_id):
    for transaction in transactions:
        if transactions["id"] == transactions:
            transactions.update(request.json)
            return jsonify(transactions)
       return jsonify("Transaction: update failed")

@app.route("/transactions", methods=["DELETE"]
def delete_transaction(transaction_id):
    global transactions
    transactions = [t for t in transactions if t["id"] != transaction_id]
    return jsonify("Message: DELETE COMPLETED")