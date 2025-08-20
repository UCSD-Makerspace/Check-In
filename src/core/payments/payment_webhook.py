from flask import Flask, request, jsonify
import global_
from utils.local_db import update_local_payment_terms

app = Flask(__name__)

@app.route("/handle_payment_webhook", methods=["POST"])
def handle_payment_webhook():
    try:
        data = request.json
        student_email = data.get("email")
        student_name = data.get("name")
        pid = data.get("pid")
        term_paid = data.get("term")


        if not student_email or not term_paid:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        success = global_.sheets.user_db.append_payment_to_sheet(
            name=student_name,
            latest_term=term_paid,
            student_id=pid,
            email=student_email
        )

        if not success:
            return jsonify({"status": "warning", "message": "Student not found in database"}), 404
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
