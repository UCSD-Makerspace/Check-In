from flask import Flask, request, jsonify
import global_

global_.init()
app = Flask(__name__)

@app.route('/test/payment', methods=['POST'])
def fake_payment_webhook():
    data = request.json
    if not data or "student_id" not in data:
        return jsonify({"error": "Missing student_id"}, 400)
    
    student_id = data["student_id"]
    student_name = data.get("name", "Test User")
    student_email = data.get("email", "test@ucsd.edu")
    term = data.get("term", "SU25")

    print(f"Simulating payment for student {student_id} with term {term}")

    success = global_.sheets.user_db.append_payment_to_sheet(
        name = student_name,
        latest_term = term,
        id = student_id,
        email = student_email,
    )

    if not success:
        return jsonify({"status": "warning", "message": "Student not found in database"}), 404

    global_.sheets.reload_user_db()

    return jsonify({"status": "success", "student_id": student_id, "term": term})

if __name__ == "__main__":
    with app.test_client() as client:
        # Simulate a fake payment
        response = client.post("/test/payment", json={
            "student_id": "A12345678",
            "name": "Test Student",
            "email": "test@student.edu",
            "term": "SU25"
        })
        print("Test response:", response.json)

    # Optionally start the server for real HTTP requests
    app.run(debug=True)