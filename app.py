import os
from flask import Flask, render_template_string, request, jsonify
import pdfplumber
import io

app = Flask(__name__)

OPERATORS = ["Fusaro", "Rojas", "Necochea", "Brinza"]

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Sostituzioni App</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; background: #f4f7f6; padding: 20px; display: flex; justify-content: center; }
        .container { max-width: 500px; width: 100%; background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; font-size: 22px; }
        .box { border: 2px dashed #3498db; padding: 30px; text-align: center; border-radius: 10px; margin: 20px 0; cursor: pointer; transition: 0.3s; }
        .box:hover { background: #eef7fe; }
        .btn { background: #3498db; color: white; border: none; padding: 15px; border-radius: 8px; width: 100%; cursor: pointer; font-size: 16px; font-weight: bold; }
        .result-item { background: #f9f9f9; padding: 12px; margin-top: 8px; border-radius: 6px; border-left: 5px solid #3498db; display: flex; justify-content: space-between; align-items: center; }
        .op-tag { font-weight: bold; color: #2980b9; background: #d6eaf8; padding: 4px 8px; border-radius: 4px; font-size: 14px; }
        #loading { display: none; color: #3498db; font-weight: bold; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Sostituzioni v1.1 🚀</h1>
        <div class="box" onclick="document.getElementById('fileInput').click()">
            <p id="fileName">📁 Clicca qui e seleziona l'Agenda PDF</p>
            <input type="file" id="fileInput" hidden accept=".pdf">
        </div>
        <button class="btn" onclick="uploadPDF()">ELABORA E ASSEGNA</button>
        <div id="loading">⏳ Elaborazione agenda in corso...</div>
        <div id="results"></div>
    </div>

    <script>
        async function uploadPDF() {
            const fileInput = document.getElementById('fileInput');
            if (fileInput.files.length === 0) return alert("Seleziona prima un file!");
            
            const resultsDiv = document.getElementById('results');
            const loading = document.getElementById('loading');
            
            resultsDiv.innerHTML = "";
            loading.style.display = "block";

            const formData = new FormData();
            formData.append("file", fileInput.files[0]);

            try {
                const response = await fetch("/process", { method: "POST", body: formData });
                const data = await response.json();
                
                loading.style.display = "none";
                
                if (data.error) {
                    resultsDiv.innerHTML = `<p style="color:red">${data.error}</p>`;
                } else {
                    let html = '<h3>Assegnazioni Generate:</h3>';
                    data.forEach(item => {
                        html += `<div class="result-item"><span>${item.paziente}</span> <span class="op-tag">${item.operatore}</span></div>`;
                    });
                    resultsDiv.innerHTML = html;
                }
            } catch (err) {
                loading.style.display = "none";
                alert("Errore durante l'elaborazione");
            }
        }
    </script>
</body>
</html>
'''

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/process", methods=["POST"])
def process():
    if 'file' not in request.files:
        return jsonify({"error": "Nessun file caricato"}), 400
    
    file = request.files['file']
    patients = []
    
    try:
        with pdfplumber.open(io.BytesIO(file.read())) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    # Logica semplice: prendiamo le righe che sembrano contenere nomi
                    # Qui puoi dirmi come sono scritti i nomi e affiniamo la ricerca
                    lines = text.split("\\n")
                    for line in lines:
                        if len(line.strip()) > 5: # Evita righe vuote o troppo corte
                            patients.append(line.strip()[:30]) # Prende i primi 30 caratteri

        # Assegnazione a rotazione
        results = []
        for i, p in enumerate(patients[:20]): # Limite a 20 per prova
            results.append({
                "paziente": p,
                "operatore": OPERATORS[i % len(OPERATORS)]
            })
        
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
