from flask import Flask, render_template_string, request
import os

app = Flask(__name__)

# Lista operatori
OPERATORS = ["Fusaro", "Rojas", "Necochea", "Brinza"]

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Sostituzioni App</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding: 50px; background: #f0f2f5; }
        .card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: inline-block; }
        button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Sostituzioni App 🚀</h1>
        <p>Carica il PDF per assegnare i turni</p>
        <input type="file" id="pdf">
        <br><br>
        <button onclick="alert('Assegnazione completata con successo!')">ASSEGNA ORA</button>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
