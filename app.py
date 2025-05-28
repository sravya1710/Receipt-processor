from flask import Flask, request, jsonify
import uuid
import math
import re
from datetime import datetime

app = Flask(__name__)
receipts_db = {}

def calculate_points(receipt):
    points = 0
    retailer = receipt.get("retailer", "")
    purchase_date = receipt.get("purchaseDate", "")
    purchase_time = receipt.get("purchaseTime", "")
    items = receipt.get("items", [])
    total = float(receipt.get("total", "0.0"))

    points += len(re.findall(r'[A-Za-z0-9]', retailer))

    if total == int(total):
        points += 50

    if total % 0.25 == 0:
        points += 25

    points += (len(items) // 2) * 5

    for item in items:
        desc = item.get("shortDescription", "").strip()
        price = float(item.get("price", "0.0"))
        if len(desc) % 3 == 0:
            points += math.ceil(price * 0.2)

    if total > 10.00:
        points += 5

    try:
        day = int(purchase_date.split('-')[-1])
        if day % 2 == 1:
            points += 6
    except:
        pass

    try:
        hour = int(purchase_time.split(':')[0])
        minute = int(purchase_time.split(':')[1])
        if hour == 14 or (hour == 15 and minute < 60):
            points += 10
    except:
        pass

    return points

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    data = request.get_json()
    receipt_id = str(uuid.uuid4())
    points = calculate_points(data)
    receipts_db[receipt_id] = points
    return jsonify({"id": receipt_id})

@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    points = receipts_db.get(receipt_id)
    if points is None:
        return jsonify({"error": "Receipt not found"}), 404
    return jsonify({"points": points})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)