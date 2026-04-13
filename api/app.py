from http import HTTPStatus
import os
from flask import redirect, send_from_directory
from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
from routes import BLUEPRINTS

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FRONT_DIR = os.path.join(CURRENT_DIR, '..', 'front')

info = Info(title="Student Predict", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Registrar blueprints
for blueprint in BLUEPRINTS:
    app.register_api(blueprint)

@app.route("/")
def home():
    return send_from_directory(FRONT_DIR, 'index.html')

@app.route("/<path:filename>")
def serve_static(filename):
    """
    Rota Catch-all: Captura qualquer requisição de arquivo 
    (ex: /styles.css, /scripts.js) e busca na pasta front.
    """
    return send_from_directory(FRONT_DIR, filename)

@app.route('/docs')
def index():
    return redirect('/openapi')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)