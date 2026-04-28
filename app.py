from flask import Flask, request, jsonify

app = Flask(__name__)

OPERATORS = ["Fusaro","Rojas","Necochea","Brinza"]

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    patients = data.get("patients", [])

    i = 0
    for p in patients:
        p["assegnato_a"] = OPERATORS[i % len(OPERATORS)]
        i += 1

    return jsonify(patients)

app.run()
