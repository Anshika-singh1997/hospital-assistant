from flask import Flask, render_template, request, jsonify, Response
from responses import get_response
import requests as req

app = Flask(__name__)

ELEVENLABS_API_KEY = "paste_your_key_here"
VOICE_ID = "c3QefzBhE1Cx4Yl23IV3"  # change this after picking voice

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

@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    text = data.get("text", "")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    response = req.post(url, headers=headers, json=body)
    return Response(response.content, mimetype="audio/mpeg")

@app.route("/ussd", methods=["POST", "GET"])
def ussd():
    text = request.form.get("text", "") if request.method == "POST" else request.args.get("text", "")

    if text == "":
        response = "CON Welcome to Hospital Assistant - Bellary\n1. Laboratory\n2. OPD / Doctor\n3. Pharmacy\n4. Billing\n5. Emergency\n6. Accessibility / Wheelchair"
    elif text == "1":
        response = "END Laboratory is on the 2nd floor. Take stairs on your left and turn right."
    elif text == "2":
        response = "CON Select Doctor:\n1. General Physician - Dr. Ramesh Kumar\n2. Gynecologist - Dr. Priya Sharma\n3. Orthopedic - Dr. Suresh Rao\n4. Pediatrician - Dr. Anita Singh\n5. Cardiologist - Dr. Vinod Patel"
    elif text == "2*1":
        response = "END Dr. Ramesh Kumar - General Physician. OPD Room 1, Ground Floor. 9AM to 2PM."
    elif text == "2*2":
        response = "END Dr. Priya Sharma - Gynecologist. OPD Room 3, Ground Floor. 10AM to 1PM."
    elif text == "2*3":
        response = "END Dr. Suresh Rao - Orthopedic. OPD Room 4, 1st Floor. 9AM to 12PM."
    elif text == "2*4":
        response = "END Dr. Anita Singh - Pediatrician. OPD Room 2, Ground Floor. 9AM to 1PM."
    elif text == "2*5":
        response = "END Dr. Vinod Patel - Cardiologist. OPD Room 5, 1st Floor. 11AM to 2PM."
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

@app.route("/ussd-test")
def ussd_test():
    return render_template("ussd_test.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
