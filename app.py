from flask import Flask, render_template_string, request, jsonify
import random

app = Flask(__name__)

# Configurazione Operatori
OPERATORS = ["Fusaro", "Rojas", "Necochea", "Brinza"]

# Interfaccia HTML integrata
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Sostituzioni App</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; background: #f4f7f6; padding: 20px; color: #333; }
        .container { max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; font-size: 24px; text-align: center; }
        .box { border: 2px dashed #3498db; padding: 20px; text-align: center; border-radius: 8px; margin-bottom: 20px; cursor: pointer; }
        .btn { background: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 5px; width: 100%; cursor: pointer; font-size: 16px; }
        .result-item { background: #e8f4fd; padding: 10px; margin-top: 10px; border-radius: 5px; display: flex; justify-content: space-between; }
        .op-tag { font-weight: bold; color: #2980b9; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Sostituzioni v1.0</h1>
        <div class="box" onclick="document.getElementById('fileInput').click()">
            <p id="fileName">📁 Clicca per caricare il PDF sostituzioni</p>
            <input type="file" id="fileInput" hidden accept=".pdf" onchange="updateName()">
        </div>
        <button class="btn" onclick="processData()">ASSEGNA OPERATORI</button>
        <div id="results"></div>
    </div>

    <script>
        function updateName() {
            const input = document.getElementById('fileInput');
            document.getElementById('fileName').innerText = input.files[0].name;
        }

        function processData() {
            // Simulazione lettura PDF e assegnazione
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '<p>Elaborazione in corso...</p>';
            
            setTimeout(() => {
                const mockPatients = ["Paziente Rossi", "Paziente Bianchi", "Paziente Verdi", "Paziente Neri"];
                let html = '<h3>Assegnazioni di oggi:</h3>';
                mockPatients.forEach((p, i) => {
                    const op = ["Fusaro", "Rojas", "Necochea", "Brinza"][i % 4];
                    html += `<div class="result-item"><span>${p}</span> <span class="op-tag">${op}</span></div>`;
                });
                resultsDiv.innerHTML = html;
            }, 1500);
        }
    </script>
</body>
</html>
'''

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    # Importante: Render usa la variabile d'ambiente PORT
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
