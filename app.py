from flask import Flask, render_template, request, jsonify
from responses import get_response

app = Flask(__name__)

# ── Smartphone Route (existing) ──
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_input = data.get("message", "")
    lang = data.get("lang", "english")
    reply = get_response(user_input, lang)
    return jsonify({"reply": reply})

# ── USSD Route (new) ──
@app.route("/ussd", methods=["POST", "GET"])
def ussd():
    text = request.form.get("text", "") if request.method == "POST" else request.args.get("text", "")

    if text == "":
        response = "CON Welcome to Hospital Assistant - Bellary\n"
        response += "1. Laboratory\n"
        response += "2. OPD / Doctor\n"
        response += "3. Pharmacy\n"
        response += "4. Billing\n"
        response += "5. Emergency\n"
        response += "6. Accessibility / Wheelchair"

    elif text == "1":
        response = "END Laboratory is on the 2nd floor. Take stairs on your left and turn right. Open 7AM to 7PM."

    elif text == "2":
        response = "CON Select Doctor:\n"
        response += "1. General Physician - Dr. Ramesh Kumar\n"
        response += "2. Gynecologist - Dr. Priya Sharma\n"
        response += "3. Orthopedic - Dr. Suresh Rao\n"
        response += "4. Pediatrician - Dr. Anita Singh\n"
        response += "5. Cardiologist - Dr. Vinod Patel"

    elif text == "2*1":
        response = "END Dr. Ramesh Kumar - General Physician. OPD Room 1, Ground Floor. Timing: 9AM to 2PM."

    elif text == "2*2":
        response = "END Dr. Priya Sharma - Gynecologist. OPD Room 3, Ground Floor. Timing: 10AM to 1PM."

    elif text == "2*3":
        response = "END Dr. Suresh Rao - Orthopedic. OPD Room 4, 1st Floor. Timing: 9AM to 12PM."

    elif text == "2*4":
        response = "END Dr. Anita Singh - Pediatrician. OPD Room 2, Ground Floor. Timing: 9AM to 1PM."

    elif text == "2*5":
        response = "END Dr. Vinod Patel - Cardiologist. OPD Room 5, 1st Floor. Timing: 11AM to 2PM."

    elif text == "3":
        response = "END Pharmacy is on Ground Floor near the exit on your right. Open 8AM to 8PM."

    elif text == "4":
        response = "END Billing counter is on Ground Floor to the left of main entrance. Open 8AM to 6PM."

    elif text == "5":
        response = "END EMERGENCY: Go to the back of the building. Follow red signs. Open 24 hours."

    elif text == "6":
        response = "END Wheelchair ramps at main entrance and elevator near reception. All floors accessible."

    else:
        response = "END Invalid option. Please dial *555# again."

    return response

# ── USSD Simulator (for testing in browser) ──
@app.route("/ussd-test")
def ussd_test():
    return render_template("ussd_test.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000, ssl_context=None)